# AutoFSC-RELION-Postprocessing-Made-Easy
Automatically extract and visualize Fourier Shell Correlation (FSC) data from RELION postprocessing files. Generate publication-ready plots and CSVs with interpolated resolutions at FSC=0.143 and 0.5 for rapid Cryo-EM map assessment.

# RELION Auto-Extract FSC

Automatically extract and visualize Fourier Shell Correlation (FSC) data from RELION postprocessing files. Generate publication-ready plots and CSVs with interpolated resolutions at FSC=0.143 and 0.5 for rapid Cryo-EM map assessment.

---

## Features

- **CSV Output**
  - Contains all FSC data in numeric format.
  - Stores FSC=0.143 and FSC=0.5 resolution values in the CSV header.

- **Plots Generated**
  1. **Main FSC Plot** (`FSC_main_plot.png`)  
     - Shows unmasked, masked, and corrected FSC curves.  
     - Vertical lines indicate interpolated FSC=0.143 and FSC=0.5 resolutions.  
     - Horizontal lines at FSC thresholds.
     
  2. **Main FSC Without Vertical Lines** (`FSC_main_no_lines.png`)  
     - Same as above but without interpolation vertical lines.  
     - Useful for cleaner visualization.
     
  3. **GSFSC FSC=0.5 Plot** (`FSC_0.5_plot.png`)  
     - Focused plot highlighting FSC=0.5 resolution.  
     - Horizontal line at FSC=0.5.  
     - Title includes interpolated resolution value.
     
  4. **GSFSC FSC=0.143 Plot** (`FSC_0.143_plot.png`)  
     - Focused plot highlighting FSC=0.143 resolution.  
     - Horizontal line at FSC=0.143.  
     - Title includes interpolated resolution value.
     
  5. **Combined 3-Panel Figure** (`FSC_combined.png`)  
     - Panels: Main FSC, GSFSC FSC=0.5, GSFSC FSC=0.143.  
     - All plots share consistent x-axis (log scale, inverted), y-axis, and tick formatting.  
     - Interpolated resolutions indicated in titles and/or vertical lines.

---

## Example Workflow

```bash
python RELION-AutoFSC.py
```


**Input**: postprocess.star file from RELION postprocessing job.

**Output**: CSV and multiple PNG plots (as above).

Horizontal lines highlight FSC thresholds; vertical lines mark interpolated resolutions.


---

## Dependencies

- **Python 3.7+**
- **Pandas**
- **Matplotlib**

```bash
pip install pandas matplotlib


---

## Notes

- If applying to Cryo-EM datasets you may need to alter the x-axis values for FSC_0.5_plot.png and FSC_0.143_plot.png as the default example is from a negative stain electron microscopy dataset (low-resolution). To alter the x-axis change the x_max = 100 variable to the desired lowest resolution value and then change the tick_positions = [100, 80, 60, 40, 20, 10, 8, 6, 4, 2]. The highest resolution frequency is automatically detected so does not require changing.

- Uses a **logarithmic x-axis** for clarity.
- X-axis is inverted to match standard EM plot conventions (high resolution on right).
- Custom tick positions are used for consistent visual appearance.
- The CSV output contains numeric data only (no empty lines between points).
- Vertical lines indicate interpolated FSC=0.143 and FSC=0.5 resolutions (except in plots designed to omit them).
