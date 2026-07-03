import numpy as np
import matplotlib.pyplot as plt

class Dataset:
    def __init__(self, filename):
        self.filename = filename
        self.__load_data()

    def __load_data(self):
        data = np.loadtxt(self.filename)
        self.tm = data[:, 0]
        self.xm = data[:, 1]
        self.ym = data[:, 2]
        self.rm = np.sqrt(self.xm**2 + self.ym**2)

ds = {}
ds['ngon3'] = Dataset('ngon3.txt')
ds['ngon4'] = Dataset('ngon4.txt')
ds['ngon6'] = Dataset('ngon6.txt')
ds['ellipse'] = Dataset('ellipse.txt')
ds['flower'] = Dataset('flower.txt')

# for k, v in ds.items():
#     plt.plot(v.xm, v.ym, label=k)
# plt.axis('equal')
# plt.legend()
# plt.show()

plt.figure(figsize=(6.4,3.2))
for k, v in ds.items():
    plt.loglog(v.tm, v.rm, label=k)
# add a segment with slope -1
x = np.array([4e0, 1e2])
y = 2.2e0 * (x**(-1))
plt.plot(x, y, 'k--')
plt.xlabel(r'$\Theta$')
plt.ylabel(r'$r(\Theta)$')
plt.xlim(1e-2, 6e1)

plt.ylim(1.0e-2, 1.5e0)
plt.legend()
plt.tight_layout()
plt.savefig('r_analysis.svg')
plt.show()
