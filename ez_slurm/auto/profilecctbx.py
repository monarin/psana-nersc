import sys, subprocess
import numpy as np

def grepThis(cmd):
  process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
  out, err = process.communicate()
  return out.strip()

if __name__ == "__main__":
  procId = sys.argv[1]
  maxSeq = int(sys.argv[2])
  runSeq = range(95, 95+maxSeq)
  exp = sys.argv[3]
  trialNo = int(sys.argv[4])
  print "#RunSeq QueueWait FastestStartCore SlowestStartCore Client-ServerProcess WallTime"
  for i in xrange(maxSeq):
    if runSeq[i] in (98, 104): continue
    cmd = "grep t_submit submit_"+str(procId)+"_"+str(i+1)+"_"+str(trialNo)+".sh | awk '{print $2}'"
    try:
      startSubmit = float(grepThis(cmd))
    except Exception:
      startSubmit = 0

    cmd = "grep PSJob log_"+str(procId)+"_"+str(i+1)+"_"+str(trialNo)+".txt | awk '{print $4}'"
    try:
      startJob = float(grepThis(cmd))
    except Exception:
      startJob = 0

    cmd = "grep PSJob log_"+str(procId)+"_"+str(i+1)+"_"+str(trialNo)+".txt | awk '{print $5}'"
    try:
      endJob = float(grepThis(cmd))
    except Exception:
      endJob = 0

    cmd = "grep PROFILEPHIL log_"+str(procId)+"_"+str(i+1)+"_"+str(trialNo)+".txt | awk '{print $4}'"
    try:
      deltaPhils = np.array([float(j) for j in grepThis(cmd).split('\n')])
    except Exception:
      deltaPhils = None

    bbPath = "/var/opt/cray/dws/mounts/batch/myBBsml_striped_scratch/d/psdm/cxi"
    cmd = "grep PROFILEPROC "+bbPath+"/%s/scratch/discovery/dials/r%04d/%03d/stdout/log_rank0000.out | awk '{print $4}'"%(exp, runSeq[i], trialNo)
    try:
      deltaClientServer = float(grepThis(cmd))
    except:
      deltaClientServer = 0
    
    cmd = "grep PROFILEPROCRANK "+bbPath+"/%s/scratch/discovery/dials/r%04d/%03d/stdout/log_rank*.out | awk '{print $3}'"%(exp, runSeq[i], trialNo)
    try:
      eachProcStarts = np.array([float(j) for j in grepThis(cmd).split('\n')])
      deltaProcStarts = eachProcStarts - startJob
    except:
      pass
    
    cmd = "grep PROFILEDS "+bbPath+"/%s/scratch/discovery/dials/r%04d/%03d/stdout/log_rank*.out | awk '{print $5}'"%(exp, runSeq[i], trialNo)
    try:
      deltaDss = np.array([float(j) for j in grepThis(cmd).split('\n')])
    except:
      deltaDss = None

    cmd = "grep PROFILEMASTEREVT "+bbPath+"/%s/scratch/discovery/dials/r%04d/%03d/stdout/log_rank*.out | awk '{print $10}'"%(exp, runSeq[i], trialNo)
    try:
      deltaMasters = np.array([float(j) for j in grepThis(cmd).split('\n')])
    except:
      deltaMasters = None
    
    cmd = "grep PROFILEJUMP "+bbPath+"/%s/scratch/discovery/dials/r%04d/%03d/stdout/log_rank*.out | awk '{print $4}'"%(exp, runSeq[i], trialNo)
    try:
      deltaJumps = np.array([float(j) for j in grepThis(cmd).split('\n')])
    except:
      deltaJumps = None

    cmd = "grep PROFILEINT "+bbPath+"/%s/scratch/discovery/dials/r%04d/%03d/stdout/log_rank*.out | awk '{print $4}'"%(exp, runSeq[i], trialNo)
    try:
      deltaInts = np.array([float(j) for j in grepThis(cmd).split('\n')])
    except:
      deltaInts = None

    print i+1, runSeq[i], startJob - startSubmit, np.min(deltaProcStarts), np.max(deltaProcStarts), deltaClientServer, endJob - startJob, \
        np.min(deltaPhils), np.max(deltaPhils), np.mean(deltaPhils), np.median(deltaPhils), \
        np.min(deltaDss), np.max(deltaDss), np.mean(deltaDss), np.median(deltaDss), \
        np.min(deltaMasters), np.max(deltaMasters), np.mean(deltaMasters), np.median(deltaMasters), \
        np.min(deltaJumps), np.max(deltaJumps), np.mean(deltaJumps), np.median(deltaJumps), \
        np.min(deltaInts), np.max(deltaInts), np.mean(deltaInts), np.median(deltaInts)
         
        
    strPhils = '\n'.join([str(tmp) for tmp in deltaPhils])
    strDss = '\n'.join([str(tmp) for tmp in deltaDss])
    strMasters ='\n'.join([str(tmp) for tmp in deltaMasters])
    strJumps = '\n'.join([str(tmp) for tmp in deltaJumps])
    strInts = '\n'.join([str(tmp) for tmp in deltaInts])
    with open('profilephils_'+str(runSeq[i])+'.csv','w') as f: f.write(strPhils)
    with open('profiledss_'+str(runSeq[i])+'.csv','w') as f: f.write(strDss)
    with open('profilemasters_'+str(runSeq[i])+'.csv','w') as f: f.write(strMasters)
    with open('profilejumps_'+str(runSeq[i])+'.csv','w') as f: f.write(strJumps)
    with open('profileints_'+str(runSeq[i])+'.csv','w') as f: f.write(strInts)
