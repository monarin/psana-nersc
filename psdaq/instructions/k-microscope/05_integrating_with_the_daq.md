# Integrating K-microscope into the daq environment
We decided to use BldDetector.cc as a pattern for integrating K-microscope to the daq. BldDetector receives bld data (through socket), 
match the bld timestamps with the pgp ones, and send data to the teb. 
```
pgp (transitions/L1 with timestamp) --> 
                                        [ matched by BldDetector ] --> teb
BLD (data with timestamp)           --> 
```
For K-microscope, we use pulseid (56 lower bits) for matching instead of the timestamp.
## Setup TDC data node
Apart from connecting the ethernet cable from the TDC box to eno2 on drp-neh-cmp012 with static IP, we also cabled timing (XPM 10 AMC 0 Lane 2
counting from 0) to one of the KCU1500 ports on drp-neh-cmp012. This provides timing for matching through the pgpread. See instructions
on how to seup the new timing node in the instructions folder.
NOTE that restarting tdetsim.service on drp-neh-cmp012 is problematic. After calling systemctl restart tdetsim.service, the node will
hang and needs a hand reset. The values for the drivers are however got updated afer the restart.

