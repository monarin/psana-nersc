'''
NEW AND IMPROVED FILECREATE!!!!
Creates multiple h5 files each with unique variable length timestamps.

Input the file size you want approximately in GB into 'file1size' variable
Input the number of h5 files you want into 'number_of_files' variable

CODE MAY NEED CLEANUP IN ORDER TO BE MORE PROFESSIONAL (i.e. using data.resize
    for the subsequential h5 file loop instead of appending a list)
'''

#Logistical Support
import h5py, random
import numpy as np

#INPUT YOUR OPTIONS HERE!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
file1size = 2 #Size of File 1 in GB (aproximately ... sort of)
number_of_files = 10 #Total number of h5 files you want

#Initialization variables
startnum = 0
r = 2 
tsFactor = 1
if file1size == 0:
    datSize = 150
else:
    datSize = file1size*20000
datAmount = int(round(datSize/6))
smallDatColors = ['red', 'blue', 'green']

if datSize < 100000:
    max_block_size = int(round(datSize*.03))
    bunch = int(round(datSize/50))
else:
    max_block_size= int(round(datSize*.003))
    bunch = int(round(datSize/300))
print 'MAXIMUM TIMESTAMP2 BLOCK SIZE:', max_block_size, 'BUNCH:', bunch

chunk = np.array([range(datAmount) for i in range(10)])
row_count = chunk.shape[0]

#Phase I --Creating the first h5 file--
with h5py.File('file1.h5', 'w') as f:
    #Creating Small Data
    smallDat1 = f.create_dataset('smalldata', (datSize,), dtype='S5')
    for event in range(datSize):
        smallDat1[event] = (random.choice(smallDatColors))
    print 'SMALLDATA1:', smallDat1[:]

    #Creating first Timestamp array
    firstStamp = f.create_dataset('timestamp1', (datSize,), dtype='i')
    for stamp in range(datSize):
        firstStamp[stamp] = startnum+(stamp*tsFactor)
    print 'TIMESTAMP1:', firstStamp[:]
    
    #Creating first Event array
    maxshape = (None,) + chunk.shape[1:]
    bigDat1 = f.create_dataset('bigdata1', shape=chunk.shape,
      maxshape=maxshape, chunks=chunk.shape, dtype=chunk.dtype)
    bigDat1[:] = chunk
    for i in range(int(datSize/chunk.shape[0])-1):
        bigDat1.resize(row_count + chunk.shape[0], axis=0)
        bigDat1[row_count:] = chunk
        row_count += chunk.shape[0]
    print 'BIGDATA1:', bigDat1[:]

#Phase II --Creating subsequent h5 files--
#Crappy way of getting the time stamps to work out below...
#Please fix with datset.resize as done with File1's bigDat1
while r <= number_of_files:
  list = np.arange(datSize)[...]
  amendment = [] 
  while startnum < len(list):   
    sel_n = int(round(random.choice(range(startnum,startnum+bunch))))
    block_size = random.choice(range(max_block_size))
    if sel_n+block_size > len(list):
        block_size = len(list)- sel_n
    for i in range(sel_n, sel_n+block_size):
        amendment.append(list[i])
    startnum = sel_n+block_size
    
  with h5py.File('file%s.h5' %r, 'w') as g:
      #Creating Timestamp arrays
      secondStamp = g.create_dataset('timestamp%s' %r, (len(amendment),), dtype='i')    
      length = len(amendment)
      secondStamp[:length]=amendment[:]
      print 'TIMESTAMP', r, ':', secondStamp[:]
    
      #Creating Event Data arrays
      maxshape = (None,) + chunk.shape[1:]
      bigDat2 = g.create_dataset('bigdata%s' %r, shape=chunk.shape, maxshape=maxshape,
        chunks=chunk.shape, dtype=chunk.dtype)
      bigDat2[:] = chunk
      for i in range(int(len(amendment)/chunk.shape[0])-1):
        bigDat2.resize(row_count + chunk.shape[0], axis=0)
        bigDat2[row_count:] = chunk
        row_count += chunk.shape[0]
      print 'BIGDATA', r, ':', bigDat2[:]

  #Part of the loop
  r = r+1
  startnum = 0
