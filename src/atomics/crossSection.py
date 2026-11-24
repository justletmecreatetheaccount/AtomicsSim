import numpy as np
import json

def load_endf_section(file_name):
    """Load an IAEA WebEndfTabSect JSON file and return (E, Sig) arrays."""
    with open(file_name) as f:
        data = json.load(f)

    # A file can contain several datasets; take the first (or pick by LIBRARY)
    ds = data["datasets"][0]
    pts = ds["pts"]

    E    = np.array([p["E"]   for p in pts])   # [eV]
    Sig  = np.array([p["Sig"] for p in pts])   # [barn]
    return E, Sig, ds


def interpolate_cross_section(E, Sig, E_query):
    """Log-log interpolation, robust across many decades of magnitude.

    E_query: scalar, list or ndarray of energies in [eV]
    Returns sigma [barn] with the same shape as E_query.
    """
    E_query = np.atleast_1d(np.asarray(E_query, dtype=float))
    assert E_query.min() >= E[0] and E_query.max() <= E[-1], \
        f"Energies out of range [{E[0]:.1e}, {E[-1]:.1e}] eV"

    # np.interp does linear interpolation; do it in log-log space so that
    # the 1/sqrt(E) low-energy tail and decades-wide resonances behave well
    logSig = np.interp(np.log10(E_query), np.log10(E), np.log10(Sig))
    return 10 ** logSig


def crossSection(X, Transfo, E_neutron):
    """
    Computes the cross section for a specific energy level
    ENDF database: https://www-nds.iaea.org/exfor/endf.htm

    ----------------
    :param X: string
        nuclide or nucleon (for a neutron), that follows the atomic notation of the element,
        e.g.: for the Uranium 235, X = 'U235'
    :param Transfo: string
        name of the considered transformation, should be one of the following in the list
        ['Fission', 'Capture']
    :param E_neutron: array, list
        value(s) of the cross section for an incident neutron of energy level equal to E_neutron in [eV]
        the value should be in the range [1e-5; 2e7] [eV]
    :return: array, list
        values of the cross section in [barn] corresponding to the input parameters
    """

    # Your work : here
    file_name = format("data/" + X + "_" + Transfo + ".json")
    
    E, Sig, ds = load_endf_section(file_name)
    sigma  = interpolate_cross_section(E, Sig, E_neutron)

    
    
    # ==================================  Check arguments  ==================================
    #  Check that the nucleon/nuclide asked, and that the associated transformation exists in the database
    if X != 'Th232' and X != 'Th233' and X != 'Pa233' and X != 'U233' and X != 'U235' and X != 'U236' and X != 'U237' and X != 'U238' \
            and X != 'U239' and X != 'Np239' and X != 'Pu239' and X != 'Pu240' and X != 'Xe135':
        print('\n WARNING : There is no database for element ', X, '. \n Please check function information')
    
    # sigma = 0.

    return sigma

# Try the function:
# cs = crossSection(X='U235', Transfo='Fission', E_neutron=np.logspace(-5,6,10000).tolist())
