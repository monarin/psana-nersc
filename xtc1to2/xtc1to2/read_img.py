#!/usr/bin/env python
# -*- coding: utf-8 -*-

import psana
import matplotlib.pyplot as plt

class DisplaySPIImg():

    def __init__(self, img, figsize, **kwargs):
        self.img     = img
        self.figsize = figsize
        for k, v in kwargs.items(): setattr(self, k, v)

        self.fig, self.ax = self.create_panels()


    def create_panels(self):
        plt.rcParams.update({'font.size': 18})
        plt.rcParams.update({'font.family' : 'sans-serif'})
        fig, ax = plt.subplots(nrows = 1, ncols = 1, figsize = self.figsize)
        return fig, ax


    def plot_img(self, title = ""): 
        #self.ax.imshow(self.img, vmin = 0, vmax = 100)
        self.ax.imshow(self.img)


    def show(self): 
        self.plot_img()
        plt.show()




class PsanaImg:
    """
    It serves as an image accessing layer based on the data management system
    psana in LCLS.  
    """

    def __init__(self, exp, run, mode, detector_name):
        # Biolerplate code to access an image
        # Set up data source
        self.datasource_id = f"exp={exp}:run={run}:{mode}"
        self.datasource    = psana.DataSource( self.datasource_id )
        self.run_current   = next(self.datasource.runs())
        self.timestamps    = self.run_current.times()

        # Set up detector
        self.detector = psana.Detector(detector_name)


    def get(self, event_num, calib=False):
        # Fetch the timestamp according to event number
        timestamp = self.timestamps[int(event_num)]

        # Access each event based on timestamp
        event = self.run_current.event(timestamp)

        # Fetch image data based on timestamp from detector
        if calib:
            img = self.detector.calib(event)
        else:
            img = self.detector.image(event)
        
        return img




if __name__ == "__main__":
    # Specify the dataset and detector...
    exp, run, mode, detector_name = 'amo06516', '90', 'idx', 'pnccdFront'

    # Initialize an image reader...
    img_reader = PsanaImg(exp, run, mode, detector_name)

    # Access an image (e.g. event 796)...
    event_num = 796
    img = img_reader.get(event_num)

    # Dispaly an image...
    disp_manager = DisplaySPIImg(img, figsize = (8, 8))
    disp_manager.show()

