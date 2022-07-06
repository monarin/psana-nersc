"""
Original code: PhotonSpectrumAna_for_MHz_Testing.ipynb
Modified to include MPI-style timing and options to select
performance test mode:
0-streaming
1 Analysis method-I
2 Analysis method-II

Questions from Mona:
1. Run 23 and 8 streams and this analysis uses data from stream 005 (tmo_opal2).
   The size of L1Accept is shown as following:
(ps-4.5.5) monarin@psanagpu110 ~ $ xtcreader -f /reg/d/psdm/tmo/tmox45419/xtc/tmox45419-r0023-s005-c000.xtc2 -n 10
event 1,   Configure transition: time 1002824825.407064904, env 0x02020001, payloadSize 33088 extent 33100
event 2,    BeginRun transition: time 1002827383.541417791, env 0x04020001, payloadSize 72 extent 84
event 3,   BeginStep transition: time 1002827383.663576050, env 0x06040001, payloadSize 0 extent 12
event 4,      Enable transition: time 1002827383.669212538, env 0x08060001, payloadSize 0 extent 12
event 5,    L1Accept transition: time 1002827383.674716486, env 0x0c090001, payloadSize 2097208 extent 2097220
event 6,    L1Accept transition: time 1002827383.682974025, env 0x0c0b0001, payloadSize 2097208 extent 2097220
event 7,    L1Accept transition: time 1002827383.691362636, env 0x0c0d0001, payloadSize 2097208 extent 2097220

    The earlier performance analysis was done on fex data (manually extracted from the original experiment).
    Each L1Accept is of around 300-600 bytes. We may need to extract just fex again?
    Should we try to test on all streams (000-007)?
    Here is the list of detectors available:
(ps-4.5.5) monarin@psanagpu110 ~ $ detnames exp=tmox45419,run=23
-----------------------
Name        | Data Type
-----------------------
tmo_fim0    | fex      
tmo_fim0    | raw      
epicsinfo   | epicsinfo
hsd         | raw      
timing      | raw      
pcav        | raw      
xgmd        | raw      
gmd         | raw      
ebeam       | raw      
tmo_atmopal | raw      
tmo_opal2   | raw      
-----------------------


"""


import matplotlib.pyplot as plt
from matplotlib import colors

import numpy as np
from scipy.optimize import curve_fit
from psana import *
import time

# Performace test required imports
import sys
from mpi4py import MPI
comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()
txt_ana = ''
txt_det = ''
txt_tot = ''
txt_r = ''

def Gaussian(x,a,b,c,d):
    return a*np.exp(-(x-b)**2/(2*c**2))+d

def Proj(img,ind1,ind2):
    return img[ind1:ind2,:].sum(0)

def PhotonSpectrumMoments(proj,hw):
    """Get the center, FWHM, AOC of the photon spectrum by direct calculation of first, second moments and array sum.
    Parameters
    ----------
    proj: photon spectrum, 1D array
    hw: predefined half width of the region centerd around spectrum peak
    Returns
    -------
    center, width and area of the photon spectrum
    
    """             
    x_max = proj.argmax()    
    
    inda = max(0,x_max-hw)
    indb = min(x_max+hw,img.shape[1]-1)
    ym = np.mean(proj[0:min(50,inda)])
    
    x = np.arange(inda,indb)                                
    y = proj[inda:indb]-ym
    y[y<0] = 0
    
    m1 = np.average(x,weights=y)
    m2 = np.sqrt(np.average((x-m1)**2,weights=y))
    
    return m1,m2,np.sum(y)

def PhotonSpectrumGauss(proj,hw):
    """Calcualte the center, FWHM, AOC of the photon spectrum by fitting with a Gaussian
    Parameters
    ----------
    proj: photon spectrum, 1D array
    hw: predefined half width of the region centerd around spectrum peak
    Returns
    -------
    center, FWHM, AOC of the photon spectrum
    
    """         
    x_max = proj.argmax()    
    
    inda = max(0,x_max-hw)
    indb = min(x_max+hw,img.shape[1]-1)
    
    x = np.arange(inda,indb)                                
    y = proj[inda:indb]
    
    p,q=curve_fit(Gaussian,x,y,p0=[proj[x_max],x_max,hw/2,np.mean(proj[0:min(20,inda)])])
    
    return p[1],2.355*np.abs(p[2]),np.sqrt(2*np.pi)*np.abs(p[2])*p[0]

def plot2d(mat,bins1,bins2,vmin=None,vmax=None,log10=True,cmap='seismic',ticks=None,xlabel=None,ylabel=None,title=None,rot=True):#'seismic'):#'RdBu_r':#'viridis'):
    """Plot 2d matrix
    Parameters
    ----------
    mat: matrix to be plotted
    bins1: bins along the x axis
    bins2: bins along the y axis
    vmin: minimum of the color scale
    vmax: maximum of the color scale
    log10: use log scale or not
    cmap: choice of cmap
    ticks: if it is None, use default tikcs, if is a tick array, use it as the ticks on the colorbar
    Returns
    -------
    plotted image handle
    
    """        
    mat = mat.copy()
    mat = np.ma.array(mat, mask=np.isnan(mat))
    if not vmin:
        vmin = mat[~np.isnan(mat)].min()
    if not vmax:
        vmax = mat[~np.isnan(mat)].max()        
        
    if rot:
        mat = np.rot90(mat)
    if log10:


        im=plt.imshow(mat,extent=[bins1.min(),bins1.max(),bins2.min(),bins2.max()],
                   aspect='auto',cmap=cmap,norm=colors.SymLogNorm(linthresh=1, linscale=1,
                                                                  vmin=vmin, vmax=vmax, clip=False))
    else:
        im=plt.imshow(mat,extent=[bins1.min(),bins1.max(),bins2.min(),bins2.max()],
                   aspect='auto',cmap=cmap,vmin=vmin,vmax=vmax)  
#     try:
#         if ticks:
#             plt.colorbar(im,ticks=np.concatenate(ticks))
#         else:
#             plt.colorbar(im)
#     except Exception as e:
#         print(e)
    if xlabel:
        plt.xlabel(xlabel)
    if ylabel:
        plt.ylabel(ylabel)
    if title:
        plt.title(title)        
    
    return im

if __name__ == "__main__":
    # 2. Define experiment, run and analysis parameters
    exp = 'tmox45419'
    runnum=23
    xtc_dir = '/cds/data/drpsrcf/users/monarin/tmox45419'
    mevt = 10000


    # [For performance test]
    test_option = 0
    if len(sys.argv) > 1:
        test_option = int(sys.argv[1])

    
    comm.Barrier()
    t1 = MPI.Wtime()

    ds = DataSource(exp=exp,run=runnum,dir=xtc_dir,max_events=mevt)
    run = next(ds.runs())
    opal = run.Detector('tmo_opal2')
    ind1,ind2,hw = 450,500,100
    
    
    if test_option == 0:
        #3-0 Streaming only
        for nevt,evt in enumerate(run.events()):
            img = opal.raw.image(evt)
    elif test_option == 1:
        # 3-1. Analysis method I - Calculate the first and second moment of the 1D array¶
        m1s = np.zeros(mevt);m2s = np.zeros(mevt);areas = np.zeros(mevt)
        t_r0 = time.monotonic()
        for nevt,evt in enumerate(run.events()):
            t_r1 = time.monotonic()
            img = opal.raw.image(evt)
            t_det = time.monotonic()
            proj = Proj(img,ind1,ind2) 
            """
            The following lines until the end of this cell should be bench marked by the MHz testing
            """
            m1,m2,area = PhotonSpectrumMoments(proj,hw)
            m1s[nevt] = m1
            m2s[nevt] = m2
            areas[nevt] = area 

            t_ana = time.monotonic()
            txt_r += str(t_r1-t_r0)+','
            txt_det += str(t_det-t_r1)+','
            txt_ana += str(t_ana-t_det)+','
            txt_tot += str(t_ana-t_r0)+','
            t_r0 = time.monotonic()
    elif test_option == 2:
        m1s_g = np.zeros(mevt);m2s_g = np.zeros(mevt);areas_g = np.zeros(mevt)
        t_r0 = time.monotonic()
        for nevt,evt in enumerate(run.events()):
            t_r1 = time.monotonic()
            if nevt>=mevt:
                break 
            img = opal.raw.image(evt)
            t_det = time.monotonic()
            proj = Proj(img,ind1,ind2)    
            """
            The following lines until the end of this cell should be bench marked by the MHz testing
            """    
            try:
                m1_g,m2_g,area_g = PhotonSpectrumGauss(proj,hw)
            except Exception as e:
                m1_g,m2_g,area_g = np.nan,np.nan,np.nan
            m1s_g[nevt] = m1_g
            m2s_g[nevt] = m2_g
            areas_g[nevt] = area_g    
            
            t_ana = time.monotonic()
            txt_r += str(t_r1-t_r0)+','
            txt_det += str(t_det-t_r1)+','
            txt_ana += str(t_ana-t_det)+','
            txt_tot += str(t_ana-t_r0)+','
            t_r0 = time.monotonic()
    


    comm.Barrier()
    t2 = MPI.Wtime()

    writeout = True
    if writeout:
        txt_ana = comm.gather(txt_ana, root=0)
        txt_det = comm.gather(txt_det, root=0)
        txt_tot = comm.gather(txt_tot, root=0)
        txt_r = comm.gather(txt_r, root=0)

        if rank == 0:
            o_ana = ''.join(txt_ana)
            o_det = ''.join(txt_det)
            o_tot = ''.join(txt_tot)
            o_r = ''.join(txt_r)

            with open('spec_ana.csv', 'w') as f:
                f.write(o_ana)
            with open('spec_det.csv', 'w') as f:
                f.write(o_det)
            with open('spec_tot.csv', 'w') as f:
                f.write(o_tot)
            with open('spec_r.csv', 'w') as f:
                f.write(o_r)
    
    if rank == 0:
        print(f'Processing time:{t2-t1:.2f} #evt:{mevt} rate:{(mevt/(t2-t1))*1e-3:.2f}kHz') 
