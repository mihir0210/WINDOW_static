'''
Takes a case number as an input and returns the slope and constant for that scenario.
Slope and constant is for the linear fit of the Spot price vs Wind speed data.

'''

class Parameters():



    def __init__(self, future_year, operational_lifetime):

        self.base_year = 2019
        self.slope_base = -0.28 # -0.28 for 2019
        self.constant_base = 80 #43 for 2019

        '''
        The max slope value has been taken from Denmark's data. This slope value was attained
        in 2020 where Denmark had a 50 % wind share in installed capacity and a mean wind 
        penetration (wind forecast/load forecast) was about 67 %. It is expected that NL will
        see this situation somewhere towards the end of lifetime for wind farms being commissioned 
        now in 2020-2022         
        '''
        self.max_slope = -2.3 #-2.3
        self.max_constant = 110


        self.future_year = future_year
        self.lifetime = operational_lifetime

        # Here, the yearly change in slope value is calculated
        tot_diff = abs(self.max_slope) - abs(self.slope_base)

        self.slope_stepsize = tot_diff/self.lifetime

        tot_diff = abs(self.max_constant) - abs(self.constant_base)


        #self.constant_stepsize = 0.01*self.constant_base
        self.constant_stepsize = tot_diff/self.lifetime




       


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
        constant = self.constant_base + (self.future_year - self.base_year)*self.constant_stepsize

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

    def eneco_coeff(self):

        coeff_2025 = [-2.42, 77.5]
        coeff_2030 = [-4.66, 95.3]
        coeff_2035 = [-5.48, 104]
        coeff_2040 = [-5.62, 104]

        if self.future_year == self.base_year:
            slope = self.slope_base
            constant = self.constant_base

        if self.future_year> self.base_year and self.future_year<=2025:
            slope_stepsize = (abs(coeff_2025[0]) - abs(self.slope_base))/(2025-self.base_year)
            constant_stepsize = (coeff_2025[1] - self.constant_base)/(2025-self.base_year)

            slope = self.slope_base - (self.future_year - self.base_year) * slope_stepsize
            constant = self.constant_base + (self.future_year - self.base_year) * constant_stepsize

        elif self.future_year>2025 and self.future_year<=2030:
            slope_stepsize = (abs(coeff_2030[0]) - abs(coeff_2025[0]))/(2030 - 2025)
            constant_stepsize = (coeff_2030[1] - coeff_2025[1])/(2030 - 2025)

            slope = coeff_2025[0] - (self.future_year - 2025) * slope_stepsize
            constant = coeff_2025[1] + (self.future_year - 2025) * constant_stepsize

        elif self.future_year>2030 and self.future_year<=2035:

            slope_stepsize = (abs(coeff_2035[0]) - abs(coeff_2030[0])) / (2035 - 2030)
            constant_stepsize = (coeff_2035[1] - coeff_2030[1]) / (2035 - 2030)

            slope = coeff_2030[0] - (self.future_year - 2030) * slope_stepsize
            constant = coeff_2030[1] + (self.future_year - 2030) * constant_stepsize

        elif self.future_year>2035 and self.future_year<=2040:

            slope_stepsize = (abs(coeff_2040[0]) - abs(coeff_2035[0])) / (2040 - 2035)
            constant_stepsize = (coeff_2040[1] - coeff_2035[1]) / (2040 - 2035)

            slope = coeff_2035[0] - (self.future_year - 2035) * slope_stepsize
            constant = coeff_2035[1] + (self.future_year - 2035) * constant_stepsize

        elif self.future_year>2040:
            slope = coeff_2040[0]
            constant = coeff_2040[1]

        return slope, constant




















