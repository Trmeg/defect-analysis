"""
Plot a Raman spectrum from a Quantum ESPRESSO dynmat.x output file.

- Reads the mode table (# mode [cm-1] [THz] IR Raman depol.fact)
- Parses it as FIXED-WIDTH columns (Fortran format i5,f10.2,f10.4,f10.4,f15.4,f10.4),
  so columns that ran into each other (e.g. "2.171631531.3625") are split correctly
- Detects Fortran overflow ("*****") in the Raman column
- Broadens each Raman-active mode with a Gaussian or Lorentzian and plots the sum

If ANY Raman value has overflowed, the true intensities are not in the file.
The script then falls back to plotting peak POSITIONS with equal height and
says so on the plot, instead of silently inventing intensities.
"""
import numpy as np
import matplotlib.pyplot as plt

# ------------------------- user settings -------------------------
FILENAME = r"C:\Users\tarun\OneDrive - IIT Delhi\Pictures\Desktop\sem3\project\sept\seram\dynmatse.out"
WMIN, WMAX = 0, 550        # plotting range, cm^-1
NPTS       = 5000
FWHM       = 5.0           # broadening FWHM, cm^-1
LINESHAPE  = "gaussian"    # "gaussian" or "lorentzian"
FREQ_CUT   = 10.0          # ignore modes below this (acoustic / imaginary), cm^-1
LABEL_PEAKS = True
# -----------------------------------------------------------------

def to_float(s):
    s = s.strip()
    if not s or "*" in s:
        return np.nan          # NaN marks an overflowed field
    return float(s)

def read_dynmat(fname):
    modes = []
    with open(fname) as f:
        lines = f.readlines()
    start = next(i for i, l in enumerate(lines) if l.startswith("# mode"))
    for l in lines[start + 1:]:
        if not l[:5].strip().isdigit():
            break
        # fixed-width slices: i5 | f10.2 | f10.4 | f10.4 | f15.4 | f10.4
        modes.append(dict(
            mode  = int(l[0:5]),
            cm1   = to_float(l[5:15]),
            thz   = to_float(l[15:25]),
            ir    = to_float(l[25:35]),
            raman = to_float(l[35:50]),
            depol = to_float(l[50:60]),
        ))
    return modes

def lineshape(w, w0, fwhm, kind):
    if kind == "gaussian":
        sigma = fwhm / (2 * np.sqrt(2 * np.log(2)))
        return np.exp(-0.5 * ((w - w0) / sigma) ** 2)
    return (0.5 * fwhm) ** 2 / ((w - w0) ** 2 + (0.5 * fwhm) ** 2)

modes = read_dynmat(FILENAME)
print(f"Read {len(modes)} modes ({len(modes)//3} atoms)")

imag = [m for m in modes if m["cm1"] < -1.0]
if imag:
    print(f"WARNING: {len(imag)} imaginary modes:",
          ", ".join(f"{m['cm1']:.2f}" for m in imag))

# Raman-active = Raman value non-zero OR overflowed (overflow means 'very large', not zero)
active = [m for m in modes
          if m["cm1"] > FREQ_CUT and (np.isnan(m["raman"]) or m["raman"] > 1e-4)]
overflow = any(np.isnan(m["raman"]) for m in active)

w = np.linspace(WMIN, WMAX, NPTS)
spec = np.zeros_like(w)
for m in active:
    height = 1.0 if overflow else m["raman"]
    spec += height * lineshape(w, m["cm1"], FWHM, LINESHAPE)
spec /= spec.max()

print("\n mode   freq(cm-1)   Raman activity   depol")
for m in active:
    r = "overflow(*****)" if np.isnan(m["raman"]) else f"{m['raman']:.4f}"
    print(f"{m['mode']:5d} {m['cm1']:11.2f}   {r:>15s}   {m['depol']:.4f}")

fig, ax = plt.subplots(figsize=(7, 4))
ax.plot(w, spec, color="b", lw=1.2)
# stick lines at mode positions (merge degenerate pairs visually)
for m in active:
    ax.axvline(m["cm1"], ymax=0.05, color="gray", lw=0.8)
if LABEL_PEAKS:
    seen = []
    for m in active:
        if all(abs(m["cm1"] - s) > 2.0 for s in seen):
            idx = np.argmin(abs(w - m["cm1"]))
            ax.text(m["cm1"], spec[idx] + 0.02, f"{m['cm1']:.0f}",
                    rotation=90, ha="center", va="bottom", fontsize=7)
            seen.append(m["cm1"])

ax.set_xlabel(r"Raman shift (cm$^{-1}$)")
ax.set_ylabel("Intensity (a.u.)")
ax.set_xlim(WMIN, WMAX)
ax.set_ylim(0, 1.25)
ax.tick_params(axis="y", which="both", left=False, labelleft=False)
title = f"({LINESHAPE}, FWHM = {FWHM} cm$^{{-1}}$)"
if overflow:
    title += "\nRaman activities overflowed equal heights"
ax.set_title(title, fontsize=9)
plt.tight_layout()
plt.savefig("plot-raman.png", dpi=600)
plt.show()
