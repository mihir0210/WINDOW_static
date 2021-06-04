'''
Takes a case number as an input and returns the slope and constant for that scenario.
Slope and constant is for the linear fit of the Spot price vs Wind speed data.

'''

class Parameters():



    def __init__(self, future_year, operational_lifetime):

        self.base_year = 2019
        self.slope_base = -0.28 #for 2019
        self.constant_base = 43 #for 2019

        '''
        The max slope value has been taken from Denmark's data. This slope value was attained
        in 2020 where Denmark had a 50 % wind share in installed capacity and a mean wind 
        penetration (wind forecast/load forecast) was about 67 %. It is expected that NL will
        see this situation somewhere towards the end of lifetime for wind farms being commissioned 
        now in 2020-2022         
        '''
        self.max_slope = -2.3


        self.future_year = future_year
        self.lifetime = operational_lifetime

        # Here, the yearly change in slope value is calculated
        tot_diff = abs(self.max_slope) - abs(self.slope_base)

        self.slope_stepsize = tot_diff/self.lifetime

        self.constant_stepsize = 0.01*self.constant_base




       


    def baseyear(self):

        slope = self.slope_base
        constant = self.constant_base

        return slope, constant


    def var_slope(self):



        slope = self.slope_base - (self.future_year - self.base_year)*self.slope_stepsize
        constant = self.constant_base

        return slope, constant

    def var_slope_and_constant(self):

        slope = self.slope_base - (self.future_year - self.base_year)*self.slope_stepsize
        constant = self.constant_base + self.constant_stepsize

        return slope, constant

    def highest_slope(self):
        slope = self.max_slope
        constant = self.constant_base

        return slope, constant

    def random_timedependent_5y(self):

        '''Here, a random number is generated in a given range. That range is year dependent'''

        import random
        import pandas as pd

        if self.future_year <= self.base_year + 5:
            slope = random.uniform(self.slope_base, self.slope_base - self.slope_stepsize*5)

        elif self.base_year + 5 <=self.future_year <= self.base_year + 10:
            slope = random.uniform(self.slope_base - self.slope_stepsize * 5, self.slope_base - self.slope_stepsize * 10)

        elif self.base_year + 10 <= self.future_year <= self.base_year + 15:
            slope = random.uniform(self.slope_base - self.slope_stepsize * 10,
                                   self.slope_base - self.slope_stepsize * 15)

        elif self.base_year + 15 <= self.future_year <= self.base_year + self.lifetime:
            slope = random.uniform(self.slope_base - self.slope_stepsize * 15,
                                   self.slope_base - self.slope_stepsize * self.lifetime)

        constant = self.constant_base

        data = pd.read_csv('Input/stochastic_slopes_5y.txt')
        slopes = data['Slope']
        idx = self.future_year - self.base_year

        slope = slopes[idx]


        return slope, constant

    def random_timedependent_10y(self):

        '''Here, a random number is generated in a given range. That range is year dependent'''

        import random
        import pandas as pd


        if self.base_year <= self.future_year <= self.base_year + 10:
            slope = random.uniform(self.slope_base,
                                   self.slope_base - self.slope_stepsize * 10)


        elif self.base_year + 10 <= self.future_year <= self.base_year + self.lifetime:
            slope = random.uniform(self.slope_base - self.slope_stepsize * 10,
                                   self.slope_base - self.slope_stepsize * self.lifetime)

        constant = self.constant_base

        data = pd.read_csv('Input/stochastic_slopes_10y.txt')
        slopes = data['Slope']
        idx = self.future_year - self.base_year

        slope = slopes[idx]


        return slope, constant









