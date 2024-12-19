# Setup DHCP Server on drp-neh-cmp011
The ctrl port on TDC box requires DHCP. We setup a dhcp server on cmp011 so that it can receive an IP address from it.  
All below are sudo required.  
## Install dhcp package and setup the configuration for rhel7
1. Install required packages
```
yum install -y dhcp*
```
2. Copy the example configuration file
```
cp /usr/share/doc/dhcp-4.2.5/dhcpd.conf.example /etc/dhcp/dhcpd.conf
```
Change this section to:
```
# A slightly different configuration for an internal subnet.
subnet 192.168.0.0 netmask 255.255.255.0 {
  range 192.168.0.100 192.168.0.150;
  # option domain-name-servers ns1.internal.example.org;
  # option domain-name "internal.example.org";
  # option routers 10.5.5.1;
  # option broadcast-address 10.5.5.31;
  default-lease-time 600;
  max-lease-time 7200;
}
```
3. Start the service *Note that prior to start the dhcpd, I had to ifdown and ifup eno2 for this to work. 
```
systemctl start dhcpd
```
(Optional) Keep the service on at restart of the node:
```
systemctl enable dhcpd
```
To check the status of service:
```
systemctl status dhcpd
```
or check the logfile of the service:
```
journalctl -u dhcpd.service
```
4. Check that the tdc box got the IP
```
root@drp-neh-cmp011 monarin cat /var/lib/dhcpd/dhcpd.leases
# The format of this file is documented in the dhcpd.leases(5) manual page.
# This lease file was written by isc-dhcp-4.2.5

server-duid "\000\001\000\001.\366#\346\254\037kW0w";

lease 192.168.0.150 {
  starts 4 2024/12/19 17:58:01;
  ends 4 2024/12/19 18:08:01;
  cltt 4 2024/12/19 17:58:01;
  binding state active;
  next binding state free;
  rewind binding state free;
  hardware ethernet 86:19:df:9e:a6:07;
  uid "\001\206\031\337\236\246\007";
  client-hostname "sc_ml_xvc_24";
}
```
5. Try pinging the IP


