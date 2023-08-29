## Adding new epix detector
### Configuration file
For example, epixhr2x2_config.py allows you to work with registers. This python script  
- Contains classes that are instantiated by c++.
- Calls yml file (structured the same way as we see in Config Edit Gui)
- Note on variables: cbase (camera base) and pbase (pci base).
- 
### Detector files
Usually we copy an existing xxdetector.cc file as a template to a new one and modify the values inside. 

### Cnf file
Add a new entry with -D to the new detector.  
