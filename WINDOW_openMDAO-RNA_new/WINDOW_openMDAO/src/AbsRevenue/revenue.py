from openmdao.api import ExplicitComponent


class AbsRevenue(ExplicitComponent):
    def initialize(self):

        self.metadata.declare('wind_speed_file', desc='wind speed data file')
        self.metadata.declare('spot_price_file', desc ='Spot price data file')


    def setup(self):



        # inputs

        self.add_input('cut_in_speed', units='m/s', desc='cut-in wind speed')
        self.add_input('rated_wind_speed', units='m/s', desc='rated wind speed')
        self.add_input('cut_out_speed', units='m/s', desc='cut-out wind speed')
        self.add_input('swept_area', units='m**2', desc='rotor swept area')
        self.add_input('machine_rating', units='kW', desc='machine rating')
        self.add_input('drive_train_efficiency', desc='efficiency of aerodynamic to electrical conversion')
        self.add_input('rotor_cp', desc='rotor power coefficient')
        self.add_input('farm_eff', desc='Farm wake efficiency')
        self.add_input('n_turbines', desc='number of turbines')

        self.add_input('total_investment', desc='Total initial investment')
        self.add_input('O_M', desc='Operation and Maintenance costs')


        # outputs
        self.add_output('Revenue',  desc='Lifetime revenue')
        self.add_output('NPV', desc='Net present value')
        self.add_output('IRR',  desc='Internal rate of return')
