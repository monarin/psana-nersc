## Note abou the setup
[Official Confluence Page](https://confluence.slac.stanford.edu/display/LCLSIIData/Integrating+Detectors+in+RIX)
### Train Generator
psdaq/psdaq/seq/traingenerator.py
```
traingenerator -s 14000 -b 28 -n 32001 -r 2 -d "burst" -t 910000 >& /tmp/beam.py
```
Arguments are:
start_bucket (-s)      : starting bucket of first train within the pattern
bunch_spacing (-b)     : buckets between bunches within the train
bunches_per_train (-n) : bunches within each train 
train_spacing (-t)     : buckets from last bunch of previous train to first bunch of the next train
repeat (-r)            : # of times to repeat (-1 = indefinite)
notify (-N)            : assert checkpoint when done
train 1                   train 2
                          offset       bunch              bunch              bunch          ...32001 bunches/train
[       ] 910000 buckets [ 14000 | -- 28 buckets -- | -- 28 buckets -- | -- 28 buckets -- |

       
