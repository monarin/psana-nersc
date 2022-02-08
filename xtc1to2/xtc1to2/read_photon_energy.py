import psana

class PsanaPhotonEnergy:
    """ Uses psana1 ebeam and epicsStore to retrieve 
    photon energy."""
    def __init__(self, exp, run, mode):
        # Biolerplate code to access an image
        # Set up data source
        self.datasource_id = f"exp={exp}:run={run}:{mode}"
        self.datasource    = psana.DataSource( self.datasource_id )
        self.run_current   = next(self.datasource.runs())
        self.timestamps    = self.run_current.times()

        # Set up detector and epicsStore
        self.ebeam_det = psana.Detector('EBeam')
        self.es = self.datasource.env().epicsStore()

    def get(self, event_num): 
        # Fetch the timestamp according to event number
        timestamp = self.timestamps[int(event_num)]

        # Access each event based on timestamp
        event = self.run_current.event(timestamp)

        # Fetch small wavelenthg (if any) as fallback plan
        try:
            wavelength = self.es.value('SIOC:SYS0:ML00:AO192')
        except:
            wavelength = 0

        # Try to get photon energy from ebeam if not
        # calculate it from wavelenght (if any)
        ebeam = self.ebeam_det.get(event)
        try:
            photonEnergy = ebeam.ebeamPhotonEnergy()
        except:
            photonEnergy = 0
            if wavelength > 0:
                h = 6.626070e-34 # J.m
                c = 2.99792458e8 # m/s
                joulesPerEv = 1.602176621e-19 # J/eV
                photonEnergy = (h / joulesPerEv * c) / (wavelength * 1e-9)

        return photonEnergy
