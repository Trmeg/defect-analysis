import numpy as np
import matplotlib.pyplot as plt

def gaussian(w, G, w0, I0):
    return I0 * np.exp(-((w - w0) / G)**2)

peak = [
    (64.05,  27875.7380),
    (96.56,  36936.9793),
    (112.08, 11393.1402),
    (155.93, 13421.6425),
    (320.64, 10512.4906),
    (351.40, 11549.6388),
    (374.42, 43219.6578),
    (461.98, 22840.2858)
]

def fit(w, G):
    intensity = np.zeros_like(w)
    for w0, I0 in peak:
        intensity += gaussian(w, G, w0, I0)
    return intensity

w = np.linspace(0, 500, 5000)

plt.figure(figsize=(8, 5))
plt.plot(w, fit(w, 2), color='red', label='Oxygen vacancy')
plt.xlabel('Raman shift (cm$^{-1}$)')
plt.ylabel('Intensity (a.u.)')
plt.title('Bi₂O₂Se: Oxygen vacancy — activity ≥ 10,000 Å⁴/amu')
plt.tick_params(axis='y', which='both',
                right=False, left=False, labelleft=False)
plt.tick_params(axis='x', which='both', top=False)
plt.xlim(0, 500)
plt.ylim(bottom=0)
plt.xticks([0, 64.05, 96.56, 112.08, 155.93, 250,
            320.64, 351.40, 374.42, 461.98, 500],
           rotation=60)
plt.legend()
plt.tight_layout()
plt.savefig('defectsel.jpg', format='jpg', dpi=300)
plt.show()