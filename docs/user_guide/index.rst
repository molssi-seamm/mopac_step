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


Index
=====

* :ref:`genindex`
