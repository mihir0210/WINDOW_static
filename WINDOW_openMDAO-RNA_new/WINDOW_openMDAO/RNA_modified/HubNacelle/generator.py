from WINDOW_openMDAO.src.api import AbsGenerator
from .drivese_utils import size_Generator


#############################################################################
#############################  MODEL#1: DriveSE #############################
#############################################################################        
class DriveSE(AbsGenerator):
    def compute(self, inputs, outputs):
        # metadata
        self.drivetrain_design = self.options['drivetrain_design']
        
        # inputs
        self.rotor_diameter = inputs['rotor_diameter']
        self.machine_rating = inputs['machine_rating']
        self.rotor_torque = inputs['rotor_torque']
        self.gear_ratio = inputs['gear_ratio']
        self.highSpeedSide_length = inputs['hss_length']
        self.highSpeedSide_cm = inputs['hss_cm']
        self.rotor_speed = inputs['rotor_speed']
        
        size_Generator(self)

        ###### USING SCALING LAWS FROM GeneratorSE #####

        generator_mass_15MW = 372000 #in kg
        rated_torque_15MW = 20308427 #in Nm
        outputs['mass'] = generator_mass_15MW*(self.rotor_torque/rated_torque_15MW)

        print(self.rotor_torque,outputs['mass'])



        # outputs
        #outputs['mass'] = self.mass
        outputs['cm'] = self.cm
        outputs['I'] = self.I