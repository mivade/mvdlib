"""
glass.py

"""

_umsq_to_msq = 1e-12

class Glass(object):
    def __init__(self, B, C):
        try:
            self.B = B
            self.C = C
            if len(B) != 3 or len(C) != 3:
                raise ValueError()
        except (AttributeError, ValueError):
            print("B and C must have length 3.")

    def sellmeier(self, lmbda):
        """Return the index of refraction at wavelength lmbda."""
        n_sq = 1 + self.B[0]*lmbda**2/(lmbda**2 - self.C[0])
        n_sq += self.B[1]*lmbda**2/(lmbda**2 - self.C[1])
        n_sq += self.B[2]*lmbda**2/(lmbda**2 - self.C[2])
        return np.sqrt(n_sq)

# The Sellmeier coefficients were obtained from refractiveindex.info
BK7 = Glass([1.03961212, 0.231792344, 1.01046945],
            [6.00069867e-15, 2.00179144e-14, 1.03560653e-10])
N_BAF10 = Glass([1.5851495, 0.143559385, 1.08521269],
                [0.00926681282e-12, 0.00926681282e-12, 105.613573e-12]

if __name__ == "__main__":
    import matplotlib.pyplot as plt
    import numpy as np
    
    wl = np.linspace(600e-9, 1000e-9, 200)
    plt.plot(wl/1e-9, BK7.sellmeier(wl))
    plt.xlabel(r'$\lambda$ [nm]')
    plt.ylabel(r'$n$')
    plt.show()
