from read_img import PsanaImg, DisplaySPIImg

# Specify the dataset and detector...
exp, run, mode, detector_name = 'amo06516', '90', 'idx', 'pnccdFront'

# Initialize an image reader...
img_reader = PsanaImg(exp, run, mode, detector_name)

# Access an image (e.g. event 796)...
event_num = 796
img = img_reader.get(event_num, calib=True)

# Dispaly an image...
for i in range(4):
    disp_manager = DisplaySPIImg(img[i], figsize = (8, 8))
    disp_manager.show()

