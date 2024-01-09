## Power cycle a node
There are two ways to access ipmi: browser and CLs (not reliable).
### Using browser to power cycle a node
1. In firefox (available on psbuild-rhel7-02), go to this url:
```
https://drp-srcf-cmp002-ipmi/
```
Note that node name should be changed to the node that you want to power cycle. Click Advance and follow the instruction if landed on the security page.  
2. Username is ADMIN and password can be found here:
```
/cds/group/pcds/admin/ipmicreds/drp-srcf-cmp010-ipmi.ini
```
Again, the ini filename should match with the node name.
3. If you get 'permission denied', there's a chance your group isn't verified correctly. Change your group to ps-ipmi with:
```
newgrpu ps-ipmi
```
  
4. Choose remote control tab, and click power cycle
### Using CLIs 
```
ssh psdev
/reg/common/tools/bin/psipmi node-name power status   # check status
/reg/common/tools/bin/psipmi node-name power reset.   # reset cpu
```
