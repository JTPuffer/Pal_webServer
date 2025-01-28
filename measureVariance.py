from RestAPI import Client

from Streaming import Grap
import subprocess
import select

from enveriment import ServerEnv

process = subprocess.Popen(["/home/matthew/dana/dana", "client.Cycle"],
            stdout=subprocess.PIPE,
             stderr=subprocess.PIPE,
             text=True,
             cwd= "/home/matthew/thirdyear/FINAL/pal_webserver",
             )
    
    
graph = Grap()
client = Client("localhost", 8008)
env = ServerEnv(client=client)

#action 0 
action = 0

#array of 10 colours for matplot lib
colours = [
    'blue', 'green', 'red', 'purple', 'orange',
    'brown', 'pink', 'gray', 'olive', 'cyan',
    'yellow', 'magenta', 'teal', 'navy', 'gold',
    'lime', 'maroon', 'turquoise', 'darkviolet', 'khaki'
]
enverimennt_to_colour = {}

colour = ""

while process.poll() == None:

    ready_to_read,_,_ = select.select([process.stdout], [], [], 0)
    
    if ready_to_read:
        workload = process.stdout.readline()
        print(workload)
        if workload not in enverimennt_to_colour:
            enverimennt_to_colour[workload] = colours.pop()

        colour = enverimennt_to_colour[workload]
        
        
    next_state, reward = env.step(action)


    graph.add_point(reward[0].item(), colour)


import numpy as np
print(f"variance is {np.var(graph.y)}")
graph.show()
