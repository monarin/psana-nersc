## Adding new wave8 to TXI and make it avaiable through already commissioning cmp004 node 
### Wave8 installation 
Wave8 takes xpm input and together with its data produce one data output.  
[ data (out) | unused | xpm (in) | unused ].  
For TXI, xpm is taken from 208 via fiber patch (mirror between txi and 208 top patch). Data is wired back with the same fiber patch to 208. 
We then connect fiber patch data port to the BOS port 1.7.4 and label it as TXI_FIM. This is then cross-linked using the BOS webgui so TXI
wave 8 is connected to cmp004_QSFP1_1.

We can check the optic signal on the BOS. 
![ins05_BOS_TXI_Wave8](/psdaq/images/ins05_BOS_TXI_Wave8.png)
## Checing the optic signal and linklock using gui
Wave8 guis require 


