import sys
sys.path.insert(0, '..')
import numpy as np
import matplotlib.pyplot as plt
from mvdlib import plotutils

x = np.linspace(0, 10, 100)
y = np.sin(x)

def test_old_plot_settings():
    from mvdlib import plot_settings
    plot_settings.load_settings('web')
    fig = plt.figure()
    plt.plot(x, y)
    plt.savefig('plotutils.pdf')
    plt.close(fig)

def pgf_test():
    fig = plt.figure()
    plt.plot(x, y)
    plt.xlabel(r'$\xi$')
    plt.ylabel(r'Sine of $\xi$')
    preamble = [
        r'\usepackage[math]{kurier}'
    ]
    plotutils.pgfsave('plotutils.pdf', preamble=preamble)
    plt.close(fig)

if __name__ == "__main__":
    test_old_plot_settings()
    #pgf_test()
