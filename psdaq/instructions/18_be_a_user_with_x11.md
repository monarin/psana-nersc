First, check xauth and DISPLAY settings on the user that has x11-forwarding.
```
$ xauth list $DISPLAY
<output1>
$ echo $DISPLAY
<outoput2>
```
Then switch to another user
```
sudo su user2
```
And set the xauth and display as found from the first user:
```
$ xauth add <output1> 
$ export DISPLAY=<output2>
```
