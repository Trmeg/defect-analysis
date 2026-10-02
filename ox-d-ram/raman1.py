import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path

# Pristine output file: keep it in your notebook folder
filename = 'OneDrive - IIT Delhi/Pictures/Desktop/sem3/proj major/aug/voram/dynmat.out'

text = Path(filename).read_text(errors='replace')

# Locate the Raman activity table
if '# mode' not in text:
    raise ValueError('Raman activity table not found in the output file.')

table = text.split('# mode', 1)[1]

# Read (frequency, Raman activity) directly from the table
peak = []

for line in table.splitlines()[1:]:
    if 'DYNMAT' in line or 'JOB DONE' in line:
        break

    values = line.split()

    if len(values) != 6:
        continue

    try:
        int(values[0])
        frequency = float(values[1])  # cm^-1 column
        activity = float(values[4])   # Raman column
    except ValueError:
        continue

    # Exclude negative and zero frequencies
    # No intensity cutoff
    if frequency > 0:
        peak.append((frequency, activity))

if not peak:
    raise ValueError('No positive-frequency Raman modes found.')

print('Positive-frequency modes included:', len(peak))


# Define the Gaussian function
def gaussian(w, G, w0, I0):
    return I0 * np.exp(-((w - w0) / G)**2)


# Sum contributions from all modes
# Repeated frequencies are automatically added together
def fit(w, G):
    intensity = np.zeros_like(w)

    for w0, I0 in peak:
        intensity += gaussian(w, G, w0, I0)

    return intensity


w = np.linspace(0, 500, 5000)

plt.figure(figsize=(8, 5))

plt.plot(
    w, fit(w, 2),
    color='blue',
    label='Non-defect'
)

plt.xlabel('Raman shift (cm$^{-1}$)')
plt.ylabel('Intensity (a.u.)')
plt.title('Bi₂O₂Se:frequency modes')

plt.tick_params(
    axis='y', which='both',
    right=False, left=False, labelleft=False
)
plt.tick_params(axis='x', which='both', top=False)

plt.xlim(0, 500)
plt.ylim(bottom=0)
plt.xticks(
    [0, 50, 100, 150,200, 250,300,350, 400,450, 500],
    rotation=45
)

plt.legend()
plt.tight_layout()
plt.savefig('defect.jpg', format='jpg', dpi=300)
plt.show()