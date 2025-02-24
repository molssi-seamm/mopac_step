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
                    "PM6-ORG": {
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

"""Description of the MOPAC keywords.

Fields
------
description : str
    A human readable description of the keyword.
takes values : int (optional)
    Number of values the keyword takes. If missing the keyword takes no values.
default : str (optional)
    The default value(s) if the keyword takes values.
format : str (optional)
    How the keyword is formatted in the MOPAC input.
"""
metadata["keywords"] = {
    "0SCF": {
        "description": "Read in data, then stop",
    },
    "1ELECTRON": {
        "description": "Print final one-electron matrix",
    },
    "1SCF": {
        "description": "Do one scf and then stop",
    },
    "ADD-H": {
        "description": (
            "Add hydrogen atoms (intended for use with organic " "compounds)"
        ),
    },
    "A0": {
        "description": "Input geometry is in atomic units",
    },
    "AIDER": {
        "description": "Read in ab-initio derivatives",
    },
    "AIGIN": {
        "description": "Geometry must be in Gaussian format",
    },
    "AIGOUT": {
        "description": "Print the geometry in Gaussian format in the ARC file",
    },
    "ALLBONDS": {
        "description": (
            "Print final bond-order matrix, including bonds to " "hydrogen"
        ),
    },
    "ALLVEC": {
        "description": "Print all vectors (keywords vectors also needed)",
    },
    "ALT_A": {
        "description": "In PDB files with alternative atoms, select atoms A",
        "takes values": 1,
        "default": "A",
        "format": "{}={}",
    },
    "ANGSTROMS": {
        "description": "Input geometry is in Angstroms",
    },
    "AUTOSYM": {
        "description": "Symmetry to be imposed automatically",
    },
    "AUX": {
        "description": ("Output auxiliary information for use by other " "programs"),
    },
    "AM1": {
        "description": "Use the AM1 hamiltonian",
    },
    "BAR": {
        "description": "reduce bar length by a maximum of n.nn%",
        "takes values": 1,
        "default": "0.01",
        "format": "{}={}",
    },
    "BCC": {
        "description": "Only even unit cells used (used by BZ)",
    },
    "BIGCYCLES": {
        "description": "Do a maximum of n big steps",
        "takes values": 1,
        "default": "1",
        "format": "{}={}",
    },
    "BIRADICAL": {
        "description": "System has two unpaired electrons",
    },
    "BFGS": {
        "description": "Use the Flepo or BFGS geometry optimizer",
    },
    "BONDS": {
        "description": "Print final bond-order matrix",
    },
    "CAMP": {
        "description": "Use Camp-King converger in SCF",
    },
    "CARTAB": {
        "description": "Print point-group character table",
    },
    "C.I.": {
        "description": "A multi-electron configuration interaction specified",
        "takes values": [1, 2],
        "default": "2",
        "format": "{}={}",
    },
    "CHAINS(text)": {
        "description": ("In a protein, explicitly define the letters of " "chains."),
    },
    "CHECK": {
        "description": "Report possible faults in input geometry",
    },
    "CHARGE": {
        "description": "Charge on system = n (e.g. NH4 = +1)",
        "takes values": 1,
        "default": "+1",
        "format": "{}={}",
    },
    "CHARGES": {
        "description": (
            "Print net charge on the system, and all charges in " "the system"
        ),
    },
    "CHARST": {
        "description": "Print details of working in CHARST",
    },
    "CIS": {
        "description": "C.I. uses 1 electron excitations only",
    },
    "CISD": {
        "description": "C.I. uses 1 and 2 electron excitations",
    },
    "CISDT": {
        "description": "C.I. uses 1, 2 and 3 electron excitations",
    },
    "COMPARE": {
        "description": "Compare the geometries of two systems",
    },
    "COMPFG": {
        "description": "Print heat of formation calculated in COMPFG",
    },
    "COSCCH": {
        "description": "Add in COSMO charge corrections",
    },
    "COSWRT": {
        "description": ("Write details of the solvent accessible surface to a " "file"),
    },
    "CUTOFP": {
        "description": "Madelung distance cutoff is n .nn Angstroms",
        "takes values": 1,
        "default": "15.0",
        "format": "{}={}",
    },
    "CUTOFF": {
        "description": (
            "In MOZYME, the interatomic distance where the NDDO " "approximation stops"
        ),
        "takes values": 1,
        "default": "6.0",
        "format": "{}={}",
    },
    "CUTOF1": {
        "description": "In MOZYME, the cutoff distance for polarization",
        "takes values": 1,
        "default": "10.0",
        "format": "{}={}",
    },
    "CUTOF2": {
        "description": ("In MOZYME, the cutoff distance for two-center " "integral"),
        "takes values": 1,
        "default": "9.9",
        "format": "{}={}",
    },
    "CUTOFS": {
        "description": "In MOZYME, the cutoff distance for overlap integrals",
        "takes values": 1,
        "default": "9.0",
        "format": "{}={}",
    },
    "CYCLES": {
        "description": "Do a maximum of n steps of geometry optimization",
        "takes values": 1,
        "default": "50",
        "format": "{}={}",
    },
    "CVB": {
        "description": (
            "In MOZYME. add and remove specific bonds to allow a "
            "Lewis or PDB structure."
        ),
    },
    "DAMP": {
        "description": (
            "in MOZYME. damp SCF oscillations using a factor of "
            "n.nn, 0<n.nn<1.0, <0.5 for solids"
        ),
        "takes values": 1,
        "default": "0.5",
        "format": "{}={}",
    },
    "DATA": {
        "description": "Input data set is re-defined to text",
        "takes values": 1,
        "default": "/file.dat",
        "format": "{}={}",
    },
    "DCART": {
        "description": "Print part of working in DCART",
    },
    "DDMAX": {
        "description": (
            "The maximum value of the trust radius in EF and TS. "
            "Defaults to 0.3 in TS and 0.5 in EF"
        ),
        "takes values": 1,
        "default": "0.3",
        "format": "{}={}",
    },
    "DDMIN": {
        "description": (
            "Minimum trust radius in a EF/TS calculation. "
            "Defaults to 0.001. Use smaller values close to "
            "minimium"
        ),
        "takes values": 1,
        "default": "0.00001",
        "format": "{}={}",
    },
    "DEBUG": {
        "description": "Debug option turned on",
    },
    "DEBUG PULAY": {
        "description": "Print working in PULAY",
    },
    "DENOUT": {
        "description": "Density matrix output, unformatted",
    },
    "DENOUTF": {
        "description": "Density matrix output, formatted",
    },
    "DENSITY": {
        "description": "Print final density matrix",
    },
    "DERI1": {
        "description": "Print part of working in DERI1",
    },
    "DERI2": {
        "description": "Print part of working in DERI2",
    },
    "DERITR": {
        "description": "Print part of working in DERIT",
    },
    "DERIV": {
        "description": "Print part of working in DERIV",
    },
    "DERNVO": {
        "description": "Print part of working in DERNVO",
    },
    "DFORCE": {
        "description": "Force calculation specified, also print force matrix.",
    },
    "DFP": {
        "description": (
            "Use Davidson-Fletcher-Powell method to optimize " "geometries"
        ),
    },
    "DISEX": {
        "description": (
            "Distance for interactions in fine grid in COSMO. "
            "Defaults is 2.0, should converge results using "
            "smaller values if needed."
        ),
        "takes values": 1,
        "default": "2.0",
        "format": "{}={}",
    },
    "DISP": {
        "description": (
            "Print the hydrogen bonding and dispersion "
            "contributions to the heat of formation"
        ),
    },
    "DMAX": {
        "description": "Maximum stepsize in eigenvector following",
        "takes values": 1,
        "default": "2.0",
        "format": "{}={}",
    },
    "DOUBLET": {
        "description": "Doublet state required",
    },
    "DRC": {
        "description": (
            "Dynamic reaction coordinate calculation. The "
            "parameter, if given, is the cooling half-life in fs"
        ),
        "takes values": [0, 1],
        "default": "50",
        "format": "{}={}",
    },
    "DUMP": {
        "description": (
            "Write restart files every n seconds, or minutes or "
            'hours with "m" or "h" suffix'
        ),
        "takes values": 1,
        "default": "2h",
        "format": "{}={}",
    },
    "ECHO": {
        "description": "Data are echoed back before calculation starts",
    },
    "EF": {
        "description": ("Use the EigenFollowing routine for geometry " "optimization"),
    },
    "EIGEN": {
        "description": (
            "Print canonical eigenvectors instead of LMOs in a " "MOZYME calculations"
        ),
    },
    "EIGS": {
        "description": "Print all eigenvalues in ITER",
    },
    "ENPART": {"description": "Partition energy into components"},
    "EPS": {
        "description": "Dielectric constant in COSMO calculation",
        "takes values": 1,
        "default": "78.4",
        "format": "{}={}",
    },
    "ESP": {
        "description": "Electrostatic potential calculation",
    },
    "ESPRST": {
        "description": "Restart of electrostatic potential",
    },
    "ESR": {
        "description": "Calculate RHF spin density",
    },
    "EXCITED": {
        "description": "Optimize first excited singlet state",
    },
    "EXTERNAL": {
        "description": "Read parameters from a file",
        "takes values": 1,
        "default": '"file name"',
        "format": "{}={}",
    },
    "FIELD=(n.nn,m.mm,l.ll)": {
        "description": (
            "Apply an external electric field of a,b,c V/Å in the"
            "Cartesian directions"
        ),
        "takes values": 3,
        "default": "(0,0,1)",
        "format": "{}={}",
    },
    "FILL": {
        "description": ("In RHF open and closed shell, force M.O. n to be " "filled"),
        "takes values": 1,
        "default": "0",
        "format": "{}={}",
    },
    "FLEPO": {
        "description": "Print details of geometry optimization",
    },
    "FMAT": {
        "description": "Print details of working in FMAT",
    },
    "FOCK": {
        "description": "Print last Fock matrix",
    },
    "FREQCY": {
        "description": "Print symmetrized Hessian in a FORCE calculation",
    },
    "FORCE": {
        "description": "Calculate vibrational frequencies",
    },
    "FORCETS": {
        "description": (
            "Calculate the vibrational frequencies for atoms in a " "transition state"
        ),
    },
    "GEO-OK": {
        "description": "Override some safety checks",
    },
    "GEO_DAT": {
        "description": "Read in geometry from the file <text>",
        "takes values": 1,
        "default": '"file name"',
        "format": "{}={}",
    },
    "GEO_REF=<text>": {
        "description": "Read in a second geometry from the file <text>",
        "takes values": 1,
        "default": '"SELF"',
        "format": "{}={}",
    },
    "GNORM": {
        "description": (
            "Exit when the gradient norm drops below n.nn " "kcal/mol/Angstrom"
        ),
        "takes values": 1,
        "default": "10.0",
        "format": "{}={}",
    },
    "GRADIENTS": {
        "description": "Print all gradients",
    },
    "GRAPH": {
        "description": "Generate unformatted file for graphics",
    },
    "GRAPHF": {
        "description": (
            "Generate a formatted file for graphics suitable for " "Jmol and MOPETE."
        ),
    },
    "HCORE": {
        "description": (
            "Print all parameters used, the one-electron matrix, "
            "and two-electron integrals"
        ),
    },
    "HESSIAN": {
        "description": "Print Hessian from geometry optimization",
    },
    "HESS": {
        "description": "Options for calculating Hessian matrices in EF",
        "takes values": 1,
        "default": "1",
        "format": "{}={}",
        "allowed values": (0, 1, 2),
    },
    "H-PRIORITY": {
        "description": (
            "Heat of formation takes priority in DRC. Print "
            "whenever the energy changes by this many kcal/mol"
        ),
        "takes values": 1,
        "default": "0.1",
        "format": "{}={}",
    },
    "HTML": {
        "description": "Write a web-page for displaying and editing a protein",
    },
    "HYPERFINE": {
        "description": "Hyperfine coupling constants to be calculated",
    },
    "INT": {
        "description": "Make all coordinates internal coordinates",
    },
    "INVERT": {
        "description": "Reverse all optimization flags",
    },
    "IRC": {
        "description": "Intrinsic reaction coordinate calculation",
        "takes values": [0, 1],
        "default": "",
        "format": "{}={}",
    },
    "ISOTOPE": {
        "description": "Force matrix written to disk (channel 9 )",
    },
    "ITER": {
        "description": "Print details of working in ITER",
    },
    "ITRY": {
        "description": "Set limit of number of SCF iterations to n",
        "takes values": 1,
        "default": "2000",
        "format": "{}={}",
    },
    "IUPD": {
        "description": (
            "Mode of Hessian update in eigenvector following: "
            "0: skip, 1: Powell, 2: BFGS"
        ),
        "takes values": 1,
        "default": "2",
        "format": "{}={}",
        "allowed values": (0, 1, 2),
    },
    "KINETIC": {
        "description": "Excess kinetic energy added to DRC calculation",
        "takes values": 1,
        "default": 20,
        "format": "{}={}",
    },
    "KING": {
        "description": "Use Camp-King converger for SCF",
    },
    "LARGE": {
        "description": "Print expanded output",
    },
    "LBFGS": {
        "description": "Use the low-memory version of the BFGS optimizer",
    },
    "LET": {
        "description": "Override certain safety checks",
    },
    "LEWIS": {
        "description": "Print the Lewis structure",
    },
    "LINMIN": {
        "description": "Print details of line minimization",
    },
    "LOCALIZE": {
        "description": (
            "Print the localized orbitals. These are also called "
            "Natural Bond Orbitals or NBO"
        ),
    },
    "LOCATE-TS": {
        "description": (
            "Given reactants and products, locate the transition "
            "state connecting them"
        ),
    },
    "LOG": {
        "description": "Generate a log file",
    },
    "MECI": {
        "description": "Print details of MECI calculation",
    },
    "MERS=(n1,n2,n3)": {
        "description": "Keyword generated by MAKPOL for use with program BZ",
        "takes values": [1, 2, 3],
        "default": "(n1[,n2[,n3]])",
        "format": "{}={}",
    },
    "METAL": {
        "description": "Make specified atoms 100% ionic",
        "takes values": "0+",
        "default": "(Au(+3),Fe)",
        "format": "{}={}",
    },
    "MICROS": {
        "description": "Use specific microstates in the C.I.",
        "takes values": 1,
        "default": "1",
        "format": "{}={}",
    },
    "MINI": {
        "description": (
            "Reduce the size of the output by only printing " "specified atoms"
        ),
    },
    "MINMEP": {
        "description": "Minimize MEP minima in the plane defined",
    },
    "MMOK": {
        "description": "Use molecular mechanics correction to CONH bonds",
    },
    "MNDO": {
        "description": "Use the MNDO hamiltonian",
    },
    "MNDOD": {"description": "Use the MNDO-d hamiltonian"},
    "MODE": {
        "description": "In EF, follow Hessian mode no. n",
        "takes values": 1,
        "default": 1,
        "format": "{}={}",
    },
    "MOL_QMMM": {
        "description": ("Incorporate environmental effects in the QM/MM " "approach"),
    },
    "MOLDAT": {
        "description": "Print details of working in MOLDAT",
    },
    "MOLSYM": {
        "description": "Print details of working in MOLSYM",
    },
    "MOPAC": {
        "description": "Use old MOPAC definition for 2nd and 3rd atoms",
    },
    "MOZYME": {
        "description": (
            "Use the Localized Molecular Orbital method to speed " "up the SCF"
        ),
    },
    "MS": {
        "description": "In MECI, magnetic component of spin",
        "takes values": 1,
        "default": "1.5",
        "format": "{}={}",
        "allowed value test": "2*value",
    },
    "MULLIK": {
        "description": "Print the Mulliken population analysis",
    },
    "N**2": {
        "description": (
            "In excited state COSMO calculations, set the value " "of N**2"
        ),
        "takes values": 1,
        "default": 2,
        "format": "{}={}",
    },
    "NLLSQ": {
        "description": "Minimize gradients using NLLSQ",
    },
    "NOANCI": {
        "description": "Do not use analytical C.I. derivatives",
    },
    "NOCOMMENTS": {
        "description": (
            "Ignore all lines except ATOM, HETATM, and TER in PDB " "files"
        ),
    },
    "NOGPU": {
        "description": "Do not use GPU acceleration",
    },
    "NOLOG": {
        "description": "Suppress log file trail, where possible",
    },
    "NOMM": {
        "description": ("Do not use molecular mechanics correction to CONH " "bonds"),
    },
    "NONET": {
        "description": "NONET state required",
    },
    "NONR": {
        "description": "Do not use Newton-Raphson method in EF",
    },
    "NOOPT": {
        "description": ("Do not optimize the coordinates of all atoms " "(see OPT-X)"),
    },
    "NOOPT-X": {
        "description": ("Do not optimize the coordinates of all atoms of type " "X"),
    },
    "NOREOR": {
        "description": "In symmetry work, use supplied orientation",
    },
    "NORESEQ": {
        "description": (
            "Suppress the default re-sequencing of atoms to the " "PDB sequence"
        ),
    },
    "NOSWAP": {
        "description": "Do not allow atom swapping when GEO_REF is used",
    },
    "NOSYM": {
        "description": "Point-group symmetry set to C1",
    },
    "NOTER": {
        "description": 'Do not put "TER"s in PDB files',
    },
    "NOTHIEL": {
        "description": "Do not use Thiel's FSTMIN technique",
    },
    "NOTXT": {
        "description": "Remove any text from atom symbols",
    },
    "NOXYZ": {
        "description": "Do not print Cartesian coordinates",
    },
    "NSPA": {
        "description": (
            "Sets number of geometric segments in COSMO " "use 42, 92, 122 or 162"
        ),
        "takes values": 1,
        "default": 42,
        "format": "{}={}",
    },
    "NSURF": {
        "description": "Number of surfaces in an ESP calculation",
    },
    "OCTET": {
        "description": "Octet state required",
    },
    "OLDCAV": {
        "description": (
            "In COSMO, use the old Solvent Accessible Surface " "calculation"
        ),
    },
    "OLDENS": {
        "description": "Read initial density matrix off disk",
    },
    "OLDFPC": {
        "description": "Use the old fundamental physical constants",
    },
    "OLDGEO": {
        "description": "Previous geometry to be used",
    },
    "OMIN=n.nn": {
        "description": "In TS, minimum allowed overlap of eigenvectors",
        "takes values": 1,
        "default": 0.8,
        "format": "{}={}",
    },
    "OPEN": {
        "description": "Open-shell UHF or RHF calculation requested",
        "takes values": 2,
        "default": "(2,2)",
        "format": "{}{}",
    },
    "OPT": {
        "description": (
            "OPT: Optimize coordinates of all atoms -- or --"
            "OPT(text=n.nn): Optimize the coordinates of all atoms within"
            'n.nn Ångstroms of atoms labeled "text" -- or --'
            'OPT("Label1"[,"Label1"[,"Label1"...]]) where labels are residues'
        ),
        "takes values": [0, 1],
        "default": "",
        "format": "OPT({value})",
    },
    "OPT-X": {
        "description": "Optimize the coordinates of all atoms of type X",
        "takes values": 1,
        "default": "H",
        "format": "OPT-X={value}",
    },
    "OUTPUT": {
        "description": ("Reduce the amount of output (useful for large " "systems)"),
    },
    "P": {
        "description": (
            "An applied pressure of n.nn Newtons/m2 to be used"
            " A suffix of GPa may be used to indicate GPa=10^9 "
            "N/m^2"
        ),
        "takes values": 1,
        "default": "10.0GPa",
        "format": "{}={}",
    },
    "PDB": {
        "description": (
            "Input geometry is in protein data bank format. "
            "Arguments give nonstandard element name:atno, e.g. "
            "D:1 or LP:0"
        ),
        "takes values": 1,
        "default": "(D:1,LP:0)",
        "format": "{}{}",
    },
    "PDBOUT	": {
        "description": "Output geometry in pdb format",
    },
    "PECI": {
        "description": "C.I. involves paired excitations only",
    },
    "PI": {
        "description": "Resolve density matrix into σ, π, and δ components",
    },
    "pKa": {
        "description": (
            "Print the pKa for ionizable hydrogen atoms attached " "to oxygen atoms"
        ),
    },
    "PL": {
        "description": "Monitor convergence of density matrix in ITER",
    },
    "PM3": {
        "description": "Use the MNDO-PM3 Hamiltonian",
    },
    "PM6": {"description": "Use the PM6 Hamiltonian"},
    "PM6-D3": {
        "description": (
            "Use the PM6 Hamiltonian with Grimme's corrections " "for dispersion"
        ),
    },
    "PM6-DH+": {
        "description": (
            "Use the PM6 Hamiltonian with corrections for "
            "dispersion and hydrogen-bonding"
        ),
    },
    "PM6-DH2": {
        "description": (
            "Use the PM6 Hamiltonian with corrections for "
            "dispersion and hydrogen-bonding"
        ),
    },
    "PM6-DH2X": {
        "description": (
            "Use PM6 with corrections for dispersion and hydrogen "
            "and halogen bonding"
        ),
    },
    "PM6-D3H4": {
        "description": "Use PM6 with Řezáč and Hobza's D3H4 correction",
    },
    "PM6-D3H4X": {
        "description": ("Use PM6 with Brahmkshatriya, et al.'s D3H4X " "correction"),
    },
    "PMEP": {
        "description": "Complete semiempirical MEP calculation",
    },
    "PM7": {
        "description": "Use the PM7 Hamiltonian",
    },
    "PM7-TS": {
        "description": "Use the PM7-TS Hamiltonian (only for barrier heights)",
    },
    "PMEPR": {
        "description": "Complete semiempirical MEP in a plane to be defined",
    },
    "POINT": {
        "description": "Number of points in reaction path",
        "takes values": 1,
        "default": "40",
        "format": "{}={}",
    },
    "POINT1": {
        "description": ("Number of points in first direction in grid " "calculation"),
        "takes values": 1,
        "default": "11",
        "format": "{}={}",
    },
    "POINT2": {
        "description": ("Number of points in second direction in grid " "calculation"),
        "takes values": 1,
        "default": "11",
        "format": "{}={}",
    },
    "POLAR": {
        "description": ("Calculate first, second and third order " "polarizabilities"),
    },
    "POTWRT": {
        "description": "In ESP, write out electrostatic potential to unit 21",
    },
    "POWSQ": {
        "description": "Print details of working in POWSQ",
    },
    "PRECISE": {
        "description": "Criteria to be increased by 100 times",
    },
    "PRESSURE": {
        "description": "Apply pressure or tension to a solid or polymer",
    },
    "PRNT": {
        "description": (
            "Print details of geometry optimization in EF, 1 = " "most, 5=least"
        ),
        "takes values": 1,
        "default": 1,
        "format": "{}={}",
        "allowed values": (0, 1, 2, 3, 4, 5),
    },
    "PRTCHAR": {
        "description": "Print charges in ARC file",
    },
    "PRTINT": {
        "description": "Print interatomic distances",
    },
    "PRTMEP": {
        "description": "MEP contour data output to <filename>.mep",
    },
    "PRTXYZ": {
        "description": "Print Cartesian coordinates",
    },
    "PULAY": {
        "description": "Use Pulay's converger to obtain a SCF",
    },
    "QMMM": {
        "description": ("Incorporate environmental effects in the QM/MM " "approach"),
    },
    "QPMEP": {
        "description": "Charges derived from Wang-Ford type AM1 MEP",
    },
    "QUARTET": {
        "description": "Quartet state required",
    },
    "QUINTET": {
        "description": "Quintet state required",
    },
    "RAPID": {
        "description": (
            "In MOZYME geometry optimizations, only use atoms "
            "being optimized in the SCF"
        ),
    },
    "RECALC": {
        "description": "In EF, recalculate Hessian every n steps",
        "takes values": 1,
        "default": 10,
        "format": "{}={}",
    },
    "RE-LOCAL": {
        "description": (
            "During and at end of a MOZYME calculation, "
            "re-localize the LMOs. Default is just at end."
        ),
        "takes values": [0, 1],
        "default": 1,
        "format": "{}={}",
    },
    "RELSCF": {
        "description": "Default SCF criterion multiplied by n",
    },
    "REORTHOG": {
        "description": (
            "In MOZYME, re-orthogonalize LMO's each 10 SCF " "calculations."
        ),
    },
    "RESEQ": {
        "description": "Re-arrange the atoms to match the PDB convention",
    },
    "RESIDUES": {
        "description": (
            "Label each atom in a polypeptide with the amino acid " "residue."
        ),
    },
    "RESTART": {
        "description": "Calculation restarted",
    },
    "RHF": {
        "description": "Use Restricted Hartree-Fock methods",
    },
    "RM1": {
        "description": "Use the RM1 Hamiltonian",
    },
    "RMAX": {
        "description": "In TS, maximum allowed ratio for energy change",
        "takes values": 1,
        "default": 4.0,
        "format": "{}={}",
    },
    "RMIN": {
        "description": "In TS, minimum allowed ratio for energy change",
        "takes values": 1,
        "default": 0.0,
        "format": "{}={}",
    },
    "ROOT": {
        "description": (
            "Root n to be optimized in a C.I. calculation. "
            "Either an integer or with a symmetry label, e.g."
            "2T2g"
        ),
        "takes values": 1,
        "default": "1",
        "format": "{}={}",
    },
    "RSCAL": {
        "description": "In EF, scale p-RFO to trust radius",
    },
    "RSOLV=n.nn": {
        "description": "Effective radius of solvent in COSMO",
    },
    "SADDLE": {
        "description": "Optimize transition state",
    },
    "SCALE": {
        "description": "Scaling factor for van der waals distance in ESP",
    },
    "SCFCRT=n.nn": {
        "description": "Default SCF criterion replaced by the value supplied",
    },
    "SCINCR=n.nn": {
        "description": "Increment between layers in ESP",
    },
    "SEPTET": {
        "description": "Septet state required",
    },
    "SETPI": {
        "description": ("In MOZYME, some π bonds are explicitly set by the " "user"),
    },
    "SETUP": {
        "description": "Extra keywords to be read from setup file",
    },
    "SEXTET": {
        "description": "Sextet state required",
    },
    "SHIFT=n.nn": {
        "description": "a damping factor of n defined to start SCF",
    },
    # 'SHUT <file>': {
    #     'description': ('Send a command to MOPAC to make a restart and '
    #                     'density file, then stop.'),
    # },
    "SIGMA": {
        "description": "Minimize gradients using SIGMA",
    },
    "SINGLET": {
        "description": "Singlet state required",
    },
    "SITE=(text)": {
        "description": "Define ionization state of residues in proteins",
    },
    "SLOG=n.nn": {
        "description": ("In L-BFGS optimization, use fixed step of length " "n .nn"),
    },
    "SLOPE": {
        "description": "Multiplier used to scale MNDO charges",
    },
    "SMOOTH": {
        "description": (
            "In a GRID calculation, remove artifacts caused by "
            "the order in which points are calculated"
        ),
    },
    "SNAP": {
        "description": "Increase precision of symmetry angles",
    },
    "SPARKLE": {
        "description": "Use sparkles instead of atoms with basis sets",
    },
    "SPIN": {
        "description": "Print final UHF spin matrix",
    },
    "START_RES(text)": {
        "description": (
            "Define starting residue numbers in a protein, if "
            "different from the default"
        ),
    },
    "STATIC": {
        "description": "Calculate Polarizability using electric fields",
    },
    "STEP": {
        "description": "Step size in path",
    },
    "STEP1=n.nnn": {
        "description": "Step size n for first coordinate in grid calculation",
    },
    "STEP2=n.nnn": {
        "description": "Step size n for second coordinate in grid calculation",
    },
    "STO3G": {
        "description": "Deorthogonalize orbitals in STO-3G basis",
    },
    "SUPER": {
        "description": "Print superdelocalizabilities",
    },
    "SYBYL": {
        "description": "Output a file for use by Tripos's SYBYL program",
    },
    "SYMAVG": {
        "description": "Average symmetry equivalent ESP charges",
    },
    "SYMOIR": {
        "description": (
            "Print characters of eigenvectors and print number of " "I.R.s"
        ),
    },
    "SYMTRZ": {
        "description": "Print details of working in subroutine SYMTRZ.",
    },
    "SYMMETRY": {
        "description": "Impose symmetry conditions",
    },
    "T=n[M,H,D]": {
        "description": "A time of n seconds requested",
    },
    "THERMO(nnn,mmm,lll)": {
        "description": "Perform a thermodynamics calculation",
    },
    "THREADS=n": {
        "description": (
            "Set the number of threads to be used in " "parallelization to n"
        ),
    },
    "TIMES": {
        "description": "Print times of various stages",
    },
    "T-PRIORITY=n.nn": {
        "description": "Time takes priority in DRC",
    },
    "TRANS=n": {
        "description": (
            "The system is a transition state (used in " "thermodynamics calculation)"
        ),
    },
    "TRIPLET": {
        "description": "Triplet state required",
    },
    "TS": {
        "description": "Using EF routine for TS search",
    },
    "UHF": {
        "description": "Use the Unrestricted Hartree-Fock method",
    },
    "VDW(text)": {
        "description": ("Van der waals radius for atoms in COSMO defined by " "user"),
    },
    "VDWM(text)": {
        "description": ("Van der waals radius for atoms in MOZYME defined by " "user"),
    },
    "VECTORS": {
        "description": "Print final eigenvectors",
    },
    "VELOCITY": {
        "description": ("Supply the initial velocity vector in a DRC " "calculation"),
    },
    "WILLIAMS": {
        "description": "Use Williams surface",
    },
    "X-PRIORITY=n.nn": {
        "description": "Geometry changes take priority in DRC",
    },
    "XENO": {
        "description": ("Allow non-standard residues in proteins to be " "labeled."),
    },
    "XYZ": {
        "description": "Do all geometric operations in Cartesian coordinates",
    },
    "Z=n": {
        "description": "Number of mers in a cluster",
    },
}

"""Descriptions of the results of MOPAC calculations.

Fields
------
calculation : [str]
    The types of calculation that can create this data.
description : str
    A short human-readable name for the item.
dimensionality : "scalar" or [int|str]
    Either "scalar" of a list of integer or strings (for variables) for the size of the
    item in each dimension.
property : str
    An optional standard name for the item in the database warehouse.
type : "integer", "float", or "string"
    The type of the value.
units : str
    An optional unit string for the value as returned by the code.
"""
metadata["results"] = {
    "energy": {
        "calculation": [
            "energy",
            "optimization",
            "thermodynamics",
            "vibrations",
            "force constants",
        ],
        "description": "enthalpy of formation",
        "dimensionality": "scalar",
        "type": "float",
        "units": "kcal/mol",
    },
    "gradients": {
        "calculation": [
            "energy",
            "optimization",
            "thermodynamics",
            "vibrations",
            "force constants",
        ],
        "description": "gradients on the atoms",
        "dimensionality": [3, "n_atoms"],
        "type": "float",
        "units": "kcal/mol/Å",
    },
    "force constants": {
        "calculation": ["thermodynamics", "vibrations", "force constants"],
        "description": "the Cartesian force constants",
        "dimensionality": "[natoms*(natoms+1)]",
        "property": "force constants#MOPAC#{model}",
        "type": "float",
        "units": "kcal/mol/Å^2",
        "format": ".2f",
    },
    "ERROR_MESSAGE": {
        "description": "An error message",
        "dimensionality": "scalar",
        "type": "string",
    },
    "AO_ATOMINDEX": {
        "calculation": [
            "energy",
            "optimization",
            "thermodynamics",
            "vibrations",
            "force constants",
        ],
        "description": "atom for AO",
        "dimensionality": ["n_aos"],
        "type": "integer",
    },
    "AO_CHARGES": {
        "calculation": [
            "energy",
            "optimization",
            "thermodynamics",
            "vibrations",
            "force constants",
        ],
        "description": "electrons in the AOs",
        "dimensionality": ["n_aos"],
        "type": "float",
    },
    "AO_SPINS": {
        "calculation": [
            "energy",
            "optimization",
            "thermodynamics",
            "vibrations",
            "force constants",
        ],
        "description": "spins in the AOs",
        "dimensionality": ["n_aos"],
        "type": "float",
    },
    "AO_ZETA": {
        "calculation": [
            "energy",
            "optimization",
            "thermodynamics",
            "vibrations",
            "force constants",
        ],
        "description": "Slater exponent",
        "dimensionality": ["n_aos"],
        "type": "float",
    },
    "AREA": {
        "calculation": [
            "energy",
            "optimization",
            "thermodynamics",
            "vibrations",
            "force constants",
        ],
        "description": "surface area",
        "dimensionality": "scalar",
        "property": "surface area#MOPAC#{model}",
        "type": "float",
        "units": "Å^2",
    },
    "ATOM_CHARGES": {
        "calculation": [
            "energy",
            "optimization",
            "thermodynamics",
            "vibrations",
            "force constants",
        ],
        "description": "atom charges",
        "dimensionality": ["n_atoms"],
        "type": "float",
    },
    "ATOM_CORE": {
        "calculation": [
            "energy",
            "optimization",
            "thermodynamics",
            "vibrations",
            "force constants",
        ],
        "description": "number of valence electrons",
        "dimensionality": ["n_atoms"],
        "type": "integer",
    },
    "ATOM_EL": {
        "calculation": [
            "energy",
            "optimization",
            "thermodynamics",
            "vibrations",
            "force constants",
        ],
        "description": "atomic symbol",
        "dimensionality": ["n_atoms"],
        "type": "string",
    },
    "ATOM_PQN": {
        "calculation": [
            "energy",
            "optimization",
            "thermodynamics",
            "vibrations",
            "force constants",
        ],
        "description": "principal quantum number",
        "dimensionality": ["n_aos"],
        "type": "integer",
    },
    "ATOM_SYMTYPE": {
        "calculation": [
            "energy",
            "optimization",
            "thermodynamics",
            "vibrations",
            "force constants",
        ],
        "description": "atomic orbital angular shape",
        "dimensionality": ["n_aos"],
        "type": "string",
    },
    "ATOM_X": {
        "calculation": [
            "energy",
            "optimization",
            "thermodynamics",
            "vibrations",
            "force constants",
        ],
        "description": "x, y, z coordinates",
        "dimensionality": [3, "n_atoms"],
        "type": "float",
        "units": "Å",
    },
    "ATOM_X_FORCE": {
        "calculation": ["thermodynamics", "vibrations", "force constants"],
        "description": "reoriented coordinates",
        "dimensionality": [3, "n_atoms"],
        "type": "float",
        "units": "Å",
    },
    "ATOM_X_OPT": {
        "calculation": [
            "optimization",
            "thermodynamics",
            "vibrations",
            "force constants",
        ],
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
    "BOND_ORDERS": {
        "calculation": [
            "energy",
            "optimization",
            "thermodynamics",
            "vibrations",
            "force constants",
        ],
        "description": "bond order matrix",
        "dimensionality": ["triangular", "n_atoms", "n_atoms"],
        "type": "float",
    },
    "COMMENTS": {
        "calculation": [],
        "description": "User comment line",
        "dimensionality": "scalar",
        "type": "string",
    },
    "CPU_TIME": {
        "calculation": [
            "energy",
            "optimization",
            "thermodynamics",
            "vibrations",
            "force constants",
        ],
        "description": "cpu time for calculation",
        "dimensionality": "scalar",
        "type": "float",
        "units": "s",
    },
    "DATE": {
        "calculation": [
            "energy",
            "optimization",
            "thermodynamics",
            "vibrations",
            "force constants",
        ],
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
        "calculation": [
            "energy",
            "optimization",
            "thermodynamics",
            "vibrations",
            "force constants",
        ],
        "description": "dipole moment",
        "dimensionality": "scalar",
        "property": "dipole moment#MOPAC#{model}",
        "type": "float",
        "units": "debye",
    },
    "DIP_VEC": {
        "calculation": [
            "energy",
            "optimization",
            "thermodynamics",
            "vibrations",
            "force constants",
        ],
        "description": "dipole vector",
        "dimensionality": [3],
        "type": "float",
        "units": "debye",
    },
    "EIGENVALUES": {
        "calculation": [
            "energy",
            "optimization",
            "thermodynamics",
            "vibrations",
            "force constants",
        ],
        "description": "orbital energies",
        "dimensionality": ["n_aos"],
        "type": "float",
        "units": "eV",
    },
    "ALPHA_EIGENVALUES": {
        "calculation": [
            "energy",
            "optimization",
            "thermodynamics",
            "vibrations",
            "force constants",
        ],
        "description": "orbital energies",
        "dimensionality": ["n_aos"],
        "type": "float",
        "units": "eV",
    },
    "BETA_EIGENVALUES": {
        "calculation": [
            "energy",
            "optimization",
            "thermodynamics",
            "vibrations",
            "force constants",
        ],
        "description": "orbital energies",
        "dimensionality": ["n_aos"],
        "type": "float",
        "units": "eV",
    },
    "LMO_ENERGY_LEVELS": {
        "calculation": [
            "energy",
            "optimization",
            "thermodynamics",
            "vibrations",
            "force constants",
        ],
        "description": "Localized MO energies",
        "dimensionality": ["n_aos"],
        "type": "float",
        "units": "eV",
    },
    "EIGENVECTORS": {
        "calculation": [
            "energy",
            "optimization",
            "thermodynamics",
            "vibrations",
            "force constants",
        ],
        "description": "orbital coefficients",
        "dimensionality": ["n_aos"],
        "type": "float",
    },
    "ALPHA_EIGENVECTORS": {
        "calculation": [
            "energy",
            "optimization",
            "thermodynamics",
            "vibrations",
            "force constants",
        ],
        "description": "orbital coefficients",
        "dimensionality": ["n_aos"],
        "type": "float",
    },
    "BETA_EIGENVECTORS": {
        "calculation": [
            "energy",
            "optimization",
            "thermodynamics",
            "vibrations",
            "force constants",
        ],
        "description": "orbital coefficients",
        "dimensionality": ["n_aos"],
        "type": "float",
    },
    "LMO_VECTORS": {
        "calculation": [
            "energy",
            "optimization",
            "thermodynamics",
            "vibrations",
            "force constants",
        ],
        "description": "localized molecular orbital coefficients",
        "dimensionality": ["n_aos"],
        "type": "float",
    },
    "EMPIRICAL_FORMULA": {
        "calculation": [
            "energy",
            "optimization",
            "thermodynamics",
            "vibrations",
            "force constants",
        ],
        "description": "empirical formula",
        "dimensionality": "scalar",
        "type": "string",
    },
    "ENERGY_ELECTRONIC": {
        "calculation": [
            "energy",
            "optimization",
            "thermodynamics",
            "vibrations",
            "force constants",
        ],
        "description": "electronic energy",
        "dimensionality": "scalar",
        "property": "electronic energy#MOPAC#{model}",
        "type": "float",
        "units": "eV",
    },
    "ENERGY_NUCLEAR": {
        "calculation": [
            "energy",
            "optimization",
            "thermodynamics",
            "vibrations",
            "force constants",
        ],
        "description": "nuclear repulsion energy",
        "dimensionality": "scalar",
        "property": "nuclear repulsion energy",
        "type": "float",
        "units": "eV",
    },
    "DIEL_ENER": {
        "calculation": [
            "energy",
            "optimization",
            "thermodynamics",
            "vibrations",
            "force constants",
        ],
        "description": "the dielectric energy from COSMO",
        "dimensionality": "scalar",
        "property": "dielectric energy#MOPAC#{model}",
        "type": "float",
        "units": "eV",
    },
    "ENTHALPY_TOT": {
        "calculation": ["thermodynamics", "vibrations", "force constants"],
        "description": "enthalpy",
        "dimensionality": [
            "n_temps",
        ],
        "type": "float",
        "units": "cal/mol",
    },
    "ENTROPY_TOT": {
        "calculation": ["thermodynamics", "vibrations", "force constants"],
        "description": "entropy",
        "dimensionality": [
            "n_temps",
        ],
        "type": "float",
        "units": "cal/K/mol",
    },
    "GRADIENTS": {
        "calculation": [
            "energy",
            "optimization",
            "thermodynamics",
            "vibrations",
            "force constants",
        ],
        "description": "gradients on the atoms",
        "dimensionality": [3, "n_atoms"],
        "type": "float",
        "units": "kcal/mol/Å",
    },
    "GRADIENT_NORM": {
        "calculation": [
            "optimization",
            "thermodynamics",
            "vibrations",
            "force constants",
        ],
        "description": "final norm of the gradient",
        "dimensionality": "scalar",
        "type": "float",
        "units": "kcal/mol/Å",
    },
    "GRADIENT_NORM_UPDATED": {
        "calculation": ["optimization"],
        "description": "current norm of the gradient",
        "dimensionality": "scalar",
        "type": "float",
        "units": "kcal/mol/Å",
    },
    "GRADIENTS_UPDATED": {
        "calculation": ["optimization"],
        "description": "forces in trajectory",
        "dimensionality": ["nsteps", [3, "n_atoms"]],
        "type": "float",
        "units": "kcal/mol/Å",
    },
    "VOIGT_STRESS": {
        "description": "Voigt stress",
        "dimensionality": [6],
        "type": "float",
        "units": "GPa",
    },
    "VOIGT_STRESS_UPDATED": {
        "description": "Voigt stress in trajectory",
        "dimensionality": [6],
        "type": "float",
        "units": "GPa",
    },
    "HEAT_CAPACITY_TOT": {
        "calculation": ["thermodynamics", "vibrations", "force constants"],
        "description": "heat capacity",
        "dimensionality": [
            "n_temps",
        ],
        "type": "float",
        "units": "cal/K/mol",
    },
    "HEAT_OF_FORMATION": {
        "calculation": [
            "energy",
            "optimization",
            "thermodynamics",
            "vibrations",
            "force constants",
        ],
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
        "calculation": ["thermodynamics", "vibrations", "force constants"],
        "description": "Hessian matrix",
        "dimensionality": ["n_dof", "n_dof"],
        "type": "float",
        "units": "mdyne/Å/Da",
    },
    "H_O_F(T)": {
        "calculation": ["thermodynamics", "vibrations", "force constants"],
        "description": "enthalpy of formation vs T",
        "dimensionality": ["n_temps"],
        "type": "float",
        "units": "kcal/mol",
    },
    "INT_FORCE_CONSTS": {
        "calculation": ["thermodynamics", "vibrations", "force constants"],
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
        "calculation": [
            "energy",
            "optimization",
            "thermodynamics",
            "vibrations",
            "force constants",
        ],
        "description": "ionization energy (IE)",
        "dimensionality": "scalar",
        "property": "ionization energy#MOPAC#{model}",
        "type": "float",
        "units": "eV",
    },
    "ISOTOPIC_MASSES": {
        "calculation": ["thermodynamics", "vibrations", "force constants"],
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
        "calculation": [
            "energy",
            "optimization",
            "thermodynamics",
            "vibrations",
            "force constants",
        ],
        "description": "molecular orbital symmetries",
        "dimensionality": ["n_mos"],
        "type": "string",
    },
    "ALPHA_M.O.SYMMETRY_LABELS": {
        "calculation": [
            "energy",
            "optimization",
            "thermodynamics",
            "vibrations",
            "force constants",
        ],
        "description": "molecular orbital symmetries",
        "dimensionality": ["n_mos"],
        "type": "string",
    },
    "BETA_M.O.SYMMETRY_LABELS": {
        "calculation": [
            "energy",
            "optimization",
            "thermodynamics",
            "vibrations",
            "force constants",
        ],
        "description": "molecular orbital symmetries",
        "dimensionality": ["n_mos"],
        "type": "string",
    },
    "METHOD": {
        "calculation": [
            "energy",
            "optimization",
            "thermodynamics",
            "vibrations",
            "force constants",
        ],
        "description": "hamiltonian",
        "dimensionality": "scalar",
        "type": "string",
    },
    "MOLECULAR_ORBITAL_OCCUPANCIES": {
        "calculation": [
            "energy",
            "optimization",
            "thermodynamics",
            "vibrations",
            "force constants",
        ],
        "description": "orbital occupancies",
        "dimensionality": ["n_mos"],
        "type": "float",
    },
    "ALPHA_MOLECULAR_ORBITAL_OCCUPANCIES": {
        "calculation": [
            "energy",
            "optimization",
            "thermodynamics",
            "vibrations",
            "force constants",
        ],
        "description": "orbital occupancies",
        "dimensionality": ["n_mos"],
        "type": "float",
    },
    "BETA_MOLECULAR_ORBITAL_OCCUPANCIES": {
        "calculation": [
            "energy",
            "optimization",
            "thermodynamics",
            "vibrations",
            "force constants",
        ],
        "description": "orbital occupancies",
        "dimensionality": ["n_mos"],
        "type": "float",
    },
    "MOLECULAR_WEIGHT": {
        "calculation": [
            "energy",
            "optimization",
            "thermodynamics",
            "vibrations",
            "force constants",
        ],
        "description": "molecular weight",
        "dimensionality": "scalar",
        "type": "float",
        "units": "Da",
    },
    "MOPAC_VERSION": {
        "calculation": [
            "energy",
            "optimization",
            "thermodynamics",
            "vibrations",
            "force constants",
        ],
        "description": "MOPAC version",
        "dimensionality": "scalar",
        "type": "string",
    },
    "NORMAL_MODES": {
        "calculation": ["thermodynamics", "vibrations", "force constants"],
        "description": "normal modes",
        "dimensionality": ["n_dof", "n_dof"],
        "type": "float",
    },
    "NORMAL_MODE_SYMMETRY_LABELS": {
        "calculation": ["thermodynamics", "vibrations", "force constants"],
        "description": "symmetry labels of normal modes",
        "dimensionality": ["n_dof"],
        "type": "string",
    },
    "NUMBER_SCF_CYCLES": {
        "calculation": [
            "energy",
            "optimization",
            "thermodynamics",
            "vibrations",
            "force constants",
        ],
        "description": "number of scf's",
        "dimensionality": "scalar",
        "type": "integer",
    },
    "NUM_ALPHA_ELECTRONS": {
        "calculation": [
            "energy",
            "optimization",
            "thermodynamics",
            "vibrations",
            "force constants",
        ],
        "description": "number of spin-up electrons",
        "dimensionality": "scalar",
        "type": "integer",
    },
    "NUM_BETA_ELECTRONS": {
        "calculation": [
            "energy",
            "optimization",
            "thermodynamics",
            "vibrations",
            "force constants",
        ],
        "description": "number of spin-down electrons",
        "dimensionality": "scalar",
        "type": "integer",
    },
    "NUM_ELECTRONS": {
        "calculation": [
            "energy",
            "optimization",
            "thermodynamics",
            "vibrations",
            "force constants",
        ],
        "description": "number of electrons",
        "dimensionality": "scalar",
        "type": "integer",
    },
    "ORIENTATION_ATOM_X": {
        "calculation": ["thermodynamics", "vibrations", "force constants"],
        "description": "",
        "dimensionality": [3, "n_atoms"],
        "type": "float",
        "units": "Å",
    },
    "OVERLAP_MATRIX": {
        "calculation": [
            "energy",
            "optimization",
            "thermodynamics",
            "vibrations",
            "force constants",
        ],
        "description": "the AO overlap matrix",
        "dimensionality": ["triangular", "n_aos", "n_aos"],
        "type": "float",
    },
    "DENSITY_MATRIX": {
        "calculation": [
            "energy",
            "optimization",
            "thermodynamics",
            "vibrations",
            "force constants",
        ],
        "description": "the density matrix",
        "dimensionality": ["triangular", "n_aos", "n_aos"],
        "type": "float",
    },
    "POINT_GROUP": {
        "calculation": [
            "energy",
            "optimization",
            "thermodynamics",
            "vibrations",
            "force constants",
        ],
        "description": "the molecular symmetry",
        "dimensionality": "scalar",
        "type": "string",
    },
    "PRI_MOM_OF_I": {
        "calculation": ["thermodynamics", "vibrations", "force constants"],
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
        "calculation": ["thermodynamics", "vibrations", "force constants"],
        "description": "rotational constants",
        "dimensionality": [3],
        "type": "float",
        "units": "1/cm",
    },
    "SET_OF_MOS": {
        "calculation": [
            "energy",
            "optimization",
            "thermodynamics",
            "vibrations",
            "force constants",
        ],
        "description": "set of MOs",
        "dimensionality": [2],
        "type": "string",
    },
    "SET_OF_ALPHA_MOS": {
        "calculation": [
            "energy",
            "optimization",
            "thermodynamics",
            "vibrations",
            "force constants",
        ],
        "description": "set of MOs",
        "dimensionality": [2],
        "type": "string",
    },
    "SET_OF_BETA_MOS": {
        "calculation": [
            "energy",
            "optimization",
            "thermodynamics",
            "vibrations",
            "force constants",
        ],
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
        "calculation": [
            "energy",
            "optimization",
            "thermodynamics",
            "vibrations",
            "force constants",
        ],
        "description": "spin component",
        "dimensionality": [3],
        "type": "float",
    },
    "THERMODYNAMIC_PROPERTIES_TEMPS": {
        "calculation": ["thermodynamics", "vibrations", "force constants"],
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
        "calculation": [
            "energy",
            "optimization",
            "thermodynamics",
            "vibrations",
            "force constants",
        ],
        "description": "density matrix",
        "dimensionality": ["n_mos", "n_mos"],
        "shape": "triangular",
        "type": "float",
    },
    "ALPHA_DENSITY_MATRIX": {
        "calculation": [
            "energy",
            "optimization",
            "thermodynamics",
            "vibrations",
            "force constants",
        ],
        "description": "density matrix",
        "dimensionality": ["n_mos", "n_mos"],
        "shape": "triangular",
        "type": "float",
    },
    "BETA_DENSITY_MATRIX": {
        "calculation": [
            "energy",
            "optimization",
            "thermodynamics",
            "vibrations",
            "force constants",
        ],
        "description": "density matrix",
        "dimensionality": ["n_mos", "n_mos"],
        "shape": "triangular",
        "type": "float",
    },
    "TOTAL_ENERGY": {
        "calculation": [
            "energy",
            "optimization",
            "thermodynamics",
            "vibrations",
            "force constants",
        ],
        "description": "total energy",
        "dimensionality": "scalar",
        "property": "total energy#MOPAC#{model}",
        "type": "float",
        "units": "eV",
    },
    "HOMO Energy": {
        "calculation": [
            "energy",
            "optimization",
            "thermodynamics",
            "vibrations",
            "force constants",
        ],
        "description": "energy of the HOMO",
        "dimensionality": "scalar",
        "property": "HOMO energy#MOPAC#{model}",
        "type": "float",
        "units": "eV",
    },
    "LUMO Energy": {
        "calculation": [
            "energy",
            "optimization",
            "thermodynamics",
            "vibrations",
            "force constants",
        ],
        "description": "energy of the LUMO",
        "dimensionality": "scalar",
        "property": "LUMO energy#MOPAC#{model}",
        "type": "float",
        "units": "eV",
    },
    "HOMO-LUMO Gap": {
        "calculation": [
            "energy",
            "optimization",
            "thermodynamics",
            "vibrations",
            "force constants",
        ],
        "description": "The energy of the HOMO-LUMO gap",
        "dimensionality": "scalar",
        "property": "band gap#MOPAC#{model}",
        "type": "float",
        "units": "eV",
    },
    "TOTAL_SPIN": {
        "calculation": [
            "energy",
            "optimization",
            "thermodynamics",
            "vibrations",
            "force constants",
        ],
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
        "calculation": ["thermodynamics", "vibrations", "force constants"],
        "description": "vibrational effective masses",
        "dimensionality": ["n_dof"],
        "type": "float",
        "units": "Da",
    },
    "VIB._FREQ": {
        "calculation": ["thermodynamics", "vibrations", "force constants"],
        "description": "vibrational frequencies",
        "dimensionality": ["n_dof"],
        "type": "float",
        "units": "1/cm",
    },
    "VIB._RED_MASS": {
        "calculation": ["thermodynamics", "vibrations", "force constants"],
        "description": "vibrational reduced masses",
        "dimensionality": ["n_dof"],
        "type": "float",
        "units": "Da",
    },
    "VIB._TRAVEL": {
        "calculation": ["thermodynamics", "vibrations", "force constants"],
        "description": "vibrational lenght of travel",
        "dimensionality": ["n_dof"],
        "type": "float",
        "units": "Å",
    },
    "VIB._T_DIP": {
        "calculation": ["thermodynamics", "vibrations", "force constants"],
        "description": "vibrational transition dipole",
        "dimensionality": ["n_dof"],
        "type": "float",
    },
    "VOLUME": {
        "calculation": [
            "energy",
            "optimization",
            "thermodynamics",
            "vibrations",
            "force constants",
        ],
        "description": "volume",
        "dimensionality": "scalar",
        "property": "volume#MOPAC#{model}",
        "type": "float",
        "units": "Å^3",
    },
    "ZERO_POINT_ENERGY": {
        "calculation": ["thermodynamics", "vibrations", "force constants"],
        "description": "zero point energy",
        "dimensionality": "scalar",
        "property": "zero point energy#MOPAC#{model}",
        "type": "float",
        "units": "kcal/mol",
    },
    "RMSD": {
        "calculation": ["optimization"],
        "description": "RMSD with H removed",
        "dimensionality": "scalar",
        "type": "float",
        "units": "Å",
    },
    "displaced atom": {
        "calculation": ["optimization"],
        "description": "Atom index with largest displacement",
        "dimensionality": "scalar",
        "type": "int",
        "units": "",
    },
    "maximum displacement": {
        "calculation": ["optimization"],
        "description": "Maximum displacement of an atom",
        "dimensionality": "scalar",
        "type": "float",
        "units": "Å",
    },
    "RMSD with H": {
        "calculation": ["optimization"],
        "description": "RMSD including H atoms",
        "dimensionality": "scalar",
        "type": "float",
        "units": "Å",
    },
    "displaced atom with H": {
        "calculation": ["optimization"],
        "description": "Atom index with largest displacement, including H",
        "dimensionality": "scalar",
        "type": "int",
        "units": "",
    },
    "maximum displacement with H": {
        "calculation": ["optimization"],
        "description": "Maximum displacement of an atom, including H",
        "dimensionality": "scalar",
        "type": "float",
        "units": "Å",
    },
    # Lewis results
    "point group": {
        "calculation": ["Lewis structure"],
        "description": "point group",
        "dimensionality": "scalar",
        "type": "string",
    },
    "charge": {
        "calculation": ["Lewis structure"],
        "description": "net charge",
        "dimensionality": "scalar",
        "type": "int",
    },
    "sum of positive charges": {
        "calculation": ["Lewis structure"],
        "description": "sum of positive charges",
        "dimensionality": "scalar",
        "type": "int",
    },
    "sum of negative charges": {
        "calculation": ["Lewis structure"],
        "description": "sum of negative charges",
        "dimensionality": "scalar",
        "type": "int",
    },
    "n sigma bonds": {
        "calculation": ["Lewis structure"],
        "description": "number of sigma bonds",
        "dimensionality": "scalar",
        "type": "int",
    },
    "n pi bonds": {
        "calculation": ["Lewis structure"],
        "description": "number of pi bonds",
        "dimensionality": "scalar",
        "type": "int",
    },
    "n lone pairs": {
        "calculation": ["Lewis structure"],
        "description": "number of lone pairs",
        "dimensionality": "scalar",
        "type": "int",
    },
    "neighbors": {
        "calculation": ["Lewis structure"],
        "description": "bonded atoms",
        "dimensionality": "[n_atoms]",
        "type": "int",
    },
    "bonds": {
        "calculation": ["Lewis structure"],
        "description": "bonds",
        "dimensionality": "[n_bonds]",
        "type": "int",
    },
    "lone pairs": {
        "calculation": ["Lewis structure"],
        "description": "number of lone pairs",
        "dimensionality": "[n_atoms]",
        "type": "int",
    },
}
