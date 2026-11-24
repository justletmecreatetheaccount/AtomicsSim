from . import crossSection as cS
from . import halfLife as hL
import matplotlib.pyplot as plt
import numpy as np

def main() -> None:


    # Evaluate the cross section on a log-spaced grid
    E = np.logspace(-4, 6, 10000)           # [eV], from 1e-5 to 1e6
    cs = cS.crossSection(X='U235', Transfo='Fission', E_neutron=E.tolist())

    # Handle both possible return formats
    if isinstance(cs, tuple):                # case: returns (E_out, sigma)
        E_plot, sigma = cs
        E_plot, sigma = np.asarray(E_plot), np.asarray(sigma)
    else:                                    # case: returns sigma aligned with input E
        E_plot, sigma = E, np.asarray(cs)

    fig, ax = plt.subplots(figsize=(9, 5.5))
    ax.loglog(E_plot, sigma, lw=0.8)

    ax.set_xlabel('Incident neutron energy  E  [eV]')
    ax.set_ylabel(r'Fission cross section  $\sigma$  [barn]')
    ax.set_title(r'$^{235}$U(n,f) fission cross section')

    # Reference points to sanity-check the data
    ax.axvline(0.0253, color='gray', ls='--', lw=0.8)          # thermal energy
    ax.annotate('thermal\n0.0253 eV', xy=(0.0253, 1), fontsize=8, color='gray', ha='right')
    ax.axhline(585, color='gray', ls=':', lw=0.8)              # ~585 b expected

    ax.grid(True, which='both', alpha=0.3)
    plt.tight_layout()
    plt.show()
    print(hL.halfLife("U235", "BetaMinus"))
    print(hL.halfLife("U235", "Alpha"))
    print("Hello from atomics!")
