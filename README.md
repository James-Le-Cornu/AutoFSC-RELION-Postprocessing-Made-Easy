# AutoFSC
**RELION Postprocessing Made Easy**

Automatically extract and visualize Fourier Shell Correlation (FSC) data from RELION postprocessing files. Generate publication-ready plots and CSVs with interpolated resolutions at FSC=0.143 and 0.5 for rapid Cryo-EM map assessment.

---

## Features

- **CSV Output**
  - Contains all FSC data in numeric format.
  - Stores FSC=0.143 and FSC=0.5 resolution values in the CSV header.

- **Plots Generated**
  1. **Main FSC Plot - for interpretation** (`FSC_main_plot.png`)  
     - Shows unmasked, masked, and corrected FSC curves.  
     - Vertical lines indicate interpolated FSC=0.143 and FSC=0.5 resolutions.  
     - Horizontal lines at FSC thresholds.
     
  2. **Main FSC Without Vertical Lines - potentially for publication figure** (`FSC_main_no_lines.png`)  
     - Same as above but without interpolation vertical lines.  
     - Useful for cleaner visualization.
     
  3. **GSFSC FSC=0.5 Plot - potentially for publication figure** (`FSC_0.5_plot.png`)  
     - Focused plot highlighting FSC=0.5 resolution.  
     - Horizontal line at FSC=0.5.  
     - Title includes interpolated resolution value.
     
  4. **GSFSC FSC=0.143 Plot - potentially for publication figure** (`FSC_0.143_plot.png`)  
     - Focused plot highlighting FSC=0.143 resolution.  
     - Horizontal line at FSC=0.143.  
     - Title includes interpolated resolution value.
     
  5. **Combined 3-Panel Figure - for interpretation** (`FSC_combined.png`)  
     - Panels: Main FSC, GSFSC FSC=0.5, GSFSC FSC=0.143.  
     - All plots share consistent x-axis (log scale, inverted), y-axis, and tick formatting.  
     - Interpolated resolutions indicated in titles and/or vertical lines.

---

## Example Workflow

Launch AutoFSC from the PostProcess directory or alter the `input_file variable`, by default postprocess.star, to a complete filepath.

```bash
python RELION-AutoFSC.py
```


**Input**: postprocess.star file from RELION postprocessing job.

**Output**: CSV and multiple PNG plots (as above).

Horizontal lines highlight FSC thresholds; vertical lines mark interpolated resolutions.

**Example output:**
  1. **Main FSC Plot - for interpretation** (`FSC_main_plot.png`)  
    <img width="1800" height="1200" alt="FSC_main_plot" src="https://github.com/user-attachments/assets/fb1f1cf5-cc86-4b1a-95c2-91f7f8bb505b" />
     
  2. **Main FSC Without Vertical Lines - potentially for publication figure** (`FSC_main_no_lines.png`)  
   <img width="1800" height="1200" alt="FSC_main_no_lines" src="https://github.com/user-attachments/assets/196fc97c-f8b4-4527-a9a9-683ba27f06de" />
     
  3. **GSFSC FSC=0.5 Plot - potentially for publication figure** (`FSC_0.5_plot.png`)  
    <img width="1800" height="1200" alt="FSC_0 5_plot" src="https://github.com/user-attachments/assets/6ac42bc1-3a7d-4f5c-a7bd-e472ba0274b8" />
     
  4. **GSFSC FSC=0.143 Plot - potentially for publication figure** (`FSC_0.143_plot.png`)  
   <img width="1800" height="1200" alt="FSC_0 143_plot" src="https://github.com/user-attachments/assets/f1c500ca-d613-4502-9557-7fe50209d80d" />

  5. **Combined 3-Panel Figure - for interpretation** (`FSC_combined.png`)  
   <img width="5400" height="1200" alt="FSC_combined" src="https://github.com/user-attachments/assets/d76b6bc7-b526-4290-ae48-8ceef007e334" />



---

## Dependencies

- **Python 3.7+**
- **Pandas**
- **Matplotlib**

After installing python install the packages using:

```bash
pip install pandas matplotlib
```

---

## Notes

- **If applying to Cryo-EM datasets** you may need to alter the x-axis values for `FSC_0.5_plot.png` and `FSC_0.143_plot.png` as the default example is from a **negative stain electron microscopy** dataset (low-resolution). To alter the x-axis change the `x_max = 100` variable to the desired lowest resolution value and then change the `tick_positions = [100, 80, 60, 40, 20, 10, 8, 6, 4, 2]`. The highest resolution frequency is automatically detected so does not require changing.
- Uses a **logarithmic x-axis** for clarity.
- X-axis is inverted to match standard EM plot conventions (high resolution on right).
- Custom tick positions are used for consistent visual appearance.
- The CSV output contains numeric data only (no empty lines between points).
- Vertical lines indicate interpolated FSC=0.143 and FSC=0.5 resolutions (except in plots designed to omit them).
