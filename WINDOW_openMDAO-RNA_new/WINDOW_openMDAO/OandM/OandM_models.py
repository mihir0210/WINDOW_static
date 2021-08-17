from WINDOW_openMDAO.src.api import AbstractOandM


class OM_model1(AbstractOandM):
    def OandM_model(self, AEP, eff, N_T, P_rated):
        #costs_om = 16.0 * AEP / eff / 1000000.0
        availability = 1 #0.98
        # costs_om = 50000000.
        #costs_om = 85000000 #taken from BVG for a 1000 MW farm

        farm_rated = N_T*P_rated/1000.0
        fixed = 30e6
        variable = 58.5e3*farm_rated

        costs_om = fixed + variable

        print 'O&M costs:', costs_om
        return costs_om, availability
