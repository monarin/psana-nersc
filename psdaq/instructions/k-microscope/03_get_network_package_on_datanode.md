The output/data port on the tdc is connected to another node (data node, currently drp-neh-cmp012). We need to set the static IP on this node in order to receive data from the tdc box.
## Setting static IP 
On drp-neh-cmp012, eno2 is the interface that connects to the tdc data port. Set its IP and netmask to the following values specifically:
```
monarin@drp-neh-cmp012 ~ sudo ifconfig eno2 10.0.0.1
monarin@drp-neh-cmp012 ~ sudo ifconfig eno2 netmask 255.255.255.0
```
You should be able to talk to the tdc (10.0.0.20)
```
monarin@drp-neh-cmp012 ~ ping 10.0.0.20
PING 10.0.0.20 (10.0.0.20) 56(84) bytes of data.
64 bytes from 10.0.0.20: icmp_seq=1 ttl=64 time=0.175 ms
64 bytes from 10.0.0.20: icmp_seq=2 ttl=64 time=0.060 ms
64 bytes from 10.0.0.20: icmp_seq=3 ttl=64 time=0.058 ms
```
## Installing Surface Concept software
The tdc box needs to be configured before we can talk to it from the readout node. 
Note that following sofware are located here:
```
(daq_20241215) monarin@drp-neh-cmp011 python ls ~monarin/sw/kmicro/SurfaceConcept/20241206/ -l
total 30504
-rw-r--r-- 1 monarin xu 26880000 Jan 14 11:30 dldgui2_centos7_lcls2_v0.2.11.tar.gz
-rw-r--r-- 1 monarin xu  4249600 Jan 14 11:30 scTDC1_centos7_lcls2_v1.3023.13.tar.gz
-rw-r--r-- 1 monarin xu   102400 Jan 14 11:31 scTDC1_devclass45_centos7_lcls2_v0.4.6.tar.gz
drwxr-xr-x 1 monarin xu        0 Jan 14 11:39 tdc_drivers
drwxr-xr-x 1 monarin xu        0 Jan 14 11:40 tdc_gui
drwxr-xr-x 1 monarin xu        0 Jan 14 11:41 tdc_ini_files
```
1. Copy all the share objects and the include files to /opt
```
cp -r ~monarin/sw/kmicro/SurfaceConcept/20241206/tdc_drivers/scTDC1_centos7_lcls2_v1.3023.13/include /opt/kmicro/
cp -r ~monarin/sw/kmicro/SurfaceConcept/20241206/tdc_drivers/scTDC1_centos7_lcls2_v1.3023.13/lib /opt/kmicro/
cp ~monarin/sw/kmicro/SurfaceConcept/20241206/tdc_drivers/scTDC1_devclass45_centos7_lcls2_v1.3023.13/* /opt/kmicro/lib/
```
2. Link the so
```
sudo ldconfig -v /opt/kmicro/lib/
```
3. Prior to running to gui (according to README.txt in guit director), you need to copy the libscDeviceClass45.so.version to this directory and creates soft links correctly as shown below:
```
(daq_20241215) monarin@drp-neh-cmp012 dldgui2_centos7_lcls2_v0.2.11 cp ~/sw/kmicro/SurfaceConcept/20241206/tdc_drivers/scTDC1_devclass45_centos7_lcls2_v1.3023.13/libscDeviceClass45.so.0.4.6 .
(daq_20241215) monarin@drp-neh-cmp012 dldgui2_centos7_lcls2_v0.2.11 ln -s libscDeviceClass45.so.0.4.6 libscDeviceClass45.so
(daq_20241215) monarin@drp-neh-cmp012 dldgui2_centos7_lcls2_v0.2.11 ln -s libscDeviceClass45.so.0.4.6 libscDeviceClass45.so.0
(daq_20241215) monarin@drp-neh-cmp012 dldgui2_centos7_lcls2_v0.2.11 ln -s libscDeviceClass45.so.0.4.6 libscDeviceClass45.so.0.4
```
4. Run the gui. Note that the first LD* path is for libqwt (sent by SurfaceConcept) and the second is libtiff available in our conda environment.
```
LD_LIBRARY_PATH=/cds/home/m/monarin/sw/kmicro/SurfaceConcept/20241206/tdc_gui/dldgui2_centos7_lcls2_v0.2.11:$CONDA_PREFIX/lib ./dldgui2
```

