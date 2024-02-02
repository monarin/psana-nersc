## Project detail
Srv nodes in psana2 writes smalldata files in hdf5 format as part_N.h5 and combine them using Hdf5 VirtualDataSource. 
Data in the output virtual h5 are not sorted and it's potentially difficult to analyze unsorted data. The size of the 
output h5 is also large containing > 10 billion records. We need good large-scale array operations. 
