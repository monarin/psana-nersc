Converts xtc1 to xtc2 file  
  
For SPI (spinifel/cmtip),
Input: experiment id, run number  
Output: xtc2 file with intensities and photon energy

Note:  
List of experiments:  
https://www.nature.com/articles/s41597-020-00745-2/tables/3  

Spinifel hdf5 file contains:  
  - pixel_position_reciprocal  
  - pixel_index_map  
  - intensities  
  - orientations  
  - volume
Obtain photon energy:
Note from Chuck:  
https://github.com/lcls-psana/psocake/blob/7d21e96961c04f149c64e9c810a8eff7f60d5982/psocake/peakFinderClient.py#L183  
Code possibly needed:
1. Photon Energy  
es = ps.ds.env().epicsStore()  
try:  
    md.small.wavelength = es.value('SIOC:SYS0:ML00:AO192')  
except:  
    md.small.wavelength = 0  
ebeamDet = psana.Detector('EBeam')  
ebeam = ebeamDet.get(ps.evt)  
try:  
    photonEnergy = ebeam.ebeamPhotonEnergy()  
    pulseEnergy = ebeam.ebeamL3Energy()  # MeV  
except:  
    photonEnergy = 0  
    pulseEnergy = 0  
    if md.small.wavelength > 0:  
        h = 6.626070e-34  # J.m  
        c = 2.99792458e8  # m/s  
        joulesPerEv = 1.602176621e-19  # J/eV  
        photonEnergy = (h / joulesPerEv * c) / (md.small.wavelength * 1e-9)  
2. Intensities
 
