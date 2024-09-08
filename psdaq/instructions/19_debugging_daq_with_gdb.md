## Use gdb to attach to a running process
Logon to the node with running drp or teb process. 
1. Source setup_env.sh (to get to drp/teb cmds). You need to be root to attach to another user's process.
```
sudo su
```
2. Find the running process id
```
ps -C drp -o pid h
```
3. If more then one pids (>1 detector running), check the cmd.
```
ps -p <pid here> -o pid,vsz=MEMORY -o user,group=GROUP -o comm,args=ARGS | cat
```
4. With the pid, attach gdb
```
gdb drp -p 43944
```
5. Use continue, ctrl-c, and backtrace 
