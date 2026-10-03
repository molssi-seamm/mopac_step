.. _user-guide:

**********
User Guide
**********
The XXXX plug-in ...

..
   The following sections cover accessing and controlling this functionality.

   .. toctree::
      :maxdepth: 2
      :titlesonly:

Settings that depend on each other
==================================

Which settings apply depends on others: UHF and MOZYME only for the Hartree-Fock
calculation, the CI settings only for CI calculations, the COSMO settings only with
COSMO, and the cell's pressure and shear only when the cell is optimized. The step's
dialogs show only the settings that apply with the current choices, and the same rules
are used when a flowchart is built or edited without the editor (``seamm-flowchart`` or
SEAMM's MCP server): a setting that would have no effect is refused, with the reason,
and a value that contradicts another is refused too. See "Flowcharts without the editor"
in SEAMM's user guide.

The **Structure** to start from is shown in the dialog: by default the first sub-step
starts from the incoming structure and the others from the previous sub-step's
(``current``); ``initial`` always uses the incoming one. Force Constants works with
MOZYME but does no follow-up calculation, so it does not offer that setting.


Rerunning a job
===============

MOPAC runs through SEAMM's task layer, in the step's directory so that its output can
be watched while it runs. The task layer keeps a record of each MOPAC calculation in
``tasks/manifest.json`` in the step's directory, with a ``tasks/mopac/DONE`` file once
it has finished.

When a job is run again in the same directory -- after it was stopped, lost its node,
or ran out of time:

* a MOPAC step that had completed is skipped, as before: its ``success.dat`` file
  says so, and its results are read from the files it left, whatever its input now;
* a MOPAC calculation that had finished but whose step had not completed (the job
  stopped just after MOPAC ended), and the Lewis structure calculation, are not
  repeated if their input is unchanged; their results are read from the files they
  left;
* a calculation that did not finish -- it failed, or the job was stopped while it was
  running -- is run again, up to three attempts in all; after that the step stops with
  a message saying so. Deleting its entry in ``tasks/manifest.json``, or changing its
  input, lets it run again. If the job was killed outright, a MOPAC process from the
  earlier run may still be running; the rerun stops it first.

To recompute a completed MOPAC step, delete its ``success.dat``.


MOPAC as a model chemistry
==========================

Steps that set up a *model chemistry* and evaluate it at many structures -- the
**Energy** step, the **Dimer Builder**'s contact search, **Normal Mode Sampling**,
LAMMPS QM-MD -- use MOPAC through a **Model Chemistry** step (e.g. ``MOPAC:PM7``), with
no settings in the MOPAC step itself. On this machine they keep one MOPAC running as an
`MDI <https://molssi-mdi.github.io/MDI_Library/>`_ engine and pass it the structures
one after another, which suits MOPAC's very short calculations. When the job's target
sends its calculations to a cluster queue, each molecule instead runs there as a
separate MOPAC calculation, and a rerun reuses the ones that had finished.

The energy is the heat of formation either way, and the gradients agree. Periodic and
open-shell structures always use the MDI engine; on a queue target where MOPAC is not
installed on the job's own machine, such a structure is reported as failed, with the
reason, and the others finish.

For a periodic structure the engine also returns the stress, as a pressure: positive
when the system pushes outward (the opposite of MOPAC's own tensile-positive stress).
MOPAC's model chemistries declare this, so steps that use the stress, such as the MBE
step's periodic levels, convert it correctly.


Index
=====

* :ref:`genindex`
