from abc import ABC, abstractmethod

import math

class Indicator(ABC):
    @abstractmethod
    def update(self, new_value:float) :
        pass


class EMA(Indicator):
    def __init__(self, days):
        self.alpha = 2 / (days + 1)
        self.days = days
        self.value = 0
        self.last_variance = 0
    
    def update(self, new_value: float):
        if self.value == 0:
            self.value = new_value
            return self.value,self.value
        old = self.value
        self.value = new_value * self.alpha + (self.value * (1 - self.alpha))
        return old , self.value
    
    

class Bollinger(Indicator):
    def __init__(self, days, Average_class: Indicator, squared_diff: Indicator):
        self.average_stream = Average_class

        self.days = days
        self.rolling_average = 0


        self.squared_diff_stream = squared_diff
        self.bottom_band = 0
        self.top_band = 0
    

    
    def update(self, new_value):
        # if self.var == 0:
        #     self.var = new_value
        #     self.rolling_average = self.average_stream.update(new_value)


        
        _ , self.rolling_average = self.average_stream.update(new_value)
        _ , variance = self.squared_diff_stream.update((new_value - self.rolling_average) ** 2)

        std = math.sqrt(abs(variance))


        old_bottom_band = self.bottom_band
        old_top_band = self.top_band


        self.bottom_band = self.rolling_average - 1 * std
        self.top_band = self.rolling_average + 1 * std

        return old_bottom_band, old_top_band, self.bottom_band, self.top_band
        
        