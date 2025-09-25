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

1. Run the DAQ script with calibration mode enabled:

   ```bash
   cd epix-quad/software
   python scripts/epixQuadDAQ.py --l 0 --adcCalib 1
   ```

   > The `--adcCalib 1` flag sets `promWrEn` to true, enabling ADC training constants to be written into PROM.

2. In the GUI that launches (or using command line), click **AdcTrain**.

   - Watch the console for training messages.
   - This process writes new calibration data (including the GitHash) into PROM.

3. **Reboot the FPGA** to reload firmware and calibration:

   - Power cycle the board **OR**
   - Use the helper script:

     ```bash
     python scripts/epixQuadRebootFPGA.py --l 0
     ```

4. Restart `epixQuadDAQ.py` (without `--adcCalib`) to confirm normal operation.

---

## Notes

- You only need to re-train after **flashing new firmware**.  
- The mismatch error will **block DAQ startup** until training is performed.  
- The GitHash check ensures that calibration data is tied to the exact firmware revision.

---

## Example Workflow

```bash
# First run after firmware flash (expect mismatch error):
python scripts/epixQuadDAQ.py --l 0

# Fix:
python scripts/epixQuadDAQ.py --l 0 --adcCalib 1
# → Click AdcTrain in GUI
# → Wait for training to complete
python scripts/epixQuadRebootFPGA.py --l 0

# Verify:
python scripts/epixQuadDAQ.py --l 0
# → Should start without mismatch error
```
