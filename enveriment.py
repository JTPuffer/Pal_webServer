import gym
import sklearn.mixture
from RestAPI import Client
import numpy as np
import time
import torch
import sklearn
DEFAULT_SERVER_IP = "localhost"
DEFAULT_SERVER_PORT = 8008
OBSERVATION_WINDOW = 1  # seconds


class ServerEnv(gym.Env):
    def __init__(self, client: Client,state_size=3):

        self.configs = client.get_all_configs()

        self.action_space = gym.spaces.Discrete(len(self.configs))
        self.observation_space = gym.spaces.Box(low=0, high=np.inf, shape=(4,), dtype=np.float32)
        
        self.state_size = state_size +1 # for entropy
        self.state = torch.zeros(self.state_size)

        self.client = client 
        self.first = True
        self.index_map = {}

        self.normalisation_low = 0.0
        self.normalisation_high = 100.0

        self.bandwidth = []
        self.enveriment_states = []
        self.shaplet_count = 1





    def _get_observation(self):
        perception = self.client.get_perception()
        return perception
    

    def __calculate_entropy(self, occurrences) -> float:
        """
        Calculate the Shannon entropy of a distribution of occurrences.
        
        :Args occurrences: List or numpy array of occurrences.
        :return: Entropy value.
        """
        occurrences = np.array(occurrences)
        total = np.sum(occurrences)
        probs = occurrences / total
        entropy = -np.sum(probs * np.log2(probs))
        return entropy

    def reset(self) -> tuple[torch.Tensor, torch.Tensor]:
        """
        resets the enveriment to the start
        really it does nothing 
        """
        self.state = torch.zeros(self.state_size)
        self.bandwidth = []
        return self.state, torch.zeros(1)


    
    def __perception_to_state(self, perception) -> torch.Tensor:
        state = torch.zeros(self.state_size)

        if perception['metrics']:
            metrics = perception['metrics'][0]
            avg_metric = metrics['value'] / metrics['count']
            state[0] = (avg_metric)

        entropy = []
        total_bandwidth = 0
        for i,event in enumerate(perception['events']):

            if "entropy:" in event['name']:
                
                entropy.append(event['count'])
                continue
            if event['name'] not in self.index_map:
                highest = -1

                for _, value in self.index_map.items():
                    highest = max(value, highest)

                self.index_map[event['name']] = highest+1
            
            total_bandwidth += event['value']

            avg_event = event['value'] / event['count']
            state[self.index_map[event['name']]] =  avg_event

        state[self.state_size - 1] = self.__calculate_entropy(entropy)

        self.bandwidth.append(total_bandwidth)
        # print(f"Total bandwidth: {self.bandwidth}")
        return state

    def __transform_reward(self,r, base=2) -> np.float64:
        # Add 1 before taking log to handle zeros, then subtract 1 to preserve zero
        return np.log1p(r * (base - 1)) / np.log(base)

    def set(self, action):
        self.client.set_config(self.configs[action])

    def step(self, action) -> tuple[torch.Tensor, float]:
        """
        Executes one step in the environment based on the given action.
        Args:
            action (int): The action to be executed, used to index into self.configs.

        Returns:
            state (torch.Tensor): The updated state after taking the action.
            reward (float): The reward based on the current perception metrics.
            done (bool): A flag indicating if the episode is done (True if done, False otherwise).
            info (dict): A dictionary containing additional information (empty in this case).
        """

        self.client.set_config(self.configs[action])
        time.sleep(OBSERVATION_WINDOW)

        perception = self.client.get_perception()
        reward = 0.0

        if perception:
            self.state = self.__perception_to_state(perception)

            if perception['metrics']:
                vk = perception['metrics'][0]['value']
                vt = perception['metrics'][0]['count']
                avg = vk / vt
                if avg == 0:
                    reward = 0
                else:
                    reward = self.__transform_reward(1 / avg)
                
                #reward = self.scale_cost(avg, self.normalisation_low, self.normalisation_high)
                #reward = 1 / avg #cause lower is better for response time

            for event in perception['events']:
                vk = event['value']
                vt = event['count']
                avg = vk / vt


        else:
            return self.state, torch.zeros(1)

        return self.state, torch.Tensor([reward]) # cause an update from the trajectory every time