Run the following command on drp-neh-ctl002
```
clush -w drp-srcf-cmp0[01-26] "grep 'Build String' /proc/datadev_1" | grep "Build String : DrpTDet"
```
## On srcf
(Last update: 01/26/2024)
```
clush -w drp-srcf-cmp0[01-26] "grep 'Build String' /proc/datadev_1" | grep "Build String : DrpTDet"
drp-srcf-cmp028:          Build String : DrpTDet: Vivado v2022.1, rdsrv301 (Ubuntu 20.04.6 LTS), Built Mon 29 Jan 2024 01:44:56 PM PST by weaver
drp-srcf-cmp002:          Build String : DrpTDet: Vivado v2022.1, rdsrv301 (Ubuntu 20.04.6 LTS), Built Thu 20 Jul 2023 12:37:07 PM PDT by weaver
drp-srcf-cmp001:          Build String : DrpTDet: Vivado v2022.1, rdsrv301 (Ubuntu 20.04.5 LTS), Built Tue 07 Feb 2023 03:58:51 PM PST by weaver
drp-srcf-cmp015:          Build String : DrpTDet: Vivado v2022.1, rdsrv300 (Ubuntu 20.04.1 LTS), Built Wed 10 Aug 2022 04:04:10 PM PDT by weaver
drp-srcf-cmp016:          Build String : DrpTDet: Vivado v2022.1, rdsrv301 (Ubuntu 20.04.5 LTS), Built Tue 07 Feb 2023 03:58:51 PM PST by weaver
drp-srcf-cmp003:          Build String : DrpTDet: Vivado v2022.1, rdsrv301 (Ubuntu 20.04.5 LTS), Built Tue 07 Feb 2023 03:58:51 PM PST by weaver
drp-srcf-cmp008:          Build String : DrpTDet: Vivado v2022.1, rdsrv301 (Ubuntu 20.04.5 LTS), Built Tue 07 Feb 2023 03:58:51 PM PST by weaver
drp-srcf-cmp025:          Build String : DrpTDet: Vivado v2022.1, rdsrv301 (Ubuntu 20.04.6 LTS), Built Thu 20 Jul 2023 12:37:07 PM PDT by weaver
drp-srcf-cmp010:          Build String : DrpTDet: Vivado v2022.1, rdsrv301 (Ubuntu 20.04.5 LTS), Built Tue 07 Feb 2023 03:58:51 PM PST by weaver
drp-srcf-cmp029:          Build String : DrpTDet: Vivado v2022.1, rdsrv301 (Ubuntu 20.04.5 LTS), Built Tue 07 Feb 2023 03:58:51 PM PST by weaver
```
## At the FEE teststand
(Last update: 01/26/2024)
```
monarin@drp-neh-ctl002 ~ clush -w drp-neh-cmp0[01-15] "grep 'Build String' /proc/datadev_1" | grep "Build String : DrpTDet"
drp-neh-cmp001:          Build String : DrpTDet: Vivado v2022.1, rdsrv300 (Ubuntu 20.04.1 LTS), Built Wed 10 Aug 2022 04:04:10 PM PDT by weaver
drp-neh-cmp015:          Build String : DrpTDet: Vivado v2022.1, rdsrv300 (Ubuntu 20.04.1 LTS), Built Wed 10 Aug 2022 04:04:10 PM PDT by weaver
drp-neh-cmp002:          Build String : DrpTDet: Vivado v2022.1, rdsrv300 (Ubuntu 20.04.1 LTS), Built Wed 10 Aug 2022 04:04:10 PM PDT by weaver
drp-neh-cmp010:          Build String : DrpTDet: Vivado v2022.1, rdsrv300 (Ubuntu 20.04.1 LTS), Built Wed 10 Aug 2022 04:04:10 PM PDT by weaver
```
