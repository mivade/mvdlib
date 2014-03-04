"""
mvdlib.optics.glass

"""

from __future__ import print_function
from __future__ import division
import numpy as np
import scipy.misc

_umsq_to_msq = 1e-12
_nm_to_micron = 0.001
_m_to_micron = 1e6

class Glass(object):
    def __init__(self, B, C):
        """
        B and C are length 3 array-like objects which are the
        Sellmeier coefficients. The B coefficients are unitless and
        the C coefficients have dimension micron**2.

        References
        ----------

        * `Refractive indices <http://refractiveindex.info/>`_
        * `Sellmeier equation <https://en.wikipedia.org/wiki/Sellmeier_equation>`_

        """
        try:
            self.B = B
            self.C = C
            if len(B) != 3 or len(C) != 3:
                raise ValueError()
        except (AttributeError, ValueError):
            raise RuntimeError("B and C must have length 3.")

    def sellmeier(self, lmbda):
        """
        Return the index of refraction at wavelength lmbda given in
        meters.

        References
        ----------

        https://en.wikipedia.org/wiki/Sellmeier_equation

        """
        wl = lmbda * _m_to_micron
        n_sq = 1.
        for i in range(3):
            n_sq += self.B[i]*wl**2/(wl**2 - self.C[i])
        return np.sqrt(n_sq)

    def chromatic_dispersion(self, lmbda):
        """
        Compute the chromatic dispersion dn/dlambda at the wavelength
        lmbda.

        References
        ----------
        * https://en.wikipedia.org/wiki/Dispersion_(optics)
        * http://refractiveindex.info/
        
        """
        return scipy.misc.derivative(self.sellmeier, lmbda, dx=1e-10)

    def focal_length(self, lmbda, R1, R2='inf', d=None):
        """
        Return the focal length for light at wavelength lmbda of a
        lens with radii of curvature R1 and R2 and center thickness
        d. If R2 is given as 'inf', it is treated as a PCX (or PCV)
        lens.

        References
        ----------

        See the 'Tutorial' tab from Thorlabs_.

        .. _Thorlabs: http://www.thorlabs.com/newgrouppage9.cfm?objectgroup_id=3280

        """
        n = self.sellmeier(lmbda)
        if R2 is 'inf':
            return 1/((n - 1)*(1/R1))
        else:
            if d is None:
                raise RuntimeError("To use the thick lens equation, you " + \
                                   "must specify a lens thickness.")
            A = n - 1
            B = 1/R1 - 1/R2 + A*d/(n*R1*R2)
            return 1/(A*B)

# Sellmeier coefficients were obtained from refractiveindex.info
BK7 = Glass([1.03961212, 0.231792344, 1.01046945],
            [6.00069867e-3, 2.00179144e-2, 1.03560653e2])
SF5 = Glass([1.46141885, 0.247713019, 0.949995832],
            [0.0111826126, 0.0508594669, 112.041888])
SF10 = Glass([1.61625977, 0.259229334, 1.07762317],
             [0.0127534559, 0.0581983954, 116.60768])
N_SF6HT = Glass([1.77931763, 0.338149866, 2.08734474],
                [0.0133714182, 0.0617533621, 174.01759])
N_LAK22 = Glass([1.14229781, 0.535138441, 1.04088385],
                [0.00585778594, 0.0198546147, 100.834017])

if __name__ == "__main__":
    import matplotlib.pyplot as plt

    if False:
        print(BK7.sellmeier(600e-9))
    if False:
        wl = np.linspace(600e-9, 1000e-9, 200)
        plt.plot(wl, BK7.sellmeier(wl))
        plt.xlabel(r'$\lambda$ [nm]')
        plt.ylabel(r'$n$')
        plt.show()
    if False:
        wl = np.linspace(800e-9, 850e-9, 100)
        plt.plot(wl/1e-9, BK7.focal_length(wl, 51.5e-3))
        plt.xlabel(r'$\lambda$ [nm]')
        plt.ylabel(r'$f$ [mm]')
        plt.xlim(800, 850)
        plt.show()
    if True:
        print(SF10.chromatic_dispersion(800e-9)*1e-6, "1/micron")
