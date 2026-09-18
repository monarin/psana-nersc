# Handling Firmware vs Calibration GitHash Mismatch (epix-quad-1kfps)

## Symptom

When running `epixQuadDAQ.py` after flashing new firmware, you may see an error like:

```
AxiVersion.GitHash = 0x49e17b8845b3dbfa5927bb368533ceb4e6b58e70 != Calibration Githash = 0xffffffffffffffffffffffffffffffffffffffff
Please re-train the ADC lanes with promWrEn enabled (--adcCalib 1 arg and running AdcTrain() Command)
```

This indicates that the **firmware GitHash** does not match the **stored calibration GitHash** in the PROM.  
This is expected the first time after flashing a new FPGA image.

---

## Fix Procedure

1. **Run the DAQ script with calibration mode enabled** from a writable folder (e.g. `~/tmp/epix10ka_1khz`).  
   This is required because the training will generate a file `ePixQuadAdcTrainingData.txt` in the current working directory.

   ```bash
   mkdir -p ~/tmp/epix10ka_1khz
   cd ~/tmp/epix10ka_1khz

   python /cds/sw/ds/ana/conda2/rel/lcls2_submodules_09252025_1kfps/epix-quad/software/scripts/epixQuadDAQ.py --l 0 --adcCalib 1
   ```

   > The `--adcCalib 1` flag sets `promWrEn` to true, enabling ADC training constants to be written into PROM.

2. In the GUI that launches (or using command line), click **AdcTrain**.

   - Watch the console for training messages.
   - This process writes new calibration data (including the GitHash) into PROM.

3. **Reboot the FPGA** to reload firmware and calibration:

   - Power cycle the board **OR**
   - Use the helper script:

     ```bash
     python /cds/sw/ds/ana/conda2/rel/lcls2_submodules_09252025_1kfps/epix-quad/software/scripts/epixQuadRebootFPGA.py --l 0
     ```

4. Restart `epixQuadDAQ.py` (without `--adcCalib`) to confirm normal operation:

   ```bash
   python /cds/sw/ds/ana/conda2/rel/lcls2_submodules_09252025_1kfps/epix-quad/software/scripts/epixQuadDAQ.py --l 0
   ```

---

## Notes

- You only need to re-train after **flashing new firmware**.  
- The mismatch error will **block DAQ startup** until training is performed.  
- The GitHash check ensures that calibration data is tied to the exact firmware revision.

---

## Example Workflow

```bash
# First run after firmware flash (expect mismatch error):
python /cds/sw/ds/ana/conda2/rel/lcls2_submodules_09252025_1kfps/epix-quad/software/scripts/epixQuadDAQ.py --l 0

# Fix (from writable folder):
mkdir -p ~/tmp/epix10ka_1khz
cd ~/tmp/epix10ka_1khz
python /cds/sw/ds/ana/conda2/rel/lcls2_submodules_09252025_1kfps/epix-quad/software/scripts/epixQuadDAQ.py --l 0 --adcCalib 1
# → Click AdcTrain in GUI
# → Wait for training to complete

python /cds/sw/ds/ana/conda2/rel/lcls2_submodules_09252025_1kfps/epix-quad/software/scripts/epixQuadRebootFPGA.py --l 0

# Verify:
python /cds/sw/ds/ana/conda2/rel/lcls2_submodules_09252025_1kfps/epix-quad/software/scripts/epixQuadDAQ.py --l 0
# → Should start without mismatch error
```
