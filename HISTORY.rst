=======
History
=======
2025.5.7 -- Bugfix and reference for PM6-ORG
   * Added the reference for PM6-ORG
   * Fixed a bug that was resulting in deleting atoms from other configurations when
     updating the structure after minimization.
     
2025.3.6 -- Updated the installer and added timing information
   * Updated the MOPAC installer to work with recent changes in the SEAMM installer.
   * Saving timing information to ~/SEAMM/timing/mopac.csv for tools to predict the
     length of calculations.
   * Corrected a small issue with the RMSD calculations.

2025.2.24 -- Changed the structure option to "Discard the structure".

2025.2.23 -- Added RMSD and ability to discard the optimized stucture
   * Added the RMSD between the initial and final structures during optimization, make
     the RMSD, maximumim displacement, and the index of the maximally displaced atom
     results that can be tabulated and stored.
   * Added an option to discard the structure from an optimization.
     
2024.12.9 -- Add the force constants as a property.
   * Add the force constants as a property of the configuration when running
     thermodynamics, IR, or force constants calculations.
     
2024.10.15 -- Bugfix: error if used in a loop and previous directories deleted.
   * The code crashed if called with a loop in the flowchart, and the last directory of
     a previous loop iteration was deleted before running the next iteration.
     
2024.8.21 -- Bugfix for PM7-TS and optimization, GUI clean up for CI calculations.
  * Calculations using PM7-TS do not write information to the AUX file, so added code to
    get the energy from the output file.
  * For optimizations, the option for the frequency of calculating the force constants
    and the maximum radius of convergence were missing from the GUI for the EF
    method. The frequency also was not being correctly handled in the input to MOPAC.
  * The GUI for using CI calculations was cleaned up.
    
2024.8.17 -- Added CI calculations and better handling of transition states
  * Added ability to do the various types of CI calculations that MOPAC supports.
  * Improved the handling of TS calculations and added NLLSQ and SIGMA methods in
    the optimization step.
  * Added option to correctly handle transition states in the thermodynamics step and
    improved the output to include the imaginary and low-lying frequencies.
    
2024.7.29 -- Bugfix in bond analysis for atoms and mopac.ini
  * Fixed a bug in the bond analysis that caused the code to crash for calculations on
    atoms. 
  * Fixed a bug in the mopac.ini file created if it did not exists that caused the code
    to crash when the calculation was run.

2024.5.14 -- Added output of energy & gradients to JSON
   * To support the Energy Scan step.
     
2024.3.17 -- Updated installation
  * Updated the installation to reflect the new way to install SEAMM plug-ins to support
    both Conda and Docker
    
2024.1.16 -- Added support for containers.
  * Added access to the new PM6-ORG parameterization and made it the default, though PM7
    is still preferred for materials simulation. PM6-ORG handle organic and biomolecules
    well.
  * Made the Lewis structure analysis more robust and added information to the output.
  * Provided an option for the Lewis structure calculation to set the charge of the
    system to that calculaed by the Lewis structure.
  * Added support for containers
  * Made default to run serially, since parallel doesn't provide much benefit.
  * Fixed bug in analysis if optimization doesn't converge.

2023.12.18 -- Added readonly flag
  * Added a flag to prepare the input but not run the calculation.
    
2023.11.15 -- More updates for v2022.1.0
  * Added PM6-ORG Hamiltonian to options
  * Added other new data types for the AUX file.
    
2023.11.14 -- Updated for MOPAC v2022.1.0
  * MOPAC v2022.1.0 added GRADIENT_NORM_UPDATED to the AUX file. This updates adds it to
    the results recognized by the plug-in
    
2023.10.30 -- Updated to standard structure handling
  * Adds IUPAC names, InChI and InChIKey as possible names for configurations
  * Cleaned up output to be properly indented and laid out.
    
2023.8.30 -- Support for spacegroup symmetry

2023.7.27 -- Bugfix: printing bond order info
  * If the bond orders were printed but not used on the system, the code crashed.
    
2023.7.26 -- Added output of bond orders
  * Also added capability to use the bond orders to put bond multiplicities on the
    structure.
    
2023.7.24 -- Bugfix in Lewis structure with bond orders
  * Major issue in getting the bonds from the Lewis structure where the atoms and bond
    orders were mixed up.
    
2023.6.5 -- Bugfix working around MOPAC problem
  * MOPAC is not consistent about putting end of file and end of program markers in the
    AUX file. This caused carashed in SEAMM, which this fixes until MOPAC can be
    corrected.
    
2023.4.24 -- Bugfixes for Lewis structure
  * Correctly handle periodic systems in Lewis structure.
  * Fixed and issue with the Lewis structure GUI not displaying all the widgets.
    
2023.3.31 -- Bugfix
  Lewis structure could reference a variable before it was set, and crash.
  
2023.3.15 -- Bugfix
  A copy of the input and output files for MOPAC was inadvertently written to the main
  job directory. This has been fixed.
  
2023.2.13 -- Added Lewis Structure step
  Provide access to the 'LEWIS' keyword in MOPAC for generating the Lewis dot
  structure. This step also allows assigning the bonds of the system using either the
  connectivity or the Lewis structure.
  
2022.11.18 -- Printing spins on atoms
  Fixed an oversight that preventing printing spins on the atoms, and storing them on
  the structure. Also increased the precision of the AUX file so have coordinates to
  seven decimals, which should maintain symmetry better.
  
2022.11.4 -- Added ForceConstant substep
  Calculates and writes the Hessian (force constant) matrix to disk. Works for both
  molecular and periodic systems, and provides an option to control which parts of the
  Hessian matrix are written. Defaults to the full matrix. Also provides options to
  control the units of the output, with default of N/m for the atom block of the
  Hessian as well as the atom-cell off-diagonal block, and GPa for the cell block.

2021.2.11 (11 February 2021)
----------------------------

* Updated the README file to give a better description.
* Updated the short description in setup.py to work with the new installer.
* Added keywords for better searchability.

2021.2.4 (4 February 2021)
--------------------------

* Updated for compatibility with the new system classes in MolSystem
  2021.2.2 release.

2020.12.5 (5 December 2020)
---------------------------

* Internal: switching CI from TravisCI to GitHub Actions, and in the
  process moving documentation from ReadTheDocs to GitHub Pages where
  it is consolidated with the main SEAMM documentation.

2020.11.2 (2 November 2020)
---------------------------

* Updated to be compatible with the new command-line argument
  handling.

2020.10.7 (7 October 2020)
----------------------------

* Updated to handle citations using the new framework.

2020.9.29 (29 September 2020)
-----------------------------

* Updated to be compatible with the new system classes in MolSystem.

2020.8.1 (1 August 2020)
------------------------

* Fixed bug caused by coordinates being strings, not numbers, in some
  cases.

2020.7.0 (23 July 2020)
-----------------------

* Improved the text output when running.

0.9 (15 April 2020)
-------------------

* General bug fixes and cleanup of the code.

0.7.0 (17 December 2019)
------------------------

* Consolidating minor changes and making a uniform release at year's
  end.

0.5.1 (29 August 2019)
----------------------

* First version that runs correctly and generates output.

0.2.0 (13 August 2019)
----------------------

* First release on PyPI.
