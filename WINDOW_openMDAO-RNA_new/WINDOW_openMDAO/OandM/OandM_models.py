from WINDOW_openMDAO.src.api import AbstractOandM


class OM_model1(AbstractOandM):
    def OandM_model(self, AEP, eff):
        costs_om = 16.0 * AEP / eff / 1000000.0
        availability = 1 #0.98
        # costs_om = 50000000.
        costs_om = 85000000 #taken from BVG for a 1000 MW farm
        print 'O&M costs:', costs_om
        return costs_om, availability
