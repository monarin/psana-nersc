The output/data port on the tdc is connected to another node (data node, currently drp-neh-cmp012). We need to set the static IP on this node in order to receive data from the tdc box.
## Setting static IP 
On drp-neh-cmp012, eno2 is the interface that connects to the tdc data port. Set its IP and netmask to the following values specifically:
```
monarin@drp-neh-cmp012 ~ sudo ifconfig eno2 10.0.0.1
monarin@drp-neh-cmp012 ~ sudo ifconfig eno2 netmask 255.255.255.0
```
You should be able to talk to the tdc (10.0.0.20)
```
monarin@drp-neh-cmp012 ~ ping 10.0.0.20
PING 10.0.0.20 (10.0.0.20) 56(84) bytes of data.
64 bytes from 10.0.0.20: icmp_seq=1 ttl=64 time=0.175 ms
64 bytes from 10.0.0.20: icmp_seq=2 ttl=64 time=0.060 ms
64 bytes from 10.0.0.20: icmp_seq=3 ttl=64 time=0.058 ms
```
