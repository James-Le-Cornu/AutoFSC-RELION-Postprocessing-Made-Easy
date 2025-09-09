import pandas as pd
import matplotlib.pyplot as plt
from io import StringIO
import matplotlib.ticker as mticker

# ===============================
# User Parameters
# ===============================
input_file = "postprocess.star"   # Path to RELION postprocess.star file
output_file = "fsc_for_prism.csv" # Output CSV for FSC data
fsc_column = "CorrectedFourierShellCorrelationPhaseRandomizedMaskedMaps"  # Corrected FSC column
x_column = "AngstromResolution"   # Resolution column for x-axis (in Å)

# ===============================
# Step 1: Extract FSC block from STAR file
# ===============================
fsc_lines = []
inside_fsc = False
with open(input_file, "r") as f:
    for line in f:
        if line.strip().startswith("data_fsc"):
            inside_fsc = True      # Start collecting FSC data
            continue
        if line.strip().startswith("data_guinier"):
            inside_fsc = False     # Stop collecting at guinier block
        if inside_fsc:
            fsc_lines.append(line)

# ===============================
# Step 2: Separate header lines and data lines
# ===============================
header_lines = []
data_lines = []
for line in fsc_lines:
    stripped = line.strip()
    if stripped.startswith("_rln"):
        header_lines.append(stripped)   # STAR column headers
    elif not stripped.startswith("loop_") and stripped:
        data_lines.append(stripped)     # FSC data rows

# Remove "_rln" prefix from column names
col_names = [h.split()[0].replace("_rln","") for h in header_lines]

# ===============================
# Step 3: Load FSC data into pandas DataFrame
# ===============================
df = pd.read_csv(StringIO("\n".join(data_lines)),
                 sep=r"\s+", names=col_names, engine="python")

# ===============================
# Step 4: Convert all columns to numeric and drop NaNs
# ===============================
for col in df.columns:
    df[col] = pd.to_numeric(df[col], errors="coerce")
df = df.dropna()

# ===============================
# Step 5: Interpolate FSC=0.143 and FSC=0.5 resolutions
# ===============================
res_fsc143, res_fsc50 = None, None
if fsc_column in df.columns and x_column in df.columns:
    fsc_values = df[fsc_column].values
    res_values = df[x_column].values
    for i in range(len(res_values)-1):
        # FSC=0.143 interpolation
        if res_fsc143 is None and (fsc_values[i] >= 0.143) and (fsc_values[i+1] < 0.143):
            x1, x2 = res_values[i], res_values[i+1]
            y1, y2 = fsc_values[i], fsc_values[i+1]
            res_fsc143 = x1 + (0.143 - y1)*(x2 - x1)/(y2 - y1)
        # FSC=0.5 interpolation
        if res_fsc50 is None and (fsc_values[i] >= 0.5) and (fsc_values[i+1] < 0.5):
            x1, x2 = res_values[i], res_values[i+1]
            y1, y2 = fsc_values[i], fsc_values[i+1]
            res_fsc50 = x1 + (0.5 - y1)*(x2 - x1)/(y2 - y1)
        if res_fsc143 and res_fsc50:
            break

# ===============================
# Step 6: Save CSV with resolution headers
# ===============================
with open(output_file, "w", newline="") as f:
    f.write("# FSC Data extracted from RELION postprocess.star\n")
    if res_fsc143:
        f.write(f"# FSC=0.143 Resolution (Å): {res_fsc143:.2f}\n")
    if res_fsc50:
        f.write(f"# FSC=0.5 Resolution (Å): {res_fsc50:.2f}\n")
    df.to_csv(f, index=False, float_format="%.10f")

print(f"✅ FSC data extracted and saved to {output_file}")
if res_fsc143:
    print(f"✅ FSC=0.143 resolution: {res_fsc143:.2f} Å")
if res_fsc50:
    print(f"✅ FSC=0.5 resolution: {res_fsc50:.2f} Å")

# ===============================
# Step 7: Individual Plots
# ===============================

# ---------- Panel 1: Main FSC with vertical interpolation lines ----------
plt.figure(figsize=(6,4))
if "FourierShellCorrelationUnmaskedMaps" in df.columns:
    plt.plot(df[x_column], df["FourierShellCorrelationUnmaskedMaps"], label="Unmasked")
if "FourierShellCorrelationMaskedMaps" in df.columns:
    plt.plot(df[x_column], df["FourierShellCorrelationMaskedMaps"], label="Masked")
if fsc_column in df.columns:
    plt.plot(df[x_column], df[fsc_column], label="Corrected")

plt.xscale("log")  # Logarithmic x-axis
plt.ylim(0,1.05)   # y-axis limits
plt.xlim(df[x_column].min(), df[x_column].max())
ax = plt.gca()
ax.set_xlim(ax.get_xlim()[::-1])  # Invert x-axis

# Horizontal reference lines at FSC thresholds
plt.axhline(y=0.143, color="gray", linestyle="--", linewidth=1)
plt.axhline(y=0.5, color="gray", linestyle=":", linewidth=1)

# Vertical lines at interpolated FSC=0.143 and 0.5
if res_fsc143:
    plt.axvline(x=res_fsc143, color="red", linestyle="--", linewidth=1,
                label=f"FSC=0.143: {res_fsc143:.2f} Å")
if res_fsc50:
    plt.axvline(x=res_fsc50, color="blue", linestyle=":", linewidth=1,
                label=f"FSC=0.5: {res_fsc50:.2f} Å")

# Numeric x-axis labels
tick_positions = [0.5, 1, 5, 10, 50, 100, 500]
tick_positions = [t for t in tick_positions if df[x_column].min() <= t <= df[x_column].max()]
ax.set_xticks(tick_positions)
ax.set_xticklabels([str(t) for t in tick_positions])

plt.xlabel("Resolution (Å)")
plt.ylabel("FSC")
plt.title("GSFSC")
plt.legend()
plt.tight_layout()
plt.savefig("FSC_main_plot.png", dpi=300)
plt.close()

# ---------- Panel 1b: Main FSC without vertical lines ----------
plt.figure(figsize=(6,4))
if "FourierShellCorrelationUnmaskedMaps" in df.columns:
    plt.plot(df[x_column], df["FourierShellCorrelationUnmaskedMaps"], label="Unmasked")
if "FourierShellCorrelationMaskedMaps" in df.columns:
    plt.plot(df[x_column], df["FourierShellCorrelationMaskedMaps"], label="Masked")
if fsc_column in df.columns:
    plt.plot(df[x_column], df[fsc_column], label="Corrected")

plt.xscale("log")
plt.ylim(0,1.05)
plt.xlim(df[x_column].min(), df[x_column].max())
ax = plt.gca()
ax.set_xlim(ax.get_xlim()[::-1])
plt.axhline(y=0.143, color="gray", linestyle="--", linewidth=1)
plt.axhline(y=0.5, color="gray", linestyle=":", linewidth=1)

# Numeric x-axis labels
ax.set_xticks(tick_positions)
ax.set_xticklabels([str(t) for t in tick_positions])

plt.xlabel("Resolution (Å)")
plt.ylabel("FSC")
plt.title("GSFSC")
plt.legend()
plt.tight_layout()
plt.savefig("FSC_main_no_lines.png", dpi=300)
plt.close()
print("✅ Main FSC plot without interpolation lines saved as FSC_main_no_lines.png")

# ---------- Panel 2: GSFSC FSC=0.5 ----------
plt.figure(figsize=(6,4))
if "FourierShellCorrelationMaskedMaps" in df.columns:
    plt.plot(df[x_column], df["FourierShellCorrelationMaskedMaps"], label="Masked")
if "FourierShellCorrelationUnmaskedMaps" in df.columns:
    plt.plot(df[x_column], df["FourierShellCorrelationUnmaskedMaps"], label="Unmasked")
if fsc_column in df.columns:
    plt.plot(df[x_column], df[fsc_column], label="Corrected")

plt.xscale("log")
plt.ylim(0,1.05)
x_min = df[x_column].iloc[-1]
x_max = 100
plt.xlim(x_min, x_max)
plt.gca().set_xlim(plt.gca().get_xlim()[::-1])

# Custom tick positions
tick_positions_gs = [100, 80, 60, 40, 20, 10, 8, 6, 4, 2]
tick_positions_gs = [t for t in tick_positions_gs if x_min <= t <= x_max]
plt.gca().set_xticks(tick_positions_gs)
plt.gca().set_xticklabels([str(t) for t in tick_positions_gs])

plt.axhline(y=0.5, color="gray", linestyle=":", linewidth=1)
if res_fsc50:
    plt.title(f"GSFSC: Resolution {res_fsc50:.2f} Å (FSC=0.5)")
plt.xlabel("Resolution (Å)")
plt.ylabel("FSC")
plt.legend()
plt.tight_layout()
plt.savefig("FSC_0.5_plot.png", dpi=300)
plt.close()

# ---------- Panel 3: GSFSC FSC=0.143 ----------
plt.figure(figsize=(6,4))
if "FourierShellCorrelationMaskedMaps" in df.columns:
    plt.plot(df[x_column], df["FourierShellCorrelationMaskedMaps"], label="Masked")
if "FourierShellCorrelationUnmaskedMaps" in df.columns:
    plt.plot(df[x_column], df["FourierShellCorrelationUnmaskedMaps"], label="Unmasked")
if fsc_column in df.columns:
    plt.plot(df[x_column], df[fsc_column], label="Corrected")

plt.xscale("log")
plt.ylim(0,1.05)
plt.xlim(x_min, x_max)
plt.gca().set_xlim(plt.gca().get_xlim()[::-1])
plt.gca().set_xticks(tick_positions_gs)
plt.gca().set_xticklabels([str(t) for t in tick_positions_gs])

plt.axhline(y=0.143, color="gray", linestyle=":", linewidth=1)
if res_fsc143:
    plt.title(f"GSFSC: Resolution {res_fsc143:.2f} Å (FSC=0.143)")
plt.xlabel("Resolution (Å)")
plt.ylabel("FSC")
plt.legend()
plt.tight_layout()
plt.savefig("FSC_0.143_plot.png", dpi=300)
plt.close()

# ===============================
# Step 8: Combined 3-panel Figure
# ===============================
fig, axes = plt.subplots(1, 3, figsize=(18, 4))

# ----- Panel 1: Main FSC -----
ax = axes[0]
if "FourierShellCorrelationUnmaskedMaps" in df.columns:
    ax.plot(df[x_column], df["FourierShellCorrelationUnmaskedMaps"], label="Unmasked")
if "FourierShellCorrelationMaskedMaps" in df.columns:
    ax.plot(df[x_column], df["FourierShellCorrelationMaskedMaps"], label="Masked")
if fsc_column in df.columns:
    ax.plot(df[x_column], df[fsc_column], label="Corrected")
ax.set_xscale("log")
ax.set_ylim(0,1.05)
ax.set_xlim(df[x_column].min(), df[x_column].max())
ax.set_xlim(ax.get_xlim()[::-1])
ax.xaxis.set_major_locator(mticker.LogLocator(base=10.0, subs=[1.0], numticks=10))
ax.xaxis.set_major_formatter(mticker.FormatStrFormatter('%d'))  # Numeric labels
ax.axhline(y=0.143, color="gray", linestyle="--", linewidth=1)
ax.axhline(y=0.5, color="gray", linestyle=":", linewidth=1)
if res_fsc143:
    ax.axvline(x=res_fsc143, color="red", linestyle="--", linewidth=1,
               label=f"FSC=0.143: {res_fsc143:.2f} Å")
if res_fsc50:
    ax.axvline(x=res_fsc50, color="blue", linestyle=":", linewidth=1,
               label=f"FSC=0.5: {res_fsc50:.2f} Å")
ax.set_xlabel("Resolution (Å)")
ax.set_ylabel("FSC")
ax.set_title("GSFSC")
ax.legend()

# ----- Panel 2: GSFSC FSC=0.5 -----
ax = axes[1]
if "FourierShellCorrelationMaskedMaps" in df.columns:
    ax.plot(df[x_column], df["FourierShellCorrelationMaskedMaps"], label="Masked")
if "FourierShellCorrelationUnmaskedMaps" in df.columns:
    ax.plot(df[x_column], df["FourierShellCorrelationUnmaskedMaps"], label="Unmasked")
if fsc_column in df.columns:
    ax.plot(df[x_column], df[fsc_column], label="Corrected")
ax.set_xscale("log")
ax.set_ylim(0,1.05)
ax.set_xlim(x_min, x_max)
ax.set_xlim(ax.get_xlim()[::-1])
ax.set_xticks(tick_positions_gs)
ax.set_xticklabels([str(t) for t in tick_positions_gs])
ax.axhline(y=0.5, color="gray", linestyle=":", linewidth=1)
if res_fsc50:
    ax.set_title(f"GSFSC: Resolution {res_fsc50:.2f} Å (FSC=0.5)")
ax.set_xlabel("Resolution (Å)")
ax.set_ylabel("FSC")
ax.legend()

# ----- Panel 3: GSFSC FSC=0.143 -----
ax = axes[2]
if "FourierShellCorrelationMaskedMaps" in df.columns:
    ax.plot(df[x_column], df["FourierShellCorrelationMaskedMaps"], label="Masked")
if "FourierShellCorrelationUnmaskedMaps" in df.columns:
    ax.plot(df[x_column], df["FourierShellCorrelationUnmaskedMaps"], label="Unmasked")
if fsc_column in df.columns:
    ax.plot(df[x_column], df[fsc_column], label="Corrected")
ax.set_xscale("log")
ax.set_ylim(0,1.05)
ax.set_xlim(x_min, x_max)
ax.set_xlim(ax.get_xlim()[::-1])
ax.set_xticks(tick_positions_gs)
ax.set_xticklabels([str(t) for t in tick_positions_gs])
ax.axhline(y=0.143, color="gray", linestyle=":", linewidth=1)
if res_fsc143:
    ax.set_title(f"GSFSC: Resolution {res_fsc143:.2f} Å (FSC=0.143)")
ax.set_xlabel("Resolution (Å)")
ax.set_ylabel("FSC")
ax.legend()

plt.tight_layout()
plt.savefig("FSC_combined.png", dpi=300)
plt.close()
print("✅ Combined 3-panel figure saved as FSC_combined.png")
