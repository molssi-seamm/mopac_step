# -*- coding: utf-8 -*-

"Metadata for MOPAC."

metadata = {}

"""Description of the computational models for MOPAC.
Hamiltonians, approximations, and basis set/parameterizations.
"""

metadata["computational models"] = {
    "Hartree-Fock": {
        "models": {
            "PM7": {
                "parameterizations": {
                    "PM7": {
                        "elements": "1-60,62-83",
                        "periodic": True,
                        "reactions": True,
                        "optimization": True,
                        "code": "mopac",
                    },
                    "PM7-TS": {
                        "elements": "1-60,62-83",
                        "periodic": True,
                        "reactions": True,
                        "optimization": False,
                        "code": "mopac",
                    },
                }
            },
            "PM6": {
                "parameterizations": {
                    "PM6": {
                        "elements": "1-60,62-83",
                        "periodic": True,
                        "reactions": True,
                        "optimization": True,
                        "code": "mopac",
                    },
                    "PM6-D3": {
                        "description": (
                            "The PM6 Hamiltonian with Grimme's corrections for "
                            "dispersion"
                        ),
                        "elements": "1-60,62-83",
                        "periodic": True,
                        "reactions": True,
                        "optimization": True,
                        "code": "mopac",
                    },
                    "PM6-DH+": {
                        "description": (
                            "The PM6 Hamiltonian with corrections for dispersion "
                            "and hydrogen-bonding"
                        ),
                        "elements": "1-60,62-83",
                        "periodic": True,
                        "reactions": True,
                        "optimization": True,
                        "code": "mopac",
                    },
                    "PM6-DH2": {
                        "description": (
                            "The PM6 Hamiltonian with corrections for dispersion "
                            "and hydrogen-bonding"
                        ),
                        "elements": "1-60,62-83",
                        "periodic": True,
                        "reactions": True,
                        "optimization": True,
                        "code": "mopac",
                    },
                    "PM6-DH2X": {
                        "description": (
                            "The PM6 Hamiltonian with corrections for dispersion "
                            "and hydrogen- and halogen-bonding"
                        ),
                        "elements": "1-60,62-83",
                        "periodic": True,
                        "reactions": True,
                        "optimization": True,
                        "code": "mopac",
                    },
                    "PM6-D3H4": {
                        "description": (
                            "The PM6 Hamiltonian with Řezáč and Hobza's D3H4 "
                            "correction. There are three parts to the D3H4 function:\n"
                            "\t1. A correction to the dispersion.  This uses Grimme's "
                            "D3 method, unmodified, with PM6 specific constants.\n"
                            "\t2. The 'H4' hydrogen-bond function developed by Řezáč "
                            "and Hobza.\n"
                            "\t3. A correction for the known fault in PM6 that "
                            "hydrogen - hydrogen steric repulsive interactions are too "
                            "small. For details, see: European Journal of Medicinal "
                            "Chemistry 2015, 89, 189-197."
                        ),
                        "elements": "1-60,62-83",
                        "periodic": False,
                        "reactions": True,
                        "optimization": True,
                        "code": "mopac",
                    },
                    "PM6-D3H4X": {
                        "description": (
                            "The PM6 Hamiltonian with Brahmkshatriya, et al.'s "
                            "D3H4X correction. This adds corrections to the "
                            "halogen-oxygen and halogen-nitrogen interactions to the "
                            "D3H4 model."
                        ),
                        "elements": "1-60,62-83",
                        "periodic": False,
                        "reactions": True,
                        "optimization": True,
                        "code": "mopac",
                    },
                }
            },
        }
    }
}

metadata["results"] = {
    "AO_ATOMINDEX": {
        "calculation": ["energy", "optimization", "thermodynamics", "vibrations"],
        "description": "atom for AO",
        "dimensionality": ["n_aos"],
        "type": "integer",
    },
    "AO_CHARGES": {
        "calculation": ["energy", "optimization", "thermodynamics", "vibrations"],
        "description": "electrons in the AOs",
        "dimensionality": ["n_aos"],
        "type": "float",
    },
    "AO_SPINS": {
        "calculation": ["energy", "optimization", "thermodynamics", "vibrations"],
        "description": "spins in the AOs",
        "dimensionality": ["n_aos"],
        "type": "float",
    },
    "AO_ZETA": {
        "calculation": ["energy", "optimization", "thermodynamics", "vibrations"],
        "description": "Slater exponent",
        "dimensionality": ["n_aos"],
        "type": "float",
    },
    "AREA": {
        "calculation": ["energy", "optimization", "thermodynamics", "vibrations"],
        "description": "surface area",
        "dimensionality": "scalar",
        "property": "surface area#MOPAC",
        "type": "float",
        "units": "Å^2",
    },
    "ATOM_CHARGES": {
        "calculation": ["energy", "optimization", "thermodynamics", "vibrations"],
        "description": "atom charges",
        "dimensionality": ["n_atoms"],
        "type": "float",
    },
    "ATOM_CORE": {
        "calculation": ["energy", "optimization", "thermodynamics", "vibrations"],
        "description": "number of valence electrons",
        "dimensionality": ["n_atoms"],
        "type": "integer",
    },
    "ATOM_EL": {
        "calculation": ["energy", "optimization", "thermodynamics", "vibrations"],
        "description": "atomic symbol",
        "dimensionality": ["n_atoms"],
        "type": "string",
    },
    "ATOM_PQN": {
        "calculation": ["energy", "optimization", "thermodynamics", "vibrations"],
        "description": "principal quantum number",
        "dimensionality": ["n_aos"],
        "type": "integer",
    },
    "ATOM_SYMTYPE": {
        "calculation": ["energy", "optimization", "thermodynamics", "vibrations"],
        "description": "atomic orbital angular shape",
        "dimensionality": ["n_aos"],
        "type": "string",
    },
    "ATOM_X": {
        "calculation": ["energy", "optimization", "thermodynamics", "vibrations"],
        "description": "x, y, z coordinates",
        "dimensionality": [3, "n_atoms"],
        "type": "float",
        "units": "Å",
    },
    "ATOM_X_FORCE": {
        "calculation": ["thermodynamics", "vibrations"],
        "description": "reoriented coordinates",
        "dimensionality": [3, "n_atoms"],
        "type": "float",
        "units": "Å",
    },
    "ATOM_X_OPT": {
        "calculation": ["optimization", "thermodynamics", "vibrations"],
        "description": "optimized x, y, z coordinates",
        "dimensionality": [3, "n_atoms"],
        "type": "float",
        "units": "Å",
    },
    "ATOM_X_UPDATED": {
        "calculation": ["optimization"],
        "description": "trajectory coordinates",
        "dimensionality": ["nsteps", [3, "n_atoms"]],
        "type": "float",
        "units": "Å",
    },
    "COMMENTS": {
        "calculation": [],
        "description": "User comment line",
        "dimensionality": "scalar",
        "type": "string",
    },
    "CPU_TIME": {
        "calculation": ["energy", "optimization", "thermodynamics", "vibrations"],
        "description": "cpu time for calculation",
        "dimensionality": "scalar",
        "type": "float",
        "units": "s",
    },
    "DATE": {
        "calculation": ["energy", "optimization", "thermodynamics", "vibrations"],
        "description": "date and time of calculation",
        "dimensionality": "scalar",
        "type": "date_time",
    },
    "DENSITY": {
        "calculation": [
            "energy",
            "optimization",
        ],
        "description": "density",
        "dimensionality": "scalar",
        "property": "density",
        "type": "float",
        "units": "g/mL",
    },
    "DIPOLE": {
        "calculation": ["energy", "optimization", "thermodynamics", "vibrations"],
        "description": "dipole moment",
        "dimensionality": "scalar",
        "property": "dipole moment#MOPAC#{model}",
        "type": "float",
        "units": "debye",
    },
    "DIP_VEC": {
        "calculation": ["energy", "optimization", "thermodynamics", "vibrations"],
        "description": "dipole vector",
        "dimensionality": [3],
        "type": "float",
        "units": "debye",
    },
    "EIGENVALUES": {
        "calculation": ["energy", "optimization", "thermodynamics", "vibrations"],
        "description": "orbital energies",
        "dimensionality": ["n_aos"],
        "type": "float",
        "units": "eV",
    },
    "ALPHA_EIGENVALUES": {
        "calculation": ["energy", "optimization", "thermodynamics", "vibrations"],
        "description": "orbital energies",
        "dimensionality": ["n_aos"],
        "type": "float",
        "units": "eV",
    },
    "BETA_EIGENVALUES": {
        "calculation": ["energy", "optimization", "thermodynamics", "vibrations"],
        "description": "orbital energies",
        "dimensionality": ["n_aos"],
        "type": "float",
        "units": "eV",
    },
    "LMO_ENERGY_LEVELS": {
        "calculation": ["energy", "optimization", "thermodynamics", "vibrations"],
        "description": "Localized MO energies",
        "dimensionality": ["n_aos"],
        "type": "float",
        "units": "eV",
    },
    "EIGENVECTORS": {
        "calculation": ["energy", "optimization", "thermodynamics", "vibrations"],
        "description": "orbital coefficients",
        "dimensionality": ["n_aos"],
        "type": "float",
    },
    "ALPHA_EIGENVECTORS": {
        "calculation": ["energy", "optimization", "thermodynamics", "vibrations"],
        "description": "orbital coefficients",
        "dimensionality": ["n_aos"],
        "type": "float",
    },
    "BETA_EIGENVECTORS": {
        "calculation": ["energy", "optimization", "thermodynamics", "vibrations"],
        "description": "orbital coefficients",
        "dimensionality": ["n_aos"],
        "type": "float",
    },
    "LMO_VECTORS": {
        "calculation": ["energy", "optimization", "thermodynamics", "vibrations"],
        "description": "localized molecular orbital coefficients",
        "dimensionality": ["n_aos"],
        "type": "float",
    },
    "EMPIRICAL_FORMULA": {
        "calculation": ["energy", "optimization", "thermodynamics", "vibrations"],
        "description": "empirical formula",
        "dimensionality": "scalar",
        "type": "string",
    },
    "ENERGY_ELECTRONIC": {
        "calculation": ["energy", "optimization", "thermodynamics", "vibrations"],
        "description": "electronic energy",
        "dimensionality": "scalar",
        "property": "electronic energy#MOPAC#{model}",
        "type": "float",
        "units": "eV",
    },
    "ENERGY_NUCLEAR": {
        "calculation": ["energy", "optimization", "thermodynamics", "vibrations"],
        "description": "nuclear repulsion energy",
        "dimensionality": "scalar",
        "property": "nuclear repulsion energy",
        "type": "float",
        "units": "eV",
    },
    "DIEL_ENER": {
        "calculation": ["energy", "optimization", "thermodynamics", "vibrations"],
        "description": "the dielectric energy from COSMO",
        "dimensionality": "scalar",
        "property": "dielectric energy#MOPAC#{model}",
        "type": "float",
        "units": "eV",
    },
    "ENTHALPY_TOT": {
        "calculation": ["thermodynamics", "vibrations"],
        "description": "enthalpy",
        "dimensionality": [
            "n_temps",
        ],
        "type": "float",
        "units": "cal/mol",
    },
    "ENTROPY_TOT": {
        "calculation": ["thermodynamics", "vibrations"],
        "description": "entropy",
        "dimensionality": [
            "n_temps",
        ],
        "type": "float",
        "units": "cal/K/mol",
    },
    "GRADIENTS": {
        "calculation": ["energy", "optimization", "thermodynamics", "vibrations"],
        "description": "gradients on the atoms",
        "dimensionality": [3, "n_atoms"],
        "type": "float",
        "units": "kcal/mol/Å",
    },
    "GRADIENT_NORM": {
        "calculation": ["optimization", "thermodynamics", "vibrations"],
        "description": "final norm of the gradient",
        "dimensionality": "scalar",
        "type": "float",
        "units": "kcal/mol/Å",
    },
    "GRADIENT_UPDATED": {
        "calculation": ["optimization"],
        "description": "forces in trajectory",
        "dimensionality": ["nsteps", [3, "n_atoms"]],
        "type": "float",
        "units": "kcal/mol/Å",
    },
    "HEAT_CAPACITY_TOT": {
        "calculation": ["thermodynamics", "vibrations"],
        "description": "heat capacity",
        "dimensionality": [
            "n_temps",
        ],
        "type": "float",
        "units": "cal/K/mol",
    },
    "HEAT_OF_FORMATION": {
        "calculation": ["energy", "optimization", "thermodynamics", "vibrations"],
        "description": "enthalpy of formation",
        "dimensionality": "scalar",
        "property": "enthalpy of formation#MOPAC#{model}",
        "type": "float",
        "units": "kcal/mol",
    },
    "HEAT_OF_FORM_UPDATED": {
        "calculation": ["optimization"],
        "description": "enthalpy of formation in trajectory",
        "dimensionality": ["nsteps"],
        "type": "float",
        "units": "kcal/mol",
    },
    "HESSIAN_MATRIX": {
        "calculation": ["thermodynamics", "vibrations"],
        "description": "Hessian matrix",
        "dimensionality": ["n_dof", "n_dof"],
        "type": "float",
        "units": "mdyne/Å/Da",
    },
    "H_O_F(T)": {
        "calculation": ["thermodynamics", "vibrations"],
        "description": "enthalpy of formation vs T",
        "dimensionality": ["n_temps"],
        "type": "float",
        "units": "kcal/mol",
    },
    "INT_FORCE_CONSTS": {
        "calculation": ["thermodynamics", "vibrations"],
        "description": "force constants for internals",
        "dimensionality": ["n_dofs"],
        "type": "float",
        "units": "mdyne/Å",
    },
    "INITIAL_TRANS_VECTS": {
        "calculation": [
            "energy",
            "optimization",
        ],
        "description": "initial translation vectors",
        "dimensionality": [9],
        "type": "float",
        "units": "Å",
    },
    "IONIZATION_POTENTIAL": {
        "calculation": ["energy", "optimization", "thermodynamics", "vibrations"],
        "description": "ionization energy (IE)",
        "dimensionality": "scalar",
        "property": "ionization energy#MOPAC#{model}",
        "type": "float",
        "units": "eV",
    },
    "ISOTOPIC_MASSES": {
        "calculation": ["thermodynamics", "vibrations"],
        "description": "isotopic masses",
        "dimensionality": ["n_atoms"],
        "type": "float",
        "units": "Da",
    },
    "KEYWORDS": {
        "calculation": [],
        "description": "MOPAC keywords",
        "dimensionality": "scalar",
        "type": "string",
    },
    "M.O.SYMMETRY_LABELS": {
        "calculation": ["energy", "optimization", "thermodynamics", "vibrations"],
        "description": "molecular orbital symmetries",
        "dimensionality": ["n_mos"],
        "type": "string",
    },
    "ALPHA_M.O.SYMMETRY_LABELS": {
        "calculation": ["energy", "optimization", "thermodynamics", "vibrations"],
        "description": "molecular orbital symmetries",
        "dimensionality": ["n_mos"],
        "type": "string",
    },
    "BETA_M.O.SYMMETRY_LABELS": {
        "calculation": ["energy", "optimization", "thermodynamics", "vibrations"],
        "description": "molecular orbital symmetries",
        "dimensionality": ["n_mos"],
        "type": "string",
    },
    "METHOD": {
        "calculation": ["energy", "optimization", "thermodynamics", "vibrations"],
        "description": "hamiltonian",
        "dimensionality": "scalar",
        "type": "string",
    },
    "MOLECULAR_ORBITAL_OCCUPANCIES": {
        "calculation": ["energy", "optimization", "thermodynamics", "vibrations"],
        "description": "orbital occupancies",
        "dimensionality": ["n_mos"],
        "type": "float",
    },
    "ALPHA_MOLECULAR_ORBITAL_OCCUPANCIES": {
        "calculation": ["energy", "optimization", "thermodynamics", "vibrations"],
        "description": "orbital occupancies",
        "dimensionality": ["n_mos"],
        "type": "float",
    },
    "BETA_MOLECULAR_ORBITAL_OCCUPANCIES": {
        "calculation": ["energy", "optimization", "thermodynamics", "vibrations"],
        "description": "orbital occupancies",
        "dimensionality": ["n_mos"],
        "type": "float",
    },
    "MOLECULAR_WEIGHT": {
        "calculation": ["energy", "optimization", "thermodynamics", "vibrations"],
        "description": "molecular weight",
        "dimensionality": "scalar",
        "type": "float",
        "units": "Da",
    },
    "MOPAC_VERSION": {
        "calculation": ["energy", "optimization", "thermodynamics", "vibrations"],
        "description": "MOPAC version",
        "dimensionality": "scalar",
        "type": "string",
    },
    "NORMAL_MODES": {
        "calculation": ["thermodynamics", "vibrations"],
        "description": "normal modes",
        "dimensionality": ["n_dof", "n_dof"],
        "type": "float",
    },
    "NORMAL_MODE_SYMMETRY_LABELS": {
        "calculation": ["thermodynamics", "vibrations"],
        "description": "symmetry labels of normal modes",
        "dimensionality": ["n_dof"],
        "type": "string",
    },
    "NUMBER_SCF_CYCLES": {
        "calculation": ["energy", "optimization", "thermodynamics", "vibrations"],
        "description": "number of scf's",
        "dimensionality": "scalar",
        "type": "integer",
    },
    "NUM_ALPHA_ELECTRONS": {
        "calculation": ["energy", "optimization", "thermodynamics", "vibrations"],
        "description": "number of spin-up electrons",
        "dimensionality": "scalar",
        "type": "integer",
    },
    "NUM_BETA_ELECTRONS": {
        "calculation": ["energy", "optimization", "thermodynamics", "vibrations"],
        "description": "number of spin-down electrons",
        "dimensionality": "scalar",
        "type": "integer",
    },
    "NUM_ELECTRONS": {
        "calculation": ["energy", "optimization", "thermodynamics", "vibrations"],
        "description": "number of electrons",
        "dimensionality": "scalar",
        "type": "integer",
    },
    "ORIENTATION_ATOM_X": {
        "calculation": ["thermodynamics", "vibrations"],
        "description": "",
        "dimensionality": [3, "n_atoms"],
        "type": "float",
        "units": "Å",
    },
    "OVERLAP_MATRIX": {
        "calculation": ["energy", "optimization", "thermodynamics", "vibrations"],
        "description": "the AO overlap matrix",
        "dimensionality": ["triangular", "n_aos", "n_aos"],
        "type": "float",
    },
    "DENSITY_MATRIX": {
        "calculation": ["energy", "optimization", "thermodynamics", "vibrations"],
        "description": "the density matrix",
        "dimensionality": ["triangular", "n_aos", "n_aos"],
        "type": "float",
    },
    "POINT_GROUP": {
        "calculation": ["energy", "optimization", "thermodynamics", "vibrations"],
        "description": "the molecular symmetry",
        "dimensionality": "scalar",
        "type": "string",
    },
    "PRI_MOM_OF_I": {
        "calculation": ["thermodynamics", "vibrations"],
        "description": "primary moments of inertia",
        "dimensionality": [3],
        "type": "float",
        "units": "10^-40*g*cm^2",
    },
    "RESTRAINING_PRESSURE": {
        "calculation": [
            "energy",
            "optimization",
        ],
        "description": "the pressure in the three lattice directions",
        "dimensionality": [3],
        "type": "float",
        "units": "GPa",
    },
    "ROTAT_CONSTS": {
        "calculation": ["thermodynamics", "vibrations"],
        "description": "rotational constants",
        "dimensionality": [3],
        "type": "float",
        "units": "1/cm",
    },
    "SET_OF_MOS": {
        "calculation": ["energy", "optimization", "thermodynamics", "vibrations"],
        "description": "set of MOs",
        "dimensionality": [2],
        "type": "string",
    },
    "SET_OF_ALPHA_MOS": {
        "calculation": ["energy", "optimization", "thermodynamics", "vibrations"],
        "description": "set of MOs",
        "dimensionality": [2],
        "type": "string",
    },
    "SET_OF_BETA_MOS": {
        "calculation": ["energy", "optimization", "thermodynamics", "vibrations"],
        "description": "set of MOs",
        "dimensionality": [2],
        "type": "string",
    },
    "SIZE_OF_ACTIVE_SPACE": {
        "calculation": [
            "optimization",
        ],
        "description": "size of active space",
        "dimensionality": [1],
        "type": "string",
    },
    "NUMBER_MICROSTATES": {
        "calculation": [
            "optimization",
        ],
        "description": "number of microstates",
        "dimensionality": [1],
        "type": "string",
    },
    "MICROSTATE_CONFIGURATIONS": {
        "calculation": [
            "optimization",
        ],
        "description": "microstate configurations",
        "dimensionality": [
            "n_microstates",
        ],
        "type": "integer",
    },
    "STATE_REQUESTED": {
        "calculation": [
            "optimization",
        ],
        "description": "state requested",
        "dimensionality": [1],
        "type": "integer",
    },
    "STATE_DEGENERACY": {
        "calculation": [
            "optimization",
        ],
        "description": "number of microstates",
        "dimensionality": [1],
        "type": "string",
    },
    "STATE_VECTOR": {
        "calculation": [
            "optimization",
        ],
        "description": "state vector",
        "dimensionality": [1],
        "type": "float",
    },
    "STATE": {
        "calculation": [
            "optimization",
        ],
        "description": "state",
        "dimensionality": [1],
        "type": "string",
    },
    "STATE_ENERGY_ABSOLUTE": {
        "calculation": [
            "optimization",
        ],
        "description": "state energy absolute",
        "dimensionality": [1],
        "type": "string",
    },
    "STATE_ENERGY_RELATIVE": {
        "calculation": [
            "optimization",
        ],
        "description": "state",
        "dimensionality": [1],
        "type": "string",
    },
    "SPIN_COMPONENT": {
        "calculation": ["energy", "optimization", "thermodynamics", "vibrations"],
        "description": "spin component",
        "dimensionality": [3],
        "type": "float",
    },
    "THERMODYNAMIC_PROPERTIES_TEMPS": {
        "calculation": ["thermodynamics", "vibrations"],
        "description": "temperature for thermodynamic properties",
        "dimensionality": ["n_temps"],
        "type": "float",
        "units": "K",
    },
    "TITLE": {
        "calculation": [],
        "description": "title of calculation",
        "dimensionality": "scalar",
        "type": "string",
    },
    "TOTAL_DENSITY_MATRIX": {
        "calculation": ["energy", "optimization", "thermodynamics", "vibrations"],
        "description": "density matrix",
        "dimensionality": ["n_mos", "n_mos"],
        "shape": "triangular",
        "type": "float",
    },
    "ALPHA_DENSITY_MATRIX": {
        "calculation": ["energy", "optimization", "thermodynamics", "vibrations"],
        "description": "density matrix",
        "dimensionality": ["n_mos", "n_mos"],
        "shape": "triangular",
        "type": "float",
    },
    "BETA_DENSITY_MATRIX": {
        "calculation": ["energy", "optimization", "thermodynamics", "vibrations"],
        "description": "density matrix",
        "dimensionality": ["n_mos", "n_mos"],
        "shape": "triangular",
        "type": "float",
    },
    "TOTAL_ENERGY": {
        "calculation": ["energy", "optimization", "thermodynamics", "vibrations"],
        "description": "total energy",
        "dimensionality": "scalar",
        "property": "total energy#MOPAC#{model}",
        "type": "float",
        "units": "eV",
    },
    "HOMO Energy": {
        "calculation": ["energy", "optimization", "thermodynamics", "vibrations"],
        "description": "energy of the HOMO",
        "dimensionality": "scalar",
        "property": "HOMO energy#MOPAC#{model}",
        "type": "float",
        "units": "eV",
    },
    "LUMO Energy": {
        "calculation": ["energy", "optimization", "thermodynamics", "vibrations"],
        "description": "energy of the LUMO",
        "dimensionality": "scalar",
        "property": "LUMO energy#MOPAC#{model}",
        "type": "float",
        "units": "eV",
    },
    "HOMO-LUMO Gap": {
        "calculation": ["energy", "optimization", "thermodynamics", "vibrations"],
        "description": "The energy of the HOMO-LUMO gap",
        "dimensionality": "scalar",
        "property": "band gap#MOPAC#{model}",
        "type": "float",
        "units": "eV",
    },
    "TOTAL_SPIN": {
        "calculation": ["energy", "optimization", "thermodynamics", "vibrations"],
        "description": "spin",
        "dimensionality": "scalar",
        "property": "S^2#MOPAC#{model}",
        "type": "float",
    },
    "TRANS_VECTS": {
        "calculation": [
            "energy",
            "optimization",
        ],
        "description": "initial translation vectors",
        "dimensionality": [9],
        "type": "float",
        "units": "Å",
    },
    "TRANS_VECTS_UPDATED": {
        "calculation": [
            "energy",
            "optimization",
        ],
        "description": "initial translation vectors",
        "dimensionality": [9],
        "type": "float",
        "units": "Å",
    },
    "VIB._EFF_MASS": {
        "calculation": ["thermodynamics", "vibrations"],
        "description": "vibrational effective masses",
        "dimensionality": ["n_dof"],
        "type": "float",
        "units": "Da",
    },
    "VIB._FREQ": {
        "calculation": ["thermodynamics", "vibrations"],
        "description": "vibrational frequencies",
        "dimensionality": ["n_dof"],
        "type": "float",
        "units": "1/cm",
    },
    "VIB._RED_MASS": {
        "calculation": ["thermodynamics", "vibrations"],
        "description": "vibrational reduced masses",
        "dimensionality": ["n_dof"],
        "type": "float",
        "units": "Da",
    },
    "VIB._TRAVEL": {
        "calculation": ["thermodynamics", "vibrations"],
        "description": "vibrational lenght of travel",
        "dimensionality": ["n_dof"],
        "type": "float",
        "units": "Å",
    },
    "VIB._T_DIP": {
        "calculation": ["thermodynamics", "vibrations"],
        "description": "vibrational transition dipole",
        "dimensionality": ["n_dof"],
        "type": "float",
    },
    "VOLUME": {
        "calculation": ["energy", "optimization", "thermodynamics", "vibrations"],
        "description": "volume",
        "dimensionality": "scalar",
        "property": "volume#MOPAC",
        "type": "float",
        "units": "Å^3",
    },
    "ZERO_POINT_ENERGY": {
        "calculation": ["thermodynamics", "vibrations"],
        "description": "zero point energy",
        "dimensionality": "scalar",
        "property": "zero point energy#MOPAC#{model}",
        "type": "float",
        "units": "kcal/mol",
    },
}
