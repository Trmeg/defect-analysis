import numpy as np
import matplotlib.pyplot as plt

def gaussian(w, G, w0, I0):
    return I0 * np.exp(-((w - w0) / G)**2)

# Dominant pristine peaks: (frequency, Raman activity)
# Degenerate modes at the same frequency are summed.
peak = [
    (64.59,  2783.5936),
    (162.47, 2226.3518),
    (352.56, 10214.0870),
    (420.78, 4830.5964)
]

def fit(w, G):
    intensity = np.zeros_like(w)
    for w0, I0 in peak:
        intensity += gaussian(w, G, w0, I0)
    return intensity

w = np.linspace(0, 500, 5000)

plt.figure(figsize=(8, 5))
plt.plot(w, fit(w, 2), color='blue', label='Non-defect')
plt.xlabel('Raman shift (cm$^{-1}$)')
plt.ylabel('Intensity (a.u.)')
plt.title('Bi₂O₂Se: Non-defect — dominant peaks')
plt.tick_params(axis='y', which='both',
                right=False, left=False, labelleft=False)
plt.tick_params(axis='x', which='both', top=False)
plt.xlim(0, 500)
plt.ylim(bottom=0)
plt.xticks([0, 64.59, 162.47, 250, 352.56, 420.78, 500],
           rotation=45)
plt.legend()
plt.tight_layout()
plt.savefig('nondefect.jpg', format='jpg', dpi=300)
plt.show()