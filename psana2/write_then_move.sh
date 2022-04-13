#!/bin/bash
# Below show hardcoded example how to setup a live run.
# Instructions: 
# 1. Create a tmp folder and a soft link of (or copy) a bigdata file.
# 2. Create smalldata folder inside
# 3. Run this script (note -m 10 to smdwriter). This will make smdwriter sleep
#    every 10 events. 
# 4. Create a normal DataSource loop which points to tmp folder and set live=True.

rm smalldata/tmolv9418-r0175-s000-c000.smd.xtc2*
smdwriter -f tmolv9418-r0175-s000-c000.xtc2 -o smalldata/tmolv9418-r0175-s000-c000.smd.xtc2.inprogress -m 10 -n 200
mv smalldata/tmolv9418-r0175-s000-c000.smd.xtc2.inprogress smalldata/tmolv9418-r0175-s000-c000.smd.xtc2
