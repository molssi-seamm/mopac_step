# -*- coding: utf-8 -*-

"""Top-level package for MOPAC step."""

__author__ = """Paul Saxe"""
__email__ = 'psaxe@molssi.org'
__version__ = '0.1.0'

# Bring up the classes so that they appear to be directly in
# the package.

from mopac_step.mopac_step import MOPACStep  # nopep8
from mopac_step.mopac import MOPAC  # nopep8
from mopac_step.tk_mopac import TkMOPAC  # nopep8
from mopac_step.energy_step import EnergyStep  # nopep8
from mopac_step.energy import Energy  # nopep8
from mopac_step.tk_energy import TkEnergy  # nopep8
from mopac_step.optimization_step import OptimizationStep  # nopep8
from mopac_step.optimization import Optimization  # nopep8
from mopac_step.tk_optimization import TkOptimization  # nopep8
from mopac_step.ir_step import IRStep  # nopep8
from mopac_step.ir import IR  # nopep8
from mopac_step.tk_ir import TkIR  # nopep8
from mopac_step.thermodynamics_step import ThermodynamicsStep  # nopep8
from mopac_step.thermodynamics import Thermodynamics  # nopep8
from mopac_step.tk_thermodynamics import TkThermodynamics  # nopep8

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
        'description': 'Add hydrogen atoms (intended for use with organic compounds)',  # nopep8
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
        'description': 'Print final bond-order matrix, including bonds to hydrogen',  # nopep8
    },
    'ALLVEC': {
        'description': 'Print all vectors (keywords vectors also needed)',
    },
    'ALT_A=A': {
        'description': 'In PDB files with alternative atoms, select atoms A',
    },
    'ALT_R=A': {
        'description': 'Deleted. All inserted residues are automatically recognized',  # nopep8
    },
    'ANGSTROMS': {
        'description': 'Input geometry is in Angstroms',
    },
    'AUTOSYM': {
        'description': 'Symmetry to be imposed automatically',
    },
    'AUX': {
        'description': 'Output auxiliary information for use by other programs',  # nopep8
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
        'description': 'In a protein, explicitely define the letters of chains.',  # nopep8
    },
    'CHECK': {
        'description': 'Report possible faults in input geometry',
    },
    'CHARGE=n': {
        'description': 'Charge on system = n (e.g. NH4 = +1)',
    },
    'CHARGES': {
        'description': 'Print net charge on system, and all charges in the system',  # nopep8
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
        'description': 'Write details of the solvent accessible surface to a file',  # nopep8
    },
    'CUTOFP=n.nn': {
        'description': 'Madelung distance cutoff is n .nn Angstroms',
    },
    'CUTOFF=n.nn': {
        'description': 'In MOZYME, the interatomic distance where the NDDO approximation stops',  # nopep8
    },
    'CYCLES=n': {
        'description': 'Do a maximum of n steps',
    },
    'CVB': {
        'description': 'In MOZYME. add and remove specific bonds to allow a Lewis or PDB structure.',  # nopep8
    },
    'DAMP=n.nn': {
        'description': 'in MOZYME. damp SCF oscillations using a factor of n.nn',  # nopep8
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
        'description': 'Use Davidson-Fletcher-Powell method to optimize geometries',  # nopep8
    },
    'DISEX=n.nn': {
        'description': 'Distance for interactions in fine grid in COSMO',
    },
    'DISP': {
        'description': 'Print the hydrogen bonding and dispersion contributions to the heat of formation',  # nopep8
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
        'description': 'Use the EigenFollowing routine for geometry optimization',  # nopep8
    },
    'EIGEN': {
        'description': 'Print canonical eigenvectors instead of LMOs in MOZYME calculations',  # nopep8
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
        'description': 'In RHF open and closed shell, force M.O. n to be filled',  # nopep8
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
        'description': 'Calculate vibrational frequencies for atoms in a transition state',  # nopep8
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
        'description': 'Exit when gradient norm drops below n .n kcal/mol/Angstrom',  # nopep8
        'value optional': False,
        'value', 'float',
    },
    'GRADIENTS': {
        'description': 'Print all gradients',
    },
    'GRAPH': {
        'description': 'Generate unformatted file for graphics',
    },
    'GRAPHF': {
        'description': 'Generate formatted file for graphics suitable for  Jmol and MOPETE.',  # nopep8
    },
    'HCORE': {
        'description': 'Print all parameters used, the one-electron matrix, and two-electron integrals',  # nopep8
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
        'value' 'float',
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
        'description': 'Print localized orbitals.  These are also called Natural Bond Orbitals or NBO',  # nopep8
    },
    'LOCATE-TS': {
        'description': 'Given reactants and products, locate the transition state connecting them',  # nopep8
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
        'description': 'Reduce the size of the output by only printing specified atoms',  # nopep8
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
        'description': 'Incorporate environmental effects in the QM/MM approach',  # nopep8
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
        'description': 'Use the Localized Molecular Orbital method to speed up the SCF',  # nopep8
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
        'description': 'In excited state COSMO calculations, set the value of N**2',  # nopep8
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
        'description': 'Ignore all lines except ATOM, HETATM, and TER in PDB files',  # nopep8
    },
    'NOGPU': {
        'description': 'Do not use GPU acceleration',
    },
    'NOLOG': {
        'description': 'Suppress log file trail, where possible',
    },
    'NOMM': {
        'description': 'Do not use molecular mechanics correction to CONH bonds',  # nopep8
    },
    'NONET': {
        'description': 'NONET state required',
    },
    'NONR': {
        'description': 'Do not use Newton-Raphson method in EF',
    },
    'NOOPT': {
        'description': 'Do not optimize the coordinates of all atoms (see OPT-X)',  # nopep8
    },
    'NOOPT-X': {
        'description': 'Do not optimize the coordinates of all atoms of type X',  # nopep8
    },
    'NOREOR': {
        'description': 'In symmetry work, use supplied orientation',
    },
    'NORESEQ': {
        'description': 'Suppress the default re-sequencing of atoms to the PDB sequence',  # nopep8
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
        'description': 'In COSMO, use the old Solvent Accessible Surface calculation',  # nopep8
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
        'description': 'Optimize coordinates of all atoms within n.nn Ångstroms of atoms labeled "text"',  # nopep8
    },
    'OUTPUT': {
        'description': 'Reduce the amount of output (useful for large systems)',  # nopep8
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
        'description': 'Print the pKa for ionizable hydrogen atoms attached to oxygen atoms',  # nopep8
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
        'description': "Use the PM6 Hamiltonian with Grimme's corrections for dispersion",  # nopep8
    },
    'PM6-DH+': {
        'description': 'Use the PM6 Hamiltonian with corrections for dispersion and hydrogen-bonding',  # nopep8
    },
    'PM6-DH2': {
        'description': 'Use the PM6 Hamiltonian with corrections for dispersion and hydrogen-bonding',  # nopep8
    },
    'PM6-DH2X': {
        'description': 'Use PM6 with corrections for dispersion and hydrogen and halogen bonding',  # nopep8
    },
    'PM6-D3H4': {
        'description': "Use PM6 with Řezáč and Hobza's D3H4 correction",
    },
    'PM6-D3H4X': {
        'description': "Use PM6 with Brahmkshatriya, et al.'s D3H4X correction",  # nopep8
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
        'description': 'Number of points in first direction in grid calculation',  # nopep8
        'value optional': False,
        'value': 'integer',
    },
    'POINT2=n': {
        'description': 'Number of points in second direction in grid calculation',  # nopep8
        'value optional': False,
        'value': 'integer',
    },
    'POLAR': {
        'description': 'Calculate first, second and third order polarizabilities',  # nopep8
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
        'description': 'Incorporate environmental effects in the QM/MM approach',  # nopep8
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
        'description': 'In MOZYME geometry optimizations, only use atoms being optimized in the SCF',  # nopep8
    },
    'RECALC=n': {
        'description': 'In EF, recalculate Hessian every n steps',
        'value optional': False,
        'value': 'integer',
    },
    'RE-LOCAL': {
        'description': 'At the end of MOZYME calculation, re-localize the LMOs',  # nopep8
    },
    'RE-LOCAL=n': {
        'description': 'During and at end of MOZYME calculation, re-localize the LMOs',  # nopep8
        'value optional': True,
        'value': 'integer',
    },
    'RELSCF': {
        'description': 'Default SCF criterion multiplied by n',
    },
    'REORTHOG': {
        'description': "In MOZYME, re-orthogonalize LMO's each 10 SCF calculations.",  # nopep8
    },
    'RESEQ': {
        'description': 'Re-arrange the atoms to match the PDB convention',
    },
    'RESIDUES': {
        'description': 'Label each atom in a polypeptide with the amino acid residue.',  # nopep8
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
        'description': 'In MOZYME, some π bonds are explicitly set by the user',  # nopep8
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
    #     'description': 'Send a command to MOPAC to make a restart and density file, then stop.',  # nopep8
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
        'description': 'In L-BFGS optimization, use fixed step of length n .nn',  # nopep8
    },
    'SLOPE': {
        'description': 'Multiplier used to scale MNDO charges',
    },
    'SMOOTH': {
        'description': 'In a GRID calculation, remove artifacts caused by the order in which points are calculated',  # nopep8
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
        'description': 'Define starting residue numbers in a protein, if different from the default',  # nopep8
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
        'description': 'Print characters of eigenvectors and print number of I.R.s',  # nopep8
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
        'description': 'Set the number of threads to be used in parallelization to n',  # nopep8
    },
    'TIMES': {
        'description': 'Print times of various stages',
    },
    'T-PRIORITY=n.nn': {
        'description': 'Time takes priority in DRC',
    },
    'TRANS=n': {
        'description': 'The system is a transition state (used in thermodynamics calculation)',  # nopep8
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
        'description': 'Van der waals radius for atoms in COSMO defined by user',  # nopep8
    },
    'VDWM(text)': {
        'description': 'Van der waals radius for atoms in MOZYME defined by user',  # nopep8
    },
    'VECTORS': {
        'description': 'Print final eigenvectors',
    },
    'VELOCITY': {
        'description': 'Supply the initial velocity vector in a DRC calculation',  # nopep8
    },
    'WILLIAMS': {
        'description': 'Use Williams surface',
    },
    'X-PRIORITY=n.nn': {
        'description': 'Geometry changes take priority in DRC',
    },
    'XENO': {
        'description': 'Allow non-standard residues in proteins to be labeled.',  # nopep8
    },
    'XYZ': {
        'description': 'Do all geometric operations in Cartesian coordinates',
    },
    'Z=n': {
        'description': 'Number of mers in a cluster',
    },
}
