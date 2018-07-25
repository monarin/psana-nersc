import sys, subprocess
import numpy as np
import os

def grepThis(cmd):
  process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
  out, err = process.communicate()
  return out.strip()

if __name__ == "__main__":
  maxSeq = int(sys.argv[1])
  runSeq = range(95, 95+maxSeq)
  trialNo = int(sys.argv[2])
  path = sys.argv[3]

  with open('profilecctbx.csv','w') as f: f.write('')

  for i in xrange(maxSeq):
    
    logPath = os.path.join(path, 'r'+str(runSeq[i]).zfill(4), str(trialNo).zfill(3), 'stdout', 'log_rank*')
    
    # Lib import time
    cmd = "grep PROFILEJUMP "+logPath+" | awk '{print $4}'"
    try:
      deltaJump = np.array([float(j) for j in grepThis(cmd).split('\n')])
    except Exception:
      deltaJump = None

    # Opening DataSource time 
    cmd = "grep PROFILEDS "+logPath+" | awk '{print $5}'"
    try:
      deltaDss = np.array([float(j) for j in grepThis(cmd).split('\n')])
    except:
      deltaDss = None

    # Integration time
    cmd = "grep PROFILEINT "+logPath+" | awk '{print $4}'"
    try:
      deltaInt = np.array([float(j) for j in grepThis(cmd).split('\n')])
    except:
      deltaInt = None

    # Master process
    cmd = "grep PROFILEMASTEREVT "+logPath+" | awk '{print $10}'"
    try:
      deltaMasters = np.array([float(j) for j in grepThis(cmd).split('\n')])
    except:
      deltaMasters = None
    
    print "Run: ", runSeq[i]
    print np.mean(deltaJump), np.mean(deltaDss), np.mean(deltaInt), np.mean(deltaMasters)
    #print "Client Process: %6.4f Data Source: %6.4f Integration: %6.4f Master Process: %6.4f"(np.mean(deltaJump), np.mean(deltaDss), np.mean(deltaInt), np.mean(deltaMasters))
    txt = ""
    for a,b,c,d in zip(deltaJump, deltaDss, deltaInt, deltaMasters):
      txt += str(a)+','+str(b)+','+str(c)+','+str(d)+'\n'
    with open('profilecctbx.csv','a') as f: f.write(txt)

