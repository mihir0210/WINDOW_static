'''
Takes a case number as an input and returns the slope and constant for that scenario.
Slope and constant is for the linear fit of the Spot price vs Wind speed data.

'''

class Parameters:

       


    def base_year(self):

        slope = -0.1012
        constant = 41

        return slope, constant


    def var_slope(self):

        slope = -0.1012*5
        constant = 41

        return slope, constant

    def var_slope_and_constant(self):

        slope = -0.1012*10
        constant = 41*1.25

        return slope, constant
