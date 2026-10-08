=======
History
=======
2026.10.8 -- The cost model counts geometry cycles and scales each regime separately
    * ``TIMING_SPEC`` counts an optimization's work in geometry cycles rather than
      SCF runs, which MOPAC reports as 1 or 2 for an optimization of any length, so
      optimizations were predicted about ten times too short. It also names the
      regime (``slope_by``), so MOZYME and the traditional SCF each get their own
      size exponent. On ChemAI's benchmark every MOPAC run is now predicted within
      a factor of 2 (from 79%). Needs seamm-exec 2026.10.8 for the regimes; older
      versions ignore it.

2026.10.7 -- The step declares what its cost model is made of, and its benchmark
    * Bugfix: a MOPAC model-chemistry task's analysis failed under seamm-exec
      2026.10.7 (``analyze_task() got an unexpected keyword argument 'task'``):
      it now takes the task and, like the step's own runs, records the run's
      timing from it.
    * ``mopac_step.TIMING_BENCHMARK`` tells seamm_exec's seed benchmark what to run
      for MOPAC: eight molecules from water to a 3000-atom alkane with PM7 and
      PM6-ORG, as energies and optimizations, both regimes (MOZYME and the
      traditional SCF) from 300 atoms, with size limits per tier; on one core.
    * ``mopac.TIMING_SPEC`` -- basis functions and atoms as size variables, the
      Hamiltonian and regime as the method class, the task, SCFs as the unit, no
      parallel exponent -- is passed when a run is recorded (seamm-exec 2026.10.6.1
      writes it beside the records), so the cost model is fitted from the step's own
      description rather than a table in seamm-exec.
    * Removed the support for running MOPAC in a Docker container, and the Docker
      image recipe, which were no longer used or maintained.
    * Requires Python 3.12 and seamm-exec 2026.10.6.1.

2026.10.6 -- Timing records that a cost model can be fitted to
    * Each MOPAC run appends a record to ``~/.seamm.d/timing/mopac.csv`` through
      ``seamm_exec.record_task_timing`` -- the machine class, cores, wall time and
      outcome from the task layer, and the descriptors of the calculation: the
      Hamiltonian, the kind of task (energy, gradient, optimization, force
      constants), the regime actually used (``mozyme`` or ``scf``, read from the
      output, since MOPAC may not use MOZYME even when asked), the atoms, heavy
      atoms, basis functions, electrons, charge and multiplicity, the SCFs and
      geometry cycles, and MOPAC's own job time. This replaces the step's own CSV
      (SMILES, formula and keyword text, hostname), which grew without bound. See
      seamm_exec's campaign of 2026-10-05.
    * Requires seamm-exec 2026.10.6.
2026.10.5 -- Bugfix: rerun MOPAC when its input changed; the MDI engine's Python
    * A MOPAC calculation is reused from an earlier run in the same directory only if
      its input is unchanged; a leftover success marker no longer skips a changed
      calculation.
    * The MDI engine is started with its conda environment's own Python, found by
      path (or asked of conda), so a virtual environment earlier on the PATH cannot
      be picked up instead (#161).
2026.10.3.2 -- Declare the sign of the stress from MOPAC
    * MOPAC's model chemistries now state that the stress they return for a periodic
      system is a pressure (positive when the system pushes outward), so steps such as
      the MBE step can use MOPAC's stress for a periodic cell.
2026.10.3.1 -- MOPAC calculations for many structures on a cluster queue
    * With a MOPAC model chemistry, the Energy step, the Dimer Builder and Normal Mode
      Sampling send each molecule to the cluster as a separate MOPAC calculation when
      the job's target sends its calculations to a queue; a rerun reuses the ones
      that had finished. On this machine they keep using MOPAC's MDI engine.
    * The energy is the heat of formation, as from the MDI engine, and the gradients
      agree with the engine's. Periodic and open-shell structures always use the MDI
      engine.
    * How MOPAC is run is worked out on the machine that runs it, from that machine's
      ``mopac.ini``, including conda and environment-module installations.
    * Requires seamm-exec 2026.10.3 or later.

2026.10.3 -- Bugfix: forces from the MOPAC MDI engine were 3.57 times too large
    * Driven over MDI (the Energy step's gradients, LAMMPS QM/MD with a MOPAC
      model chemistry, and Normal Mode Sampling's finite-difference Hessian),
      MOPAC returned forces 3.57 times too large: the conversion from kcal/mol/Å
      to hartree/bohr multiplied by bohr/Å instead of Å/bohr. Energies were
      right. Results computed with MOPAC over MDI since 2026-06-23 that used the
      forces -- gradients, QM/MD trajectories, MOPAC normal-mode frequencies
      (about 1.89 times too high) -- should be recomputed.
    * A test now compares the engine's forces with a finite difference of its
      energies.

2026.10.2 -- MOPAC runs as a task; failures are reported with the reason
    * MOPAC now runs through SEAMM's task layer, still in the step's directory so its
      output can be watched as it runs. A failed run is now reported with the reason,
      for example its return code.
    * Rerunning a job in the same directory reuses a MOPAC calculation that had
      finished with the same input. A MOPAC step that had completed was already skipped
      on a rerun; now the Lewis structure calculation, and a calculation that finished
      just before the job was stopped, are reused too.
    * Otherwise nothing changes: the output files are where they always were and the
      results are the same. The record of the calculations is in
      ``tasks/manifest.json`` in the step's directory.
    * Requires seamm-exec 2026.10.2 or later.

2026.10.1 -- Settings that depend on each other; MOZYME force constants
    * The dialogs show only the settings that apply with the current choices, and SEAMM's
      flowchart tools use the same rules: UHF and MOZYME only for Hartree-Fock; the CI
      settings only for CI calculations; the COSMO settings only with COSMO; the
      gradient criterion, Hessian recalculation, trust radius, pressure and shear only
      where they apply.
    * The structure to start from is now shown in the dialog. Bugfix: choosing
      ``initial`` after the first sub-step raised an UnboundLocalError.
    * Bugfix: force constants with MOZYME raised NotImplementedError. MOPAC's FORCE works
      with MOZYME, so only the follow-up calculation is dropped there.
    * Bugfix: two errors in the descriptions printed in the output.
    * Documented in the user guide. Needs seamm 2026.10.1.
    * Internal: CI now installs the package's declared dependencies with uv rather than
      a conda test environment; seamm-exec, which it uses, is now declared.

2026.7.27 -- Bugfix: run MOPAC single-threaded when driven over MDI
    * When another step drove MOPAC through the MDI engine (QM/MD, and the Dimer
      Builder's energy-based contact), MOPAC was not held to a single thread the
      way a normal MOPAC step is, so it spread across all available cores. Since
      these drivers issue many small calls one after another, the extra threads
      only oversubscribed the cores and could slow the run. The MDI engine now
      pins MOPAC -- and the linear-algebra libraries it calls -- to a single
      thread, matching the normal MOPAC step. Set ``OMP_NUM_THREADS`` in the
      environment to override.

2026.7.6 -- Quieter MDI engine logging
    * The MDI engine used to drive MOPAC from other steps (QM/MD, and the Dimer
      Builder's energy-based contact) logged its connection, setup, and timing
      lines at INFO, which cluttered the driving step's output. These are now at
      DEBUG, so normal runs are quiet.

2026.3.1 -- Internal: switching from deprecated library pkg_resources to importlib

2025.12.21 -- Fixed an issue with periodic systems and lattice size
    * Mopac is sensitive to where the atoms are in periodic systems, and stops with a
      warning if the atoms are too far out of the unit cell. SEAMM now avoids this by
      translating the atoms into the unit cell before running MOPAC.
    * Added error checking for a bond matrix with incompatible size to the number of
      atoms and print a warning but continue.
    * For periodic systems, avoid calculating the RMS and maximum displacement of atoms,
      which is not well-defined and also causes problems in the current code.

2025.12.20 -- Added control over cell optimization for periodic systems
    * Added control over whether to shear the cell when optimizing, and also to couple
      the diagonal directions so they have identical values.
    * Enhanced the output to show changes in the cell parameters, volume, and denisty
      and also to print the stress.
    * Added an option to save the gradients to the configuration.

2025.10.22 -- Bugfix: corrected incorrect keywords
    * Some of the keywords in the metadata had '=xxx' as part of the keyword. This was
      incorrect and stripped leaving just the keyword.
      
2025.5.7.1 -- Bugfix: typo in PM6-ORG reference BibTeX

2025.5.7 -- Bugfix and added the reference for PM6-ORG
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
