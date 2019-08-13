# -*- coding: utf-8 -*-

"""Top-level package for MOPAC step."""

__author__ = """Paul Saxe"""
__email__ = 'psaxe@molssi.org'
__version__ = '0.1.0'

# Bring up the classes so that they appear to be directly in
# the package.

from mopac_step.mopac_step import MOPACStep  # noqa: F401
from mopac_step.mopac import MOPAC  # noqa: F401
from mopac_step.tk_mopac import TkMOPAC  # noqa: F401
from mopac_step.energy_step import EnergyStep  # noqa: F401
from mopac_step.energy import Energy  # noqa: F401
from mopac_step.energy_parameters import EnergyParameters  # noqa: F401
from mopac_step.tk_energy import TkEnergy  # noqa: F401
from mopac_step.optimization_step import OptimizationStep  # noqa: F401
from mopac_step.optimization import Optimization  # noqa: F401
from mopac_step.optimization_parameters import OptimizationParameters  # noqa: F401 E501
from mopac_step.tk_optimization import TkOptimization  # noqa: F401
from mopac_step.ir_step import IRStep  # noqa: F401
from mopac_step.ir import IR  # noqa: F401
from mopac_step.ir_parameters import IRParameters  # noqa: F401
from mopac_step.tk_ir import TkIR  # noqa: F401
from mopac_step.thermodynamics_step import ThermodynamicsStep  # noqa: F401
from mopac_step.thermodynamics import Thermodynamics  # noqa: F401
from mopac_step.thermodynamics_parameters import ThermodynamicsParameters  # noqa: F401 E501
from mopac_step.tk_thermodynamics import TkThermodynamics  # noqa: F401

keywords = {
    '0SCF': {
        'description': 'Read in data, then stop',
    },
    '1ELECTRON': {
        'description': 'Print final one-electron matrix',
    },
    '1SCF': {
        'description': 'Do one scf and then stop',
    },
    'ADD-H': {
        'description': ('Add hydrogen atoms (intended for use with organic '
                        'compounds)'),
    },
    'A0': {
        'description': 'Input geometry is in atomic units',
    },
    'AIDER': {
        'description': 'Read in ab-initio derivatives',
    },
    'AIGIN': {
        'description': 'Geometry must be in Gaussian format',
    },
    'AIGOUT': {
        'description': 'Print the geometry in Gaussian format in the ARC file',
    },
    'ALLBONDS': {
        'description': ('Print final bond-order matrix, including bonds to '
                        'hydrogen'),
    },
    'ALLVEC': {
        'description': 'Print all vectors (keywords vectors also needed)',
    },
    'ALT_A=A': {
        'description': 'In PDB files with alternative atoms, select atoms A',
    },
    'ALT_R=A': {
        'description': ('Deleted. All inserted residues are automatically '
                        'recognized'),
    },
    'ANGSTROMS': {
        'description': 'Input geometry is in Angstroms',
    },
    'AUTOSYM': {
        'description': 'Symmetry to be imposed automatically',
    },
    'AUX': {
        'description': ('Output auxiliary information for use by other '
                        'programs'),
    },
    'AM1': {
        'description': 'Use the AM1 hamiltonian',
    },
    'BAR=n.nn': {
        'description': 'reduce bar length by a maximum of n.nn%',
    },
    'BCC': {
        'description': 'Only even unit cells used (used by BZ)',
    },
    'BIGCYCLES=n': {
        'description': 'Do a maximum of n big steps',
    },
    'BIRADICAL': {
        'description': 'System has two unpaired electrons',
    },
    'BFGS': {
        'description': 'Use the Flepo or BFGS geometry optimizer',
    },
    'BONDS': {
        'description': 'Print final bond-order matrix',
    },
    'CAMP': {
        'description': 'Use Camp-King converger in SCF',
    },
    'CARTAB': {
        'description': 'Print point-group character table',
    },
    'C.I.=n ': {
        'description': 'A multi-electron configuration interaction specified',
    },
    'C.I.=(n,m)': {
        'description': 'A multi-electron configuration interaction specified',
    },
    'CHAINS(text)': {
        'description': ('In a protein, explicitly define the letters of '
                        'chains.'),
    },
    'CHECK': {
        'description': 'Report possible faults in input geometry',
    },
    'CHARGE=n': {
        'description': 'Charge on system = n (e.g. NH4 = +1)',
    },
    'CHARGES': {
        'description': ('Print net charge on the system, and all charges in '
                        'the system'),
    },
    'CHARST': {
        'description': 'Print details of working in CHARST',
    },
    'CIS': {
        'description': 'C.I. uses 1 electron excitations only',
    },
    'CISD': {
        'description': 'C.I. uses 1 and 2 electron excitations',
    },
    'CISDT': {
        'description': 'C.I. uses 1, 2 and 3 electron excitations',
    },
    'COMPARE': {
        'description': 'Compare the geometries of two systems',
    },
    'COMPFG': {
        'description': 'Print heat of formation calculated in COMPFG',
    },
    'COSCCH': {
        'description': 'Add in COSMO charge corrections',
    },
    'COSWRT': {
        'description': ('Write details of the solvent accessible surface to a '
                        'file'),
    },
    'CUTOFP=n.nn': {
        'description': 'Madelung distance cutoff is n .nn Angstroms',
    },
    'CUTOFF=n.nn': {
        'description': ('In MOZYME, the interatomic distance where the NDDO '
                        'approximation stops'),
    },
    'CYCLES=n': {
        'description': 'Do a maximum of n steps',
        'value optional': False,
        'value': 'integer',
    },
    'CVB': {
        'description': ('In MOZYME. add and remove specific bonds to allow a '
                        'Lewis or PDB structure.'),
    },
    'DAMP=n.nn': {
        'description': ('in MOZYME. damp SCF oscillations using a factor of '
                        'n.nn'),
    },
    'DATA=text': {
        'description': 'Input data set is re-defined to text',
    },
    'DCART': {
        'description': 'Print part of working in DCART',
    },
    'DDMAX=n.nn': {
        'description': 'See EF code',
    },
    'DDMIN=n.nn': {
        'description': 'Minimum trust radius in a EF/TS calculation',
    },
    'DEBUG': {
        'description': 'Debug option turned on',
    },
    'DEBUG PULAY': {
        'description': 'Print working in PULAY',
    },
    'DENOUT': {
        'description': 'Density matrix output, unformatted',
        },
    'DENOUTF': {
        'description': 'Density matrix output, formatted',
    },
    'DENSITY': {
        'description': 'Print final density matrix',
    },
    'DERI1': {
        'description': 'Print part of working in DERI1',
    },
    'DERI2': {
        'description': 'Print part of working in DERI2',
    },
    'DERITR': {
        'description': 'Print part of working in DERIT',
    },
    'DERIV': {
        'description': 'Print part of working in DERIV',
    },
    'DERNVO': {
        'description': 'Print part of working in DERNVO',
    },
    'DFORCE': {
        'description': 'Force calculation specified, also print force matrix.',
    },
    'DFP': {
        'description': ('Use Davidson-Fletcher-Powell method to optimize '
                        'geometries'),
    },
    'DISEX=n.nn': {
        'description': 'Distance for interactions in fine grid in COSMO',
    },
    'DISP': {
        'description': ('Print the hydrogen bonding and dispersion '
                        'contributions to the heat of formation'),
    },
    'DMAX=n.nn': {
        'description': 'Maximum stepsize in eigenvector following',
    },
    'DOUBLET': {
        'description': 'Doublet state required',
    },
    'DRC=n.nnn': {
        'description': 'Dynamic reaction coordinate calculation',
        'value optional': True,
        'value': 'float',
    },
    'DUMP=nn.nn': {
        'description': 'Write restart files every n seconds',
        'value optional': False,
        'value': 'float',
    },
    'ECHO': {
        'description': 'Data are echoed back before calculation starts',
    },
    'EF': {
        'description': ('Use the EigenFollowing routine for geometry '
                        'optimization'),
    },
    'EIGEN': {
        'description': ('Print canonical eigenvectors instead of LMOs in a '
                        'MOZYME calculations'),
    },
    'EIGS': {
        'description': 'Print all eigenvalues in ITER',
    },
    'ENPART': {
        'description': 'Partition energy into components'
    },
    'EPS=n.nn': {
        'description': 'Dielectric constant in COSMO calculation',
        'value optional': False,
        'value': 'float',
    },
    'ESP': {
        'description': 'Electrostatic potential calculation',
    },
    'ESPRST': {
        'description': 'Restart of electrostatic potential',
    },
    'ESR': {
        'description': 'Calculate RHF spin density',
    },
    'EXCITED': {
        'description': 'Optimize first excited singlet state',
    },
    'EXTERNAL=name': {
        'description': 'Read parameters off disk',
    },
    'FIELD=(n.nn,m.mm,l.ll)': {
        'description': 'An external electric field is to be used',
        'value optional': False,
        'value': ('float', 'float', 'float'),
    },
    'FILL=n': {
        'description': ('In RHF open and closed shell, force M.O. n to be '
                        'filled'),
        'value optional': False,
        'value': 'integer',
    },
    'FLEPO': {
        'description': 'Print details of geometry optimization',
    },
    'FMAT': {
        'description': 'Print details of working in FMAT',
    },
    'FOCK': {
        'description': 'Print last Fock matrix',
    },
    'FREQCY': {
        'description': 'Print symmetrized Hessian in a FORCE calculation',
    },
    'FORCE': {
        'description': 'Calculate vibrational frequencies',
    },
    'FORCETS': {
        'description': ('Calculate the vibrational frequencies for atoms in a '
                        'transition state'),
    },
    'GEO-OK': {
        'description': 'Override some safety checks',
    },
    'GEO_DAT=<text>': {
        'description': 'Read in geometry from the file <text>',
        'value optional': False,
        'value': 'filename',
    },
    'GEO_REF=<text>': {
        'description': 'Read in a second geometry from the file <text>',
        'value optional': False,
        'value': 'filename',
    },
    'GNORM=n.nn': {
        'description': ('Exit when the gradient norm drops below n.nn '
                        'kcal/mol/Angstrom'),
        'value optional': False,
        'value': 'float',
    },
    'GRADIENTS': {
        'description': 'Print all gradients',
    },
    'GRAPH': {
        'description': 'Generate unformatted file for graphics',
    },
    'GRAPHF': {
        'description': ('Generate a formatted file for graphics suitable for '
                        'Jmol and MOPETE.'),
    },
    'HCORE': {
        'description': ('Print all parameters used, the one-electron matrix, '
                        'and two-electron integrals'),
    },
    'HESSIAN': {
        'description': 'Print Hessian from geometry optimization',
    },
    'HESS=n': {
        'description': 'Options for calculating Hessian matrices in EF',
        'value optional': False,
        'value': 'integer',
        'allowed values': (0, 1, 2),
    },
    'H-PRIORITY=n.nn': {
        'description': 'Heat of formation takes priority in DRC',
        'value optional': True,
        'value': 'float',
    },
    'HTML': {
        'description': 'Write a web-page for displaying and editing a protein',
    },
    'HYPERFINE': {
        'description': 'Hyperfine coupling constants to be calculated',
    },
    'INT': {
        'description': 'Make all coordinates internal coordinates',
    },
    'INVERT': {
        'description': 'Reverse all optimization flags',
    },
    'IRC=n': {
        'description': 'Intrinsic reaction coordinate calculation',
        'value optional': True,
        'value': 'integer',
    },
    'ISOTOPE': {
        'description': 'Force matrix written to disk (channel 9 )',
    },
    'ITER': {
        'description': 'Print details of working in ITER',
    },
    'ITRY=nn': {
        'description': 'Set limit of number of SCF iterations to n',
        'value optional': False,
        'value': 'integer',
        'default': 2000,
        'minimum': 0,
    },
    'IUPD=n': {
        'description': 'Mode of Hessian update in eigenvector following',
        'value optional': False,
        'value': 'integer',
    },
    'KINETIC=n.nnn': {
        'description': 'Excess kinetic energy added to DRC calculation',
        'value optional': False,
        'value': 'float',
    },
    'KING': {
        'description': 'Use Camp-King converger for SCF',
    },
    'LARGE': {
        'description': 'Print expanded output',
    },
    'LBFGS': {
        'description': 'Use the low-memory version of the BFGS optimizer',
    },
    'LET': {
        'description': 'Override certain safety checks',
    },
    'LEWIS': {
        'description': 'Print the Lewis structure',
    },
    'LINMIN': {
        'description': 'Print details of line minimization',
    },
    'LOCALIZE': {
        'description': ('Print the localized orbitals. These are also called '
                        'Natural Bond Orbitals or NBO'),
    },
    'LOCATE-TS': {
        'description': ('Given reactants and products, locate the transition '
                        'state connecting them'),
    },
    'LOG': {
        'description': 'Generate a log file',
    },
    'MECI': {
        'description': 'Print details of MECI calculation',
    },
    'MERS=(n1,n2,n3)': {
        'description': 'Keyword generated by MAKPOL for use with program BZ',
    },
    'METAL=(a[,b[,c[...]]])': {
        'description': 'Make specified atoms 100% ionic',
    },
    'MICROS=n': {
        'description': 'Use specific microstates in the C.I.',
        'value optional': False,
        'value': 'integer',
    },
    'MINI': {
        'description': ('Reduce the size of the output by only printing '
                        'specified atoms'),
    },
    'MINMEP': {
        'description': 'Minimize MEP minima in the plane defined',
    },
    'MMOK': {
        'description': 'Use molecular mechanics correction to CONH bonds',
    },
    'MNDO': {
        'description': 'Use the MNDO hamiltonian',
    },
    'MNDOD': {
        'description': 'Use the MNDO-d hamiltonian'
    },
    'MODE=n': {
        'description': 'In EF, follow Hessian mode no. n',
        'value optional': False,
        'value': 'integer',
    },
    'MOL_QMMM': {
        'description': ('Incorporate environmental effects in the QM/MM '
                        'approach'),
    },
    'MOLDAT': {
        'description': 'Print details of working in MOLDAT',
    },
    'MOLSYM': {
        'description': 'Print details of working in MOLSYM',
    },
    'MOPAC': {
        'description': 'Use old MOPAC definition for 2nd and 3rd atoms',
    },
    'MOZYME': {
        'description': ('Use the Localized Molecular Orbital method to speed '
                        'up the SCF'),
    },
    'MS=n': {
        'description': 'In MECI, magnetic component of spin',
        'value optional': False,
        'value': 'float',
        'allowed value test': '2*value',
    },
    'MULLIK': {
        'description': 'Print the Mulliken population analysis',
    },
    'N**2=n.nn': {
        'description': ('In excited state COSMO calculations, set the value '
                        'of N**2'),
        'value optional': False,
        'value': 'float',
    },
    'NLLSQ': {
        'description': 'Minimize gradients using NLLSQ',
    },
    'NOANCI': {
        'description': 'Do not use analytical C.I. derivatives',
    },
    'NOCOMMENTS': {
        'description': ('Ignore all lines except ATOM, HETATM, and TER in PDB '
                        'files'),
    },
    'NOGPU': {
        'description': 'Do not use GPU acceleration',
    },
    'NOLOG': {
        'description': 'Suppress log file trail, where possible',
    },
    'NOMM': {
        'description': ('Do not use molecular mechanics correction to CONH '
                        'bonds'),
    },
    'NONET': {
        'description': 'NONET state required',
    },
    'NONR': {
        'description': 'Do not use Newton-Raphson method in EF',
    },
    'NOOPT': {
        'description': ('Do not optimize the coordinates of all atoms '
                        '(see OPT-X)'),
    },
    'NOOPT-X': {
        'description': ('Do not optimize the coordinates of all atoms of type '
                        'X'),
    },
    'NOREOR': {
        'description': 'In symmetry work, use supplied orientation',
    },
    'NORESEQ': {
        'description': ('Suppress the default re-sequencing of atoms to the '
                        'PDB sequence'),
    },
    'NOSWAP': {
        'description': 'Do not allow atom swapping when GEO_REF is used',
    },
    'NOSYM': {
        'description': 'Point-group symmetry set to C1',
    },
    'NOTER': {
        'description': 'Do not put "TER"s in PDB files',
    },
    'NOTHIEL': {
        'description': "Do not use Thiel's FSTMIN technique",
    },
    'NOTXT': {
        'description': 'Remove any text from atom symbols',
    },
    'NOXYZ': {
        'description': 'Do not print Cartesian coordinates',
    },
    'NSPA=n': {
        'description': 'Sets number of geometric segments in COSMO',
        'value optional': False,
        'value': 'integer',
    },
    'NSURF': {
        'description': 'Number of surfaces in an ESP calculation',
    },
    'OCTET': {
        'description': 'Octet state required',
    },
    'OLDCAV': {
        'description': ('In COSMO, use the old Solvent Accessible Surface '
                        'calculation'),
    },
    'OLDENS': {
        'description': 'Read initial density matrix off disk',
    },
    'OLDFPC': {
        'description': 'Use the old fundamental physical constants',
    },
    'OLDGEO': {
        'description': 'Previous geometry to be used',
    },
    'OMIN=n.nn': {
        'description': 'In TS, minimum allowed overlap of eigenvectors',
        'value optional': False,
        'value': 'float',
    },
    'OPEN(n1,n2)': {
        'description': 'Open-shell UHF or RHF calculation requested',
    },
    'OPT': {
        'description': 'Optimize coordinates of all atoms',
    },
    'OPT-X': {
        'description': 'Optimize the coordinates of all atoms of type X',
    },
    'OPT(text=n.nn)': {
        'description': ('Optimize the coordinates of all atoms within n.nn '
                        'Ångstroms of atoms labeled "text"'),
    },
    'OUTPUT': {
        'description': ('Reduce the amount of output (useful for large '
                        'systems)'),
    },
    'P=n.nn': {
        'description': 'An applied pressure of n.nn Newtons/m2 to be used',
    },
    'PDB': {
        'description': 'Input geometry is in protein data bank format',
    },
    'PDB=(text)': {
        'description': 'User defined chemical symbols in protein data base',
    },
    'PDBOUT	': {
        'description': 'Output geometry in pdb format',
    },
    'PECI': {
        'description': 'C.I. involves paired excitations only',
    },
    'PI': {
        'description': 'Resolve density matrix into σ, π, and δ components',
    },
    'pKa': {
        'description': ('Print the pKa for ionizable hydrogen atoms attached '
                        'to oxygen atoms'),
    },
    'PL': {
        'description': 'Monitor convergence of density matrix in ITER',
    },
    'PM3': {
        'description': 'Use the MNDO-PM3 Hamiltonian',
    },
    'PM6': {
        'description': 'Use the PM6 Hamiltonian'
    },
    'PM6-D3': {
        'description': ("Use the PM6 Hamiltonian with Grimme's corrections "
                        "for dispersion"),
    },
    'PM6-DH+': {
        'description': ('Use the PM6 Hamiltonian with corrections for '
                        'dispersion and hydrogen-bonding'),
    },
    'PM6-DH2': {
        'description': ('Use the PM6 Hamiltonian with corrections for '
                        'dispersion and hydrogen-bonding'),
    },
    'PM6-DH2X': {
        'description': ('Use PM6 with corrections for dispersion and hydrogen '
                        'and halogen bonding'),
    },
    'PM6-D3H4': {
        'description': "Use PM6 with Řezáč and Hobza's D3H4 correction",
    },
    'PM6-D3H4X': {
        'description': ("Use PM6 with Brahmkshatriya, et al.'s D3H4X "
                        "correction"),
    },
    'PMEP': {
        'description': 'Complete semiempirical MEP calculation',
    },
    'PM7': {
        'description': 'Use the PM7 Hamiltonian',
    },
    'PM7-TS': {
        'description': 'Use the PM7-TS Hamiltonian (only for barrier heights)',
    },
    'PMEPR': {
        'description': 'Complete semiempirical MEP in a plane to be defined',
    },
    'POINT=n': {
        'description': 'Number of points in reaction path',
        'value optional': False,
        'value': 'integer',
    },
    'POINT1=n': {
        'description': ('Number of points in first direction in grid '
                        'calculation'),
        'value optional': False,
        'value': 'integer',
    },
    'POINT2=n': {
        'description': ('Number of points in second direction in grid '
                        'calculation'),
        'value optional': False,
        'value': 'integer',
    },
    'POLAR': {
        'description': ('Calculate first, second and third order '
                        'polarizabilities'),
    },
    'POTWRT': {
        'description': 'In ESP, write out electrostatic potential to unit 21',
    },
    'POWSQ': {
        'description': 'Print details of working in POWSQ',
    },
    'PRECISE': {
        'description': 'Criteria to be increased by 100 times',
    },
    'PRESSURE': {
        'description': 'Apply pressure or tension to a solid or polymer',
    },
    'PRNT=n': {
        'description': 'Print details of geometry optimization in EF',
    },
    'PRTCHAR': {
        'description': 'Print charges in ARC file',
    },
    'PRTINT': {
        'description': 'Print interatomic distances',
    },
    'PRTMEP': {
        'description': 'MEP contour data output to <filename>.mep',
    },
    'PRTXYZ': {
        'description': 'Print Cartesian coordinates',
    },
    'PULAY': {
        'description': "Use Pulay's converger to obtain a SCF",
    },
    'QMMM': {
        'description': ('Incorporate environmental effects in the QM/MM '
                        'approach'),
    },
    'QPMEP': {
        'description': 'Charges derived from Wang-Ford type AM1 MEP',
    },
    'QUARTET': {
        'description': 'Quartet state required',
    },
    'QUINTET': {
        'description': 'Quintet state required',
    },
    'RAPID': {
        'description': ('In MOZYME geometry optimizations, only use atoms '
                        'being optimized in the SCF'),
    },
    'RECALC=n': {
        'description': 'In EF, recalculate Hessian every n steps',
        'value optional': False,
        'value': 'integer',
    },
    'RE-LOCAL': {
        'description': ('At the end of a MOZYME calculation, re-localize the '
                        'LMOs'),
    },
    'RE-LOCAL=n': {
        'description': ('During and at end of a MOZYME calculation, '
                        're-localize the LMOs'),
        'value optional': True,
        'value': 'integer',
    },
    'RELSCF': {
        'description': 'Default SCF criterion multiplied by n',
    },
    'REORTHOG': {
        'description': ("In MOZYME, re-orthogonalize LMO's each 10 SCF "
                        "calculations."),
    },
    'RESEQ': {
        'description': 'Re-arrange the atoms to match the PDB convention',
    },
    'RESIDUES': {
        'description': ('Label each atom in a polypeptide with the amino acid '
                        'residue.'),
    },
    'RESTART': {
        'description': 'Calculation restarted',
    },
    'RHF': {
        'description': 'Use Restricted Hartree-Fock methods',
    },
    'RM1': {
        'description': 'Use the RM1 Hamiltonian',
    },
    'RMAX=n.nn': {
        'description': 'In TS, maximum allowed ratio for energy change',
    },
    'RMIN=n.nn': {
        'description': 'In TS, minimum allowed ratio for energy change',
    },
    'ROOT=n': {
        'description': 'Root n to be optimized in a C.I. calculation',
    },
    'RSCAL': {
        'description': 'In EF, scale p-RFO to trust radius',
    },
    'RSOLV=n.nn': {
        'description': 'Effective radius of solvent in COSMO',
    },
    'SADDLE': {
        'description': 'Optimize transition state',
    },
    'SCALE': {
        'description': 'Scaling factor for van der waals distance in ESP',
    },
    'SCFCRT=n.nn': {
        'description': 'Default SCF criterion replaced by the value supplied',
    },
    'SCINCR=n.nn': {
        'description': 'Increment between layers in ESP',
    },
    'SEPTET': {
        'description': 'Septet state required',
    },
    'SETPI': {
        'description': ('In MOZYME, some π bonds are explicitly set by the '
                        'user'),
    },
    'SETUP': {
        'description': 'Extra keywords to be read from setup file',
    },
    'SEXTET': {
        'description': 'Sextet state required',
    },
    'SHIFT=n.nn': {
        'description': 'a damping factor of n defined to start SCF',
    },
    # 'SHUT <file>': {
    #     'description': ('Send a command to MOPAC to make a restart and '
    #                     'density file, then stop.'),
    # },
    'SIGMA': {
        'description': 'Minimize gradients using SIGMA',
    },
    'SINGLET': {
        'description': 'Singlet state required',
    },
    'SITE=(text)': {
        'description': 'Define ionization state of residues in proteins',
    },
    'SLOG=n.nn': {
        'description': ('In L-BFGS optimization, use fixed step of length '
                        'n .nn'),
    },
    'SLOPE': {
        'description': 'Multiplier used to scale MNDO charges',
    },
    'SMOOTH': {
        'description': ('In a GRID calculation, remove artifacts caused by '
                        'the order in which points are calculated'),
    },
    'SNAP': {
        'description': 'Increase precision of symmetry angles',
    },
    'SPARKLE': {
        'description': 'Use sparkles instead of atoms with basis sets',
    },
    'SPIN': {
        'description': 'Print final UHF spin matrix',
    },
    'START_RES(text)': {
        'description': ('Define starting residue numbers in a protein, if '
                        'different from the default'),
    },
    'STATIC': {
        'description': 'Calculate Polarizability using electric fields',
    },
    'STEP': {
        'description': 'Step size in path',
    },
    'STEP1=n.nnn': {
        'description': 'Step size n for first coordinate in grid calculation',
    },
    'STEP2=n.nnn': {
        'description': 'Step size n for second coordinate in grid calculation',
    },
    'STO3G': {
        'description': 'Deorthogonalize orbitals in STO-3G basis',
    },
    'SUPER': {
        'description': 'Print superdelocalizabilities',
    },
    'SYBYL': {
        'description': "Output a file for use by Tripos's SYBYL program",
    },
    'SYMAVG': {
        'description': 'Average symmetry equivalent ESP charges',
    },
    'SYMOIR': {
        'description': ('Print characters of eigenvectors and print number of '
                        'I.R.s'),
    },
    'SYMTRZ': {
        'description': 'Print details of working in subroutine SYMTRZ.',
    },
    'SYMMETRY': {
        'description': 'Impose symmetry conditions',
    },
    'T=n[M,H,D]': {
        'description': 'A time of n seconds requested',
    },
    'THERMO(nnn,mmm,lll)': {
        'description': 'Perform a thermodynamics calculation',
    },
    'THREADS=n': {
        'description': ('Set the number of threads to be used in '
                        'parallelization to n'),
    },
    'TIMES': {
        'description': 'Print times of various stages',
    },
    'T-PRIORITY=n.nn': {
        'description': 'Time takes priority in DRC',
    },
    'TRANS=n': {
        'description': ('The system is a transition state (used in '
                        'thermodynamics calculation)'),
    },
    'TRIPLET': {
        'description': 'Triplet state required',
    },
    'TS': {
        'description': 'Using EF routine for TS search',
    },
    'UHF': {
        'description': 'Use the Unrestricted Hartree-Fock method',
    },
    'VDW(text)': {
        'description': ('Van der waals radius for atoms in COSMO defined by '
                        'user'),
    },
    'VDWM(text)': {
        'description': ('Van der waals radius for atoms in MOZYME defined by '
                        'user'),
    },
    'VECTORS': {
        'description': 'Print final eigenvectors',
    },
    'VELOCITY': {
        'description': ('Supply the initial velocity vector in a DRC '
                        'calculation'),
    },
    'WILLIAMS': {
        'description': 'Use Williams surface',
    },
    'X-PRIORITY=n.nn': {
        'description': 'Geometry changes take priority in DRC',
    },
    'XENO': {
        'description': ('Allow non-standard residues in proteins to be '
                        'labeled.'),
    },
    'XYZ': {
        'description': 'Do all geometric operations in Cartesian coordinates',
    },
    'Z=n': {
        'description': 'Number of mers in a cluster',
    },
}

properties = {
    "AO_ATOMINDEX": {
        "calculation": [
            "single point energy",
            "optimization",
            "thermodynamics",
            "vibrations"
        ],
        "description": "atom for AO",
        "dimensionality": [
            "n_aos"
        ],
        "type": "integer"
    },
    "AO_ZETA": {
        "calculation": [
            "single point energy",
            "optimization",
            "thermodynamics",
            "vibrations"
        ],
        "description": "Slater exponent",
        "dimensionality": [
            "n_aos"
        ],
        "type": "float"
    },
    "AREA": {
        "calculation": [
            "single point energy",
            "optimization",
            "thermodynamics",
            "vibrations"
        ],
        "description": "surface area",
        "dimensionality": "scalar",
        "type": "float",
        "units": "Å^2"
    },
    "ATOM_CHARGES": {
        "calculation": [
            "single point energy",
            "optimization",
            "thermodynamics",
            "vibrations"
        ],
        "description": "atom charges",
        "dimensionality": [
            "n_atoms"
        ],
        "type": "float"
    },
    "ATOM_CORE": {
        "calculation": [
            "single point energy",
            "optimization",
            "thermodynamics",
            "vibrations"
        ],
        "description": "number of valence electrons",
        "dimensionality": [
            "n_atoms"
        ],
        "type": "integer"
    },
    "ATOM_EL": {
        "calculation": [
            "single point energy",
            "optimization",
            "thermodynamics",
            "vibrations"
        ],
        "description": "atomic symbol",
        "dimensionality": [
            "n_atoms"
        ],
        "type": "string"
    },
    "ATOM_PQN": {
        "calculation": [
            "single point energy",
            "optimization",
            "thermodynamics",
            "vibrations"
        ],
        "description": "principal quantum number",
        "dimensionality": [
            "n_aos"
        ],
        "type": "integer"
    },
    "ATOM_SYMTYPE": {
        "calculation": [
            "single point energy",
            "optimization",
            "thermodynamics",
            "vibrations"
        ],
        "description": "atomic orbital angular shape",
        "dimensionality": [
            "n_aos"
        ],
        "type": "string"
    },
    "ATOM_X": {
        "calculation": [
            "single point energy",
            "optimization",
            "thermodynamics",
            "vibrations"
        ],
        "description": "x, y, z coordinates",
        "dimensionality": [
            3,
            "n_atoms"
        ],
        "type": "float",
        "units": "Å"
    },
    "ATOM_X_FORCE": {
        "calculation": [
            "thermodynamics",
            "vibrations"
        ],
        "description": "reoriented coordinates",
        "dimensionality": [
            3,
            "n_atoms"
        ],
        "type": "float",
        "units": "Å"
    },
    "ATOM_X_OPT": {
        "calculation": [
            "optimization",
            "thermodynamics",
            "vibrations"
        ],
        "description": "optimized x, y, z coordinates",
        "dimensionality": [
            3,
            "n_atoms"
        ],
        "type": "float",
        "units": "Å"
    },
    "ATOM_X_UPDATED": {
        "calculation": [
            "optimization"
        ],
        "description": "trajectory coordinates",
        "dimensionality": [
            "nsteps", [
                3,
                "n_atoms"
            ]
        ],
        "type": "float",
        "units": "Å"
    },
    "COMMENTS": {
        "calculation": [
        ],
        "description": "User comment line",
        "dimensionality": "scalar",
        "type": "string"
    },
    "CPU_TIME": {
        "calculation": [
            "single point energy",
            "optimization",
            "thermodynamics",
            "vibrations"
        ],
        "description": "cpu time for calculation",
        "dimensionality": "scalar",
        "type": "float",
        "units": "s"
    },
    "DATE": {
        "calculation": [
            "single point energy",
            "optimization",
            "thermodynamics",
            "vibrations"
        ],
        "description": "date and time of calculation",
        "dimensionality": "scalar",
        "type": "date_time"
    },
    "DIPOLE": {
        "calculation": [
            "single point energy",
            "optimization",
            "thermodynamics",
            "vibrations"
        ],
        "description": "dipole moment",
        "dimensionality": "scalar",
        "type": "float",
        "units": "debye"
    },
    "DIP_VEC": {
        "calculation": [
            "single point energy",
            "optimization",
            "thermodynamics",
            "vibrations"
        ],
        "description": "dipole vector",
        "dimensionality": [
            3
        ],
        "type": "float",
        "units": "debye"
    },
    "EIGENVALUES": {
        "calculation": [
            "single point energy",
            "optimization",
            "thermodynamics",
            "vibrations"
        ],
        "description": "orbital energies",
        "dimensionality": [
            "n_aos"
        ],
        "type": "float",
        "units": "eV"
    },
    "EIGENVECTORS": {
        "calculation": [
            "single point energy",
            "optimization",
            "thermodynamics",
            "vibrations"
        ],
        "description": "orbital coefficients",
        "dimensionality": [
            "n_aos"
        ],
        "type": "float"
    },
    "EMPIRICAL_FORMULA": {
        "calculation": [
            "single point energy",
            "optimization",
            "thermodynamics",
            "vibrations"
        ],
        "description": "empirical formula",
        "dimensionality": "scalar",
        "type": "string"
    },
    "ENERGY_ELECTRONIC": {
        "calculation": [
            "single point energy",
            "optimization",
            "thermodynamics",
            "vibrations"
        ],
        "description": "electronic energy",
        "dimensionality": "scalar",
        "type": "float",
        "units": "eV"
    },
    "ENERGY_NUCLEAR": {
        "calculation": [
            "single point energy",
            "optimization",
            "thermodynamics",
            "vibrations"
        ],
        "description": "nuclear repulsion energy",
        "dimensionality": "scalar",
        "type": "float",
        "units": "eV"
    },
    "ENTHALPY_TOT": {
        "calculation": [
            "thermodynamics",
            "vibrations"
        ],
        "description": "enthalpy",
        "dimensionality": [
            "n_temps",
        ],
        "type": "float",
        "units": "cal/mol"
    },
    "ENTROPY_TOT": {
        "calculation": [
            "thermodynamics",
            "vibrations"
        ],
        "description": "entropy",
        "dimensionality": [
            "n_temps",
        ],
        "type": "float",
        "units": "cal/K/mol"
    },
    "GRADIENTS": {
        "calculation": [
            "optimization",
            "thermodynamics",
            "vibrations"
        ],
        "description": "",
        "dimensionality": [
            3,
            "n_atoms"
        ],
        "type": "float",
        "units": "kcal/mol/Å"
    },
    "GRADIENT_NORM": {
        "calculation": [
            "optimization",
            "thermodynamics",
            "vibrations"
        ],
        "description": "final norm of the gradient",
        "dimensionality": "scalar",
        "type": "float",
        "units": "kcal/mol/Å"
    },
    "GRADIENT_UPDATED": {
        "calculation": [
            "optimization"
        ],
        "description": "forces in trajectory",
        "dimensionality": [
            "nsteps", [
                3,
                "n_atoms"
            ]
        ],
        "type": "float",
        "units": "kcal/mol/Å"
    },
    "HEAT_CAPACITY_TOT": {
        "calculation": [
            "thermodynamics",
            "vibrations"
        ],
        "description": "heat capacity",
        "dimensionality": [
            "n_temps",
        ],
        "type": "float",
        "units": "cal/K/mol"
    },
    "HEAT_OF_FORMATION": {
        "calculation": [
            "single point energy",
            "optimization",
            "thermodynamics",
            "vibrations"
        ],
        "description": "heat of formation",
        "dimensionality": "scalar",
        "type": "float",
        "units": "kcal/mol"
    },
    "HEAT_OF_FORM_UPDATED": {
        "calculation": [
            "optimization"
        ],
        "description": "heat of formation in trajectory",
        "dimensionality": [
            "nsteps"
        ],
        "type": "float",
        "units": "kcal/mol"
    },
    "HESSIAN_MATRIX": {
        "calculation": [
            "thermodynamics",
            "vibrations"
        ],
        "description": "",
        "dimensionality": [
            "n_dof",
            "n_dof"
        ],
        "type": "float",
        "units": "mdynes/Å/Da"
    },
    "H_O_F(T)": {
        "calculation": [
            "thermodynamics",
            "vibrations"
        ],
        "description": "",
        "dimensionality": [
            "n_temps"
        ],
        "type": "float",
        "units": "kcal/mol"
    },
    "INT_FORCE_CONSTS": {
        "calculation": [
            "thermodynamics",
            "vibrations"
        ],
        "description": "force constants for internals",
        "dimensionality": ["n_dofs"],
        "type": "float",
        "units": "mdyne/Å"
    },
    "IONIZATION_POTENTIAL": {
        "calculation": [
            "single point energy",
            "optimization",
            "thermodynamics",
            "vibrations"
        ],
        "description": "ionization potential (IP)",
        "dimensionality": "scalar",
        "type": "float",
        "units": "eV"
    },
    "ISOTOPIC_MASSES": {
        "calculation": [
            "thermodynamics",
            "vibrations"
        ],
        "description": "",
        "dimensionality": [
            "n_atoms"
        ],
        "type": "float",
        "units": "Da"
    },
    "KEYWORDS": {
        "calculation": [
        ],
        "description": "",
        "dimensionality": "scalar",
        "type": "string"
    },
    "M.O.SYMMETRY_LABELS": {
        "calculation": [
            "single point energy",
            "optimization",
            "thermodynamics",
            "vibrations"
        ],
        "description": "molecular orbital symmetries",
        "dimensionality": [
            "n_mos"
        ],
        "type": "string"
    },
    "METHOD": {
        "calculation": [
            "single point energy",
            "optimization",
            "thermodynamics",
            "vibrations"
        ],
        "description": "hamiltonian",
        "dimensionality": "scalar",
        "type": "string"
    },
    "MOLECULAR_ORBITAL_OCCUPANCIES": {
        "calculation": [
            "single point energy",
            "optimization",
            "thermodynamics",
            "vibrations"
        ],
        "description": "orbital occupancies",
        "dimensionality": [
            "n_mos"
        ],
        "type": "float"
    },
    "MOLECULAR_WEIGHT": {
        "calculation": [
            "single point energy",
            "optimization",
            "thermodynamics",
            "vibrations"
        ],
        "description": "molecular weight",
        "dimensionality": "scalar",
        "type": "float",
        "units": "Da"
    },
    "MOPAC_VERSION": {
        "calculation": [
            "single point energy",
            "optimization",
            "thermodynamics",
            "vibrations"
        ],
        "description": "MOPAC version",
        "dimensionality": "scalar",
        "type": "string"
    },
    "NORMAL_MODES": {
        "calculation": [
            "thermodynamics",
            "vibrations"
        ],
        "description": "",
        "dimensionality": [
            "n_dof",
            "n_dof"
        ],
        "type": "float"
    },
    "NORMAL_MODE_SYMMETRY_LABELS": {
        "calculation": [
            "thermodynamics",
            "vibrations"
        ],
        "description": "",
        "dimensionality": [
            "n_dof"
        ],
        "type": "string"
    },
    "NUMBER_SCF_CYCLES": {
        "calculation": [
            "single point energy",
            "optimization",
            "thermodynamics",
            "vibrations"
        ],
        "description": "number of scf's",
        "dimensionality": "scalar",
        "type": "integer"
    },
    "NUM_ALPHA_ELECTRONS": {
        "calculation": [
            "single point energy",
            "optimization",
            "thermodynamics",
            "vibrations"
        ],
        "description": "number of spin-up electrons",
        "dimensionality": "scalar",
        "type": "integer"
    },
    "NUM_BETA_ELECTRONS": {
        "calculation": [
            "single point energy",
            "optimization",
            "thermodynamics",
            "vibrations"
        ],
        "description": "number of spin-down electrons",
        "dimensionality": "scalar",
        "type": "integer"
    },
    "NUM_ELECTRONS": {
        "calculation": [
            "single point energy",
            "optimization",
            "thermodynamics",
            "vibrations"
        ],
        "description": "number of electrons",
        "dimensionality": "scalar",
        "type": "integer"
    },
    "ORIENTATION_ATOM_X": {
        "calculation": [
            "thermodynamics",
            "vibrations"
        ],
        "description": "",
        "dimensionality": [
            3,
            "n_atoms"
        ],
        "type": "float",
        "units": "Å"
    },
    "OVERLAP_MATRIX": {
        "calculation": [
            "single point energy",
            "optimization",
            "thermodynamics",
            "vibrations"
        ],
        "description": "the AO overlap matrix",
        "dimensionality": [
            "triangular",
            "n_aos",
            "n_aos"
        ],
        "type": "float"
    },
    "POINT_GROUP": {
        "calculation": [
            "single point energy",
            "optimization",
            "thermodynamics",
            "vibrations"
        ],
        "description": "the molecular symmetry",
        "dimensionality": "scalar",
        "type": "string"
    },
    "PRI_MOM_OF_I": {
        "calculation": [
            "thermodynamics",
            "vibrations"
        ],
        "description": "",
        "dimensionality": [
            3
        ],
        "type": "float",
        "units": "10^-40*g*cm^2"
    },
    "ROTAT_CONSTS": {
        "calculation": [
            "thermodynamics",
            "vibrations"
        ],
        "description": "",
        "dimensionality": [
            3
        ],
        "type": "float",
        "units": "1/cm"
    },
    "SET_OF_MOS": {
        "calculation": [
            "single point energy",
            "optimization",
            "thermodynamics",
            "vibrations"
        ],
        "description": "set of MOs",
        "dimensionality": [
            2
        ],
        "type": "string"
    },
    "SPIN_COMPONENT": {
        "calculation": [
            "single point energy",
            "optimization",
            "thermodynamics",
            "vibrations"
        ],
        "description": "spin component",
        "dimensionality": [3],
        "type": "float"
    },
    "THERMODYNAMIC_PROPERTIES_TEMPS": {
        "calculation": [
            "thermodynamics",
            "vibrations"
        ],
        "description": "",
        "dimensionality": [
            "n_temps"
        ],
        "type": "float",
        "units": "K"
    },
    "TITLE": {
        "calculation": [
        ],
        "description": "title of calculation",
        "dimensionality": "scalar",
        "type": "string"
    },
    "TOTAL_DENSITY_MATRIX": {
        "calculation": [
            "single point energy",
            "optimization",
            "thermodynamics",
            "vibrations"
        ],
        "description": "density matrix",
        "dimensionality": [
            "n_mos",
            "n_mos"
        ],
        "shape": "triangular",
        "type": "float"
    },
    "TOTAL_ENERGY": {
        "calculation": [
            "single point energy",
            "optimization",
            "thermodynamics",
            "vibrations"
        ],
        "description": "total energy",
        "dimensionality": "scalar",
        "type": "float",
        "units": "eV"
    },
    "TOTAL_SPIN": {
        "calculation": [
            "single point energy",
            "optimization",
            "thermodynamics",
            "vibrations"
        ],
        "description": "spin",
        "dimensionality": "scalar",
        "type": "float"
    },
    "VIB._EFF_MASS": {
        "calculation": [
            "thermodynamics",
            "vibrations"
        ],
        "description": "",
        "dimensionality": [
            "n_dof"
        ],
        "type": "float",
        "units": "Da"
    },
    "VIB._FREQ": {
        "calculation": [
            "thermodynamics",
            "vibrations"
        ],
        "description": "",
        "dimensionality": [
            "n_dof"
        ],
        "type": "float",
        "units": "1/cm"
    },
    "VIB._RED_MASS": {
        "calculation": [
            "thermodynamics",
            "vibrations"
        ],
        "description": "",
        "dimensionality": [
            "n_dof"
        ],
        "type": "float",
        "units": "Da"
    },
    "VIB._TRAVEL": {
        "calculation": [
            "thermodynamics",
            "vibrations"
        ],
        "description": "",
        "dimensionality": [
            "n_dof"
        ],
        "type": "float",
        "units": "Å"
    },
    "VIB._T_DIP": {
        "calculation": [
            "thermodynamics",
            "vibrations"
        ],
        "description": "",
        "dimensionality": [
            "n_dof"
        ],
        "type": "float",
        "units": "electrons"
    },
    "VOLUME": {
        "calculation": [
            "single point energy",
            "optimization",
            "thermodynamics",
            "vibrations"
        ],
        "description": "volume",
        "dimensionality": "scalar",
        "type": "float",
        "units": "Å^3"
    },
    "ZERO_POINT_ENERGY": {
        "calculation": [
            "thermodynamics",
            "vibrations"
        ],
        "description": "zero point energy",
        "dimensionality": "scalar",
        "type": "float",
        "units": "kcal/mol"
    }
}
