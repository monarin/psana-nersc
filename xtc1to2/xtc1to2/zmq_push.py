from read_img import PsanaImg, DisplaySPIImg
from read_photon_energy import PsanaPhotonEnergy

# Specify the dataset and detector...
exp, run, mode, detector_name = 'amo06516', '90', 'idx', 'pnccdFront'

# Initialize an image reader...
img_reader = PsanaImg(exp, run, mode, detector_name)

# Initialize photon energy reader
phe_reader = PsanaPhotonEnergy(exp, run, mode)

# Access an image (e.g. event 796)...
event_num = 796
img = img_reader.get(event_num, calib=True)
photon_energy = phe_reader.get(event_num)
ts = img_reader.timestamp(event_num)


print(f'event_num={event_num} ts={ts} {img.shape} photon energy:{photon_energy:.3f}')


