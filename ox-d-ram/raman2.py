import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path

# Input files: keep both in your notebook folder
non_defect_file ='OneDrive - IIT Delhi/Pictures/Desktop/sem3/proj major/aug/rambi221/dynmat.out'
defect_file =  'OneDrive - IIT Delhi/Pictures/Desktop/sem3/proj major/aug/voram/dynmat.out'  # Change to your defect filename


# Read frequency and Raman activity
def read_peaks(filename):
    text = Path(filename).read_text(errors='replace')

    if '# mode' not in text:
        raise ValueError(
            f'Raman activity table not found in {filename}'
        )

    table = text.split('# mode', 1)[1]
    peaks = []

    for line in table.splitlines()[1:]:
        if 'DYNMAT' in line or 'JOB DONE' in line:
            break

        values = line.split()

        if len(values) != 6:
            continue

        try:
            int(values[0])

            # Support scientific notation using E or D
            frequency = float(values[1].replace('D', 'E'))
            activity = float(values[4].replace('D', 'E'))

        except ValueError:
            continue

        # Include all finite positive-frequency modes
        if (
            np.isfinite(frequency)
            and np.isfinite(activity)
            and frequency > 0
        ):
            peaks.append((frequency, activity))

    if not peaks:
        raise ValueError(
            f'No positive-frequency Raman modes found in {filename}'
        )

    print(f'{filename}: {len(peaks)} positive-frequency modes')
    return peaks


# Gaussian function
def gaussian(w, G, w0, I0):
    return I0 * np.exp(-((w - w0) / G)**2)


# Sum contributions from all modes
def spectrum(w, G, peaks):
    intensity = np.zeros_like(w)

    for w0, I0 in peaks:
        intensity += gaussian(w, G, w0, I0)

    return intensity


# Normalize independently: highest intensity becomes 1
def normalize(intensity, label):
    maximum = intensity.max()

    if maximum <= 0:
        raise ValueError(
            f'{label}: no positive intensity in the plotted range '
            'to normalize.'
        )

    return intensity / maximum


# Load both files
non_defect_peaks = read_peaks(non_defect_file)
defect_peaks = read_peaks(defect_file)

# Raman shift range and Gaussian broadening
w = np.linspace(0, 500, 5000)
G = 2

# Calculate spectra
non_defect_intensity = spectrum(w, G, non_defect_peaks)
defect_intensity = spectrum(w, G, defect_peaks)

# Normalize each spectrum within the plotted range
non_defect_normalized = normalize(
    non_defect_intensity, 'Non-defect'
)
defect_normalized = normalize(
    defect_intensity, 'Defect'
)

# Plot comparison
plt.figure(figsize=(8, 5))

plt.plot(
    w,
    non_defect_normalized,
    color='red',
    label='Non-defect',
    linewidth=1.8
)

plt.plot(
    w,
    defect_normalized,
    color='blue',
    label='Defect',
    linewidth=1.8
)

plt.xlabel('Raman shift (cm$^{-1}$)')
plt.ylabel('Normalized intensity')
plt.title('Bi₂O₂Se: Defect vs Non-defect')

plt.xlim(0, 500)
plt.ylim(0, 1.05)

plt.xticks(
    [0, 50, 100, 150,200, 250,300,350, 400,450, 500],
    rotation=45
)

plt.tick_params(
    axis='both', which='both',
    top=False, right=False
)

plt.legend()
plt.tight_layout()
plt.savefig('compare.jpg', format='jpg', dpi=300)
plt.show()