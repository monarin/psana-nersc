#Code will produce two h5 files; each containing multiple arays.

#logistical support
import h5py, time, math, string, random
import numpy as np

#data parameters
startnum=0          #counts start at 0
tsFactor=1000       #timestamps increase by factor of this number
datSize=150000        #legth of data for first h5 file ~filesize in GB is this number divided by 500 
datSize2=60         #legth of data for second h5 file
datAmount=250000    #width of data for h5 files

#--------------------PHASE I ~ File 1--------------------
#data chunking for fast writing
chunk = np.array([range(250000) for i in range(10)])
row_count = chunk.shape[0]
eventnum = slot #we changed all 'slot' to 'eventnum'

start = time.time()

with h5py.File('file1.h5', 'w') as f:
#creation of timestamp array 1
  firstStamp = f.create_dataset('timestamp1', (datSize,), dtype='i')
  for eventnum in range(datSize):
    startstamp = time.time()
    firstStamp[eventnum]=startnum+(eventnum*tsFactor)
    endstamp = time.time()
   # print 'timestamp times', endstamp-startstamp

#creation of small array
  smallDat1 = f.create_dataset('smalldata', (datSize,), dtype='S7')
  for eventnum in range(datSize):
    startsmall = time.time()
    smallDat1[eventnum]='kjadsdl'
    endsmall = time.time()
    #print 'small dat time', endsmall-startsmall

#creation of large array 1
  maxshape = (None,) + chunk.shape[1:]
  bigDat1 = f.create_dataset('bigdata1', shape=chunk.shape, maxshape=maxshape,
    chunks=chunk.shape, dtype=chunk.dtype)
  bigDat1[:] = chunk
  for i in range(datSize/chunk.shape[0]):
    start1 = time.time()
    bigDat1.resize(row_count + chunk.shape[0], axis=0)
    bigDat1[row_count:] = chunk
    row_count += chunk.shape[0]
    end1 = time.time()
    #print i, 'bigdat time', end1-start1
end = time.time()
#print 'total time', end-start


'''
#for debugging
print 'Timestamp 1:',firstStamp[()]
print ''
print 'Big Data 1: ',bigDat1[()]
print ''
print 'Small Data: ',smallDat1[()]
print ''
'''
'''
#--------------------PHASE II ~ File 2-------------------
h5File2 = h5py.File('file2.h5', 'w')

#creation of timestamp array 2
secondStamp = h5File2.create_dataset('timestamp2', (datSize2,), dtype='i')
for eventnum in range(datSize2):
    secondStamp[eventnum]=startnum+(eventnum*2*tsFactor)

#creation of large array 2
bigDat2 = h5File2.create_dataset('bigdata2', (datSize2, datAmount), dtype='i')
for eventnum in range(datSize2):
    bigDat2[eventnum] = np.array(range(datAmount))

#for debugging
print 'Timestamp 2:',secondStamp[()]
print ''
print 'Big Data 2:', bigDat2[()]

h5File2.close()
'''
