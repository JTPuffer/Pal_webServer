
import matplotlib.pyplot as plt
from abc import ABC, abstractmethod

from Indicators import EMA
from Indicators import Bollinger

class Grap:
    

    def __init__(self):
        self.x = []
        self.y = []
        self.colour_arr = []

        plt.ion()
        self.fig, self.ax = plt.subplots(figsize=(10, 6))
        self.ax.set_xlabel('Episode')
        self.ax.set_ylabel('Reward')
        self.ax.set_title('Training Progress - Live Reward Updates')
        self.ax.grid(True)
        
        plt.show(block=False)

        self.ema3 = EMA(3)

        

        self.bollinger = Bollinger(2, EMA(5), EMA(5))


        pass




    def add_point(self, y: float, colour:str):
        self.y.append(y)
        self.x.append(len(self.x))
        self.colour_arr.append(colour)
        # self.ax.clear()
        if len(self.x) < 2:
            self.ema3.update(y)
            return
        

        # self.ax.plot( self.x[-2:],[self.ema13.value,self.ema13.update(y)],'r-',color = "black")
        #self.ax.plot( self.x[-2:],[self.ema7.value,self.ema7.update(y)], 'r-',color = "black")

        #must be 1st as uses the last value

        last_ema, new_ema = self.ema3.update(y)

        #self.ax.plot( self.x[-2:],[last_ema, new_ema], 'r-',color = "black")

        old_bottom_band, old_top_band, bottom_band, top_band = self.bollinger.update(y)


        #self.ax.plot( self.x[-2:],[last_ema, new_ema], 'r-',color = self.colour_arr[-1])
        self.ax.plot( self.x[-2:], self.y[-2:], 'r-',color =self.colour_arr[-1])

        ##bollinger bands
        #self.ax.plot( self.x[-2:],[old_top_band, top_band], 'r-',color = "black")
        self.ax.plot( self.x[-2:],[old_bottom_band, bottom_band], 'r-',color = "black")

        
        # for i in range(len(self.x)):
        #self.ax.plot(self.x[-2:],self.y[-2:], 'b-',color = self.colour_arr[-1])
        
        self.ax.legend()


        self.ax.relim()  # Recalculate limits
        self.ax.autoscale_view()  # Autoscale the view
        self.fig.canvas.draw()
        self.fig.canvas.flush_events()
    def show(self):
        plt.ioff()
        plt.show()
        pass

    def get_x(self):
        return self.x

    def pause(self):
        pass

    def reset(self):
        self.x = []
        self.y = []
        self.colour_arr = []
        self.ax.clear()



