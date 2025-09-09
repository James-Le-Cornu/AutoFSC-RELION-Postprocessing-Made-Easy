# AutoFSC-RELION-Postprocessing-Made-Easy
Automatically extract and visualize Fourier Shell Correlation (FSC) data from RELION postprocessing files. Generate publication-ready plots and CSVs with interpolated resolutions at FSC=0.143 and 0.5 for rapid Cryo-EM map assessment.

This Python script extracts Fourier Shell Correlation (FSC) data from a RELION postprocess.star file, calculates interpolated resolutions at FSC thresholds (0.143 and 0.5), outputs a CSV, and generates publication-quality plots.

Features

CSV Output

Contains all FSC data with numeric formatting.

FSC=0.143 and FSC=0.5 resolution values are stored in the CSV header.

Plots Generated

Main FSC Plot (FSC_main_plot.png)

Shows unmasked, masked, and corrected FSC curves.

Vertical lines indicate interpolated FSC=0.143 and FSC=0.5 resolutions.

Horizontal lines at FSC thresholds.

Main FSC Without Vertical Lines (FSC_main_no_lines.png)

Same as above but without interpolation vertical lines.

Useful for visual clarity in presentations.

GSFSC FSC=0.5 Plot (FSC_0.5_plot.png)

Focused plot highlighting FSC=0.5 resolution.

Horizontal line at FSC=0.5.

Title includes interpolated resolution value.

GSFSC FSC=0.143 Plot (FSC_0.143_plot.png)

Focused plot highlighting FSC=0.143 resolution.

Horizontal line at FSC=0.143.

Title includes interpolated resolution value.

Combined 3-Panel Figure (FSC_combined.png)

Panels: Main FSC, GSFSC FSC=0.5, GSFSC FSC=0.143.

All plots share consistent x-axis (log scale, inverted), y-axis, and tick formatting.

Interpolated resolutions indicated in titles and/or vertical lines.

Example Workflow
python plot_fsc.py


Inputs: postprocess.star file from RELION postprocessing.

Outputs: CSV and multiple PNG plots (as above).

Horizontal lines highlight FSC thresholds, vertical lines mark interpolated resolutions.

Example Output (schematic)
┌─────────────┬───────────────┬───────────────┐
│  Main FSC   │  FSC=0.5 GSFSC│  FSC=0.143 GSFSC │
│  with lines │  horizontal   │  horizontal   │
│  & vertical │  line         │  line         │
└─────────────┴───────────────┴───────────────┘


The final combined figure shows all three panels side-by-side for easy comparison.

Resolution thresholds are clearly annotated, making the plots ready for presentations or publications.

Dependencies

Python 3.7+

Pandas

Matplotlib

pip install pandas matplotlib

Notes

Logarithmic x-axis for clarity.

X-axis inverted to match standard EM plot conventions (high resolution on right).

Custom tick positions for consistent visual appearance.

CSV contains numeric data only (no empty lines between points).
