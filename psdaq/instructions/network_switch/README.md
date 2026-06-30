# ATCA Network Switch Troubleshooting

This note summarizes the June 2026 XPM/network debugging around
`drp-srcf-mon001`, `swh-neh-daq01`, and `swh-xpp-daq01`.

The production DAQ network may be active while these checks are run. Use the
commands here as read-only diagnostics. Do not change port modes, clear/reset
switches, restart DAQ services, run loopback/PRBS tests, or flood ping while
experiments are running unless operations explicitly approves it.

## Access

The VadaTech switches are not generally reachable directly from a normal shell.
The working access path used for this investigation was:

```bash
ssh psbuild-rocky9-01
ssh <psbuild-rhel7-host>
ssh root@swh-neh-daq01.pcdsn
ssh root@swh-xpp-daq01.pcdsn
```

Some switch images only offer the old `ssh-rsa` host key type. If SSH refuses
with `no matching host key type found. Their offer: ssh-rsa`, use:

```bash
ssh -oHostKeyAlgorithms=+ssh-rsa root@swh-neh-daq01.pcdsn
```

If needed for an older client/server combination:

```bash
ssh -oHostKeyAlgorithms=+ssh-rsa -oPubkeyAcceptedAlgorithms=+ssh-rsa root@swh-neh-daq01.pcdsn
```

Known switch names from this investigation:

```text
swh-neh-daq01.pcdsn  Room 208 / NEH switch
swh-xpp-daq01        XPP ATCA switch
```

The switch clocks may be wrong. During this investigation, `swh-neh-daq01`
reported a 1970 date, so use the operator terminal time for correlations unless
NTP/time has been corrected.

## Port Naming

The switch commands report internal switch port numbers and board-specific
logical names.

For the ATC807-style mapping seen here:

```text
port 20 -> SFP+0
port 0  -> SFP+1
port 21 -> SFP+2
port 1  -> SFP+3
port 22 -> SFP+4
port 2  -> SFP+5
port 23 -> SFP+6
port 3  -> SFP+7
port 6  -> FABRIC1
```

Common labels:

```text
SFP+    Front-panel pluggable port.
FABRIC  Backplane fabric link to an ATCA/AMC module.
RTM     Rear Transition Module path.
UPDATE  Switch/MCH update/redundancy channel.
SWTOSW  Internal switch-to-switch path on the blade.
MANAGE  Management CPU path used for SSH/control/register access.
```

`XAUI` is a 10G electrical interface using four lanes, common for internal
fabric/backplane links. It is not an external SFP+ optical/copper port, but it
can carry 10G Ethernet traffic.

## Current Topology Findings

MAC table observations showed:

```text
drp-srcf-mon001 eno2d1 MAC: 3C:EC:EF:42:1F:F5
FEH XPM 4 MAC:              08:00:56:00:54:16
```

On `swh-neh-daq01`:

```text
3C:EC:EF:42:1F:F5 -> 0x00100000 -> port 20 / SFP+0  -> drp-srcf-mon001
08:00:56:00:54:16 -> 0x00000002 -> port 1  / SFP+3  -> FEH XPM 4 path
00:13:3A:0D:31:*  -> 0x00000008 -> port 3  / SFP+7  -> XPP/uplink branch
```

On `swh-xpp-daq01`:

```text
3C:EC:EF:42:1F:F5 -> 0x00100000 -> port 20 / SFP+0
08:00:56:00:54:16 -> 0x00000040 -> port 6  / FABRIC1
```

The inferred inter-switch link is:

```text
swh-neh-daq01 port 3  / SFP+7
    <->
swh-xpp-daq01 port 20 / SFP+0
```

The `pyxpm-feh-4` process runs on `drp-srcf-mon001` and talks to XPM IP
`10.0.8.102`. Based on current MAC learning, the direct path from `mon001` to
FEH XPM 4 is NEH-local:

```text
drp-srcf-mon001
  -> swh-neh-daq01 port 20 / SFP+0
  -> swh-neh-daq01 port 1  / SFP+3
  -> FEH XPM 4
```

The bad NEH-XPP inter-switch link does not appear to be the direct L2 path for
`pyxpm-feh-4` register reads based on current MAC learning. It may still affect
other traffic, flooding, or other XPMs.

## Main Findings

### mon001

`drp-srcf-mon001:eno2d1` shows persistent receive-side FCS/stat errors:

```text
rx_fcs_err_frames: increasing
rx_stat_err:       increasing
rx_align_err:      0
rx_mtu_err:        0
rx_pcs_symbol_err: 0
tx_fcs_err_frames: 0
tx_err:            0
```

The interface is configured for jumbo MTU and 10G full-duplex:

```text
eno2d1 mtu 9000
Speed: 10000Mb/s
Duplex: Full
Port: Twisted Pair
Auto-negotiation: on
driver: bnxt_en
```

The absence of MTU/frame-length counters points away from jumbo/MTU mismatch as
the primary symptom. The increasing counters are receive FCS/stat counters,
which are more consistent with corrupted frames or NIC/PHY receive-side
accounting.

`dmesg` showed historical `eno2d1` link flaps on June 2, 2026:

```text
2026-06-02 10:04:50 eno2d1 link Down/Up
2026-06-02 10:09:47 eno2d1 link Down/Up
2026-06-02 10:12:53 eno2d1 link Down/Up
2026-06-02 10:12:55 eno2d1 link Down/Up
```

### swh-neh-daq01

Port mode checks:

```text
port 20 / SFP+0  mon001       10G
port 3  / SFP+7  XPP uplink   10G
port 1  / SFP+3  XPM path     10G
```

`swh-neh-daq01` port 20, the direct `mon001` port, did not show switch-side FCS
errors during interval checks:

```text
(SFP+ 0) Port 20 RX FCS: 0 | TX FCS: 0
```

`swh-neh-daq01` port 3, the inter-switch/uplink branch, did show RX FCS and
code errors:

```text
(SFP+ 7) Port 3 RX FCS:  increasing
(SFP+ 7) Port 3 RX code: increasing
```

### swh-xpp-daq01

Port mode checks:

```text
port 20 / SFP+0   NEH uplink       10G
port 6  / FABRIC1 FEH XPM 4 path   XAUI
```

`swh-xpp-daq01` port 20, the other side of the inter-switch link, showed RX FCS
and code errors:

```text
(SFP+ 0) Port 20 RX FCS:  increasing
(SFP+ 0) Port 20 RX code: increasing
```

The XPM-facing fabric path was clean in the sampled checks:

```text
(FABRIC 1) Port 6 LINK/ALIGN/SYNC0-3
(FABRIC 1) Port 6 RX FCS: 0
(FABRIC 1) Port 6 RX code: 0
```

### pyxpm

The active `pyxpm-feh-4` job was:

```text
JobName: pyxpm-feh-4
JobID:   999517
Host:    drp-srcf-mon001
XPM IP:  10.0.8.102
PV:      DAQ:FEH:XPM:4
```

Its log showed repeated PyRogue/Rogue register transaction timeouts:

```text
AMCc.XPM.UsTiming.block
Timeout waiting for register transaction ... message response
Caught exception... retrying.
```

`pyxpm-feh-4` had not restarted during the check. Slurm showed `Restarts=0`.

Other `pyxpm` jobs showed similar timeout bursts. The most relevant current
pattern was synchronized bursts on `pyxpm-feh-4` and `pyxpm-feh-5`, both on
`drp-srcf-mon001`, for example around:

```text
2026-06-16 13:29
2026-06-16 14:33
2026-06-16 15:13-15:14
```

This suggests a shared host/network/polling-path issue, not only an isolated
FEH XPM 4 board issue.

## Current Conclusions

There are at least two network-health observations:

1. The NEH-XPP inter-switch link is confirmed bad or marginal.

   Both ends saw receive-side FCS/code errors:

   ```text
   swh-neh-daq01 port 3  / SFP+7
   swh-xpp-daq01 port 20 / SFP+0
   ```

2. `drp-srcf-mon001:eno2d1` has persistent RX FCS/stat errors.

   However, `swh-neh-daq01` port 20, the switch port to `mon001`, did not show
   TX FCS errors during interval checks. This does not prove corrupted
   inter-switch frames are being forwarded to `mon001` with bad FCS. It may be
   a separate physical/NIC receive-side issue or a switch/NIC counter visibility
   difference.

For `pyxpm-feh-4`, current MAC learning says the direct path from `mon001` to
FEH XPM 4 is through `swh-neh-daq01` port 20 to port 1, not through the bad
NEH-XPP inter-switch link. The inter-switch link remains actionable because it
is clearly accumulating physical errors and may affect other XPM/DAQ paths.

## Commands

### Host NIC Checks on mon001

Show link, MTU, and MAC:

```bash
ssh drp-srcf-mon001 /sbin/ip link show eno2d1
```

Show speed/duplex/autoneg:

```bash
ssh drp-srcf-mon001 /usr/sbin/ethtool eno2d1
```

Show driver/firmware:

```bash
ssh drp-srcf-mon001 /usr/sbin/ethtool -i eno2d1
```

Show relevant counters:

```bash
ssh drp-srcf-mon001 "/usr/sbin/ethtool -S eno2d1 | egrep 'rx_fcs_err_frames|rx_stat_err|rx_align_err_frames|rx_mtu_err_frames|rx_pcs_symbol_err|rx_corrected_bits|rx_discards|rx_drops|rx_total_discard_pkts|link_down_events|tx_fcs_err_frames|tx_err'"
```

Show EEE status:

```bash
ssh drp-srcf-mon001 /usr/sbin/ethtool --show-eee eno2d1
```

Show kernel link history:

```bash
ssh drp-srcf-mon001 "dmesg -T | egrep -i 'eno2d1|bnxt|link|firmware|error|fcs'"
```

Show historical interface errors from `sar`:

```bash
ssh drp-srcf-mon001 "sar -n EDEV -f /var/log/sa/saDD -s HH:MM:SS -e HH:MM:SS | egrep 'IFACE|eno2d1'"
```

`sar -n EDEV` uses the sysstat file named by `-f`, so `sa05` means the fifth day
of the current retained month, not an arbitrary date.

### Switch Link and Mode Checks

Show link state:

```bash
axel_linkstat
```

Show physical layer detail for all ports or a specific port:

```bash
axel_l1stat all
axel_l1stat 20
axel_l1stat 3
axel_l1stat 1
```

Show port mode:

```bash
axel_portmode 20
axel_portmode 3
axel_portmode 1
axel_portmode 6
```

Avoid speed-setting commands while operations are active:

```text
axel_sfp_port <port> 10g
axel_sfp_port <port> 1g
axel_sfp_port <port> auto
axel_10g_port <port>
axel_1g_port <port>
axel_xaui_port <port>
```

### Switch Error Counters

Important: `axel_stats <counter>` clears that selected counter group on read.
The first read is the accumulated value since the previous read/boot; the next
read is the interval delta.

FCS errors:

```bash
axel_stats fcs
```

Code errors:

```bash
axel_stats cde
```

Frame-length errors, useful for MTU/jumbo suspicion:

```bash
axel_stats flr
```

Alignment errors:

```bash
axel_stats aln
```

Packet drops:

```bash
axel_stats drp
```

Packet counts:

```bash
axel_stats pkt
```

Typical focused checks:

```bash
# On swh-neh-daq01
axel_stats fcs | grep -E 'SFP\+ 0|SFP\+ 7|SFP\+ 3|Port 20|Port  3|Port  1'
axel_stats cde | grep -E 'SFP\+ 0|SFP\+ 7|SFP\+ 3|Port 20|Port  3|Port  1'
axel_stats flr | grep -E 'SFP\+ 0|SFP\+ 7|SFP\+ 3|Port 20|Port  3|Port  1'
axel_stats aln | grep -E 'SFP\+ 0|SFP\+ 7|SFP\+ 3|Port 20|Port  3|Port  1'

# On swh-xpp-daq01
axel_stats fcs | grep -E 'SFP\+ 0|FABRIC 1|Port 20|Port  6'
axel_stats cde | grep -E 'SFP\+ 0|FABRIC 1|Port 20|Port  6'
```

### Paired 60-Second Counter Snapshot

Use this style to correlate host and switch counters. Run each query, wait about
60 seconds, and repeat. Subtract host cumulative counters; switch `axel_stats`
second reads are already interval deltas.

```bash
# mon001
ethtool -S eno2d1 | egrep 'rx_fcs_err_frames|rx_stat_err'

# swh-neh-daq01
axel_stats fcs | grep -E 'SFP\+ 0|SFP\+ 7|Port 20|Port  3'

# swh-xpp-daq01
axel_stats fcs | grep -E 'SFP\+ 0|Port 20'
```

Example interpretation from this investigation:

```text
mon001 rx_fcs/rx_stat increased by about 50-60 per minute.
swh-neh-daq01 port 20 stayed at RX/TX FCS 0.
swh-neh-daq01 port 3 showed RX FCS increments.
swh-xpp-daq01 port 20 showed RX FCS increments.
```

### MAC Table and IP/MAC Lookup

Show learned MAC addresses on a switch:

```bash
axel_reg macshow
```

Find a specific MAC:

```bash
axel_reg macshow | grep -i '3C:EC:EF:42:1F:F5'
axel_reg macshow | grep -i '08:00:56:00:54:16'
```

Find all MACs learned on selected port vectors:

```bash
# swh-neh-daq01: port 1, port 3, port 20
axel_reg macshow | grep -E '0x00000002|0x00000008|0x00100000'

# swh-xpp-daq01: port 6, port 20
axel_reg macshow | grep -E '0x00000040|0x00100000'
```

Port vector decoding:

```text
0x00000001 -> port 0
0x00000002 -> port 1
0x00000004 -> port 2
0x00000008 -> port 3
0x00000010 -> port 4
0x00000020 -> port 5
0x00000040 -> port 6
0x00100000 -> port 20
```

On `mon001`, map IP addresses to MAC addresses using the neighbor cache:

```bash
ip neigh
arp -an
```

Specific passive lookup examples:

```bash
ip neigh show 10.0.8.102
arp -an | grep 10.0.8.102
```

During this investigation:

```text
10.0.8.102 -> 08:00:56:00:54:16  FEH XPM 4
10.0.3.103 -> 08:00:56:00:4F:D8
10.0.3.105 -> 08:00:56:00:4F:98
10.0.3.1   -> AC:1F:6B:A1:B5:D9
```

### pyxpm Checks

List running `pyxpm` jobs:

```bash
ssh drp-srcf-mon001 "squeue -h -u tmoopr -o '%i|%j|%T|%M|%R' | grep pyxpm | sort -t'|' -k2,2"
```

Find the `pyxpm-feh-4` process:

```bash
ssh drp-srcf-mon001 "pgrep -af 'pyxpm.*10.0.8.102|pyxpm.*DAQ:FEH:XPM:4'"
```

Get Slurm job details and the stdout/stderr log path:

```bash
ssh drp-srcf-mon001 "scontrol show job <jobid>"
```

Check for timeout errors in a log:

```bash
grep -nE 'Timeout waiting for register transaction|Caught exception|Traceback|ERROR|Error' <pyxpm-log>
```

Count timestamped register timeouts:

```bash
grep -c 'ERROR:pyrogue.*Timeout waiting for register transaction' <pyxpm-log>
```

Group timeout counts by minute:

```bash
awk '/ERROR:pyrogue.*Timeout waiting for register transaction/ {k=substr($1 " " $2,1,16); c[k]++} END {for (k in c) print k, c[k]}' <pyxpm-log> | sort
```

For `pyxpm-feh-4`, the log path found from Slurm was:

```text
/cds/home/opr/tmoopr/2026/06/09_13:06:44_drp-srcf-mon001:pyxpm-feh-4.log
```

## Reporting Checklist

When sending this to IT or DAQ experts, include:

```text
1. Host NIC counters from mon001, with two timestamps and deltas.
2. Switch `axel_stats fcs` and `cde` on:
   - swh-neh-daq01 port 20 / SFP+0
   - swh-neh-daq01 port 3  / SFP+7
   - swh-xpp-daq01 port 20 / SFP+0
   - swh-xpp-daq01 port 6  / FABRIC1
3. `axel_portmode` output for the same ports.
4. MAC table lines proving which devices are learned on each port.
5. pyxpm timeout log timestamps and whether Slurm `Restarts` is nonzero.
```

Lead with the confirmed physical link issue:

```text
swh-neh-daq01 SFP+7/port 3 <-> swh-xpp-daq01 SFP+0/port 20
shows RX FCS/code errors on both ends while both ports are 10G.
```

Then separately mention:

```text
drp-srcf-mon001 eno2d1 RX FCS/stat counters are increasing, but
swh-neh-daq01 port 20 switch-side TX/RX FCS counters stayed at zero in sampled
intervals.
```
