.. _notes-mopac-model-chemistry-metadata:

================================================================================
Notes: MOPAC Metadata for the Model Chemistry Step (get_model_chemistry_options)
================================================================================

:Date: 2026-06-22
:Status: Classmethod drafted and corrected; metadata for AM1/RM1/PM3/
   MNDO/MNDOD added; PM6/PM7 element coverage corrected against real
   source; Sparkle/lanthanide distinction discovered and documented;
   tests written and dry-run against the real combined data. Not yet
   applied to the live ``mopac_step`` repository -- these are patches
   to merge, not a description of completed work in the codebase.
:Connects to: the Model Chemistry Step campaign, documented in this
   project's notes as :ref:`plan-model-chemistry-step` (drafted
   2026-06-20) and, per Paul, also published in the campaigns section
   of the molssi-seamm.github.io developer guide under today's date.
   This note was written without direct access to that rendered build
   (a local file path, not reachable from here) -- the connection
   below is drawn from this project's own copy of the plan, not from
   re-reading the published version.

.. contents:: Contents
   :depth: 2
   :local:


How this fits into the campaign
==================================

:ref:`plan-model-chemistry-step` laid out a metadata protocol --
``get_model_chemistry_options(periodic_only, mdi_only)`` -- that every
program-step package implementing model chemistries would expose, so
the (still to be built) Model Chemistry Step's dialog and
``lammps_step``'s MDI launch logic could both query "what can this
program provide" uniformly. The plan included a worked sketch of this
classmethod for MOPAC, built against ``mopac_step``'s real
``metadata["computational models"]`` structure as it existed at the
time -- ten parameterizations (PM7, PM7-TS, PM6, PM6-ORG, and the six
PM6 dispersion/H-bond correction variants), with the explicit
observation that AM1 and RM1 were absent from that structure entirely,
not just unconfirmed for periodicity.

This note documents closing that gap and the corrections that followed
from doing so properly rather than guessing -- this is Phase 2 of the
plan's phased breakdown ("confirm the AM1/RM1 periodic flags ... land
the classmethod for real"), plus some unplanned but necessary detours
once real source data was available to check against.


What was done, in order
==========================

1. Drafted ``MOPACStep.get_model_chemistry_options()`` against the
   metadata structure as it stood, with ``_MDI_CAPABLE_METHODS`` (the
   six methods in ``mopactools.api.MopacSystem.model_dict``) and
   ``_MDI_PERIODIC_VALIDATED`` (the three -- PM7, PM6-ORG, PM6 --
   actually run periodic via MDI and confirmed this week, per
   :ref:`notes-qm-mdi-engines-validation`) as class attributes.
2. Corrected the class name used in the draft (``MOPACStep``, not
   ``MopacStep`` as first guessed) and the import style
   (``mopac_step.metadata``, matching the file's own existing
   convention) against the real uploaded ``mopac_step`` bundle.
3. Drafted metadata entries for AM1, RM1, PM3, MNDO, and MNDOD,
   initially from general knowledge -- explicitly flagged at the time
   as unverified, since none of it had been checked against any real
   source.
4. Given MOPAC's actual parameter source files (``src/models/
   parameters_for_*_C.F90``), re-extracted real element coverage for
   all five by parsing each file's "Data for Element" header comments
   and excluding non-element pseudo-atom entries (MOPAC's "Capped
   bond" dummy atoms). This changed every one of the five from
   guessed to verified, and incidentally revealed that RM1's parameter
   table includes the full lanthanide series (La-Lu) -- unexpected,
   not predicted from general knowledge of the original 2006 RM1
   paper's 10-element scope.
5. At Paul's request, applied the same direct-extraction technique to
   the *existing*, previously-unquestioned PM6/PM7 entries (elements
   "1-60,62-83"). This is where the real correction landed: actual
   coverage is "1-57,71-83,85,87,90,97" -- the old value understated
   the lanthanide gap by an order of magnitude (one element, Pm,
   thought missing; thirteen, Ce-Yb, actually missing). Also surfaced
   a parameter table entry at Z=98 labeled "Mithril" in the source
   comment (Tolkien's fictional metal; Z=98 is actually Californium) --
   excluded from the verified range pending confirmation of whether
   this is real, mislabeled Californium data or a non-functional
   placeholder.
6. Paul identified the actual explanation for the PM6/PM7 lanthanide
   gap from ``mopac_step``'s own ``mopac.py``: Ce-Yb are only
   representable via the SPARKLES point-charge model (no real NDDO
   parameters exist for them at all), while La and Lu have genuine
   parameters and may *optionally* use SPARKLES (geometry vs. energy
   tradeoff). This is a deliberate design choice, not a coverage gap --
   reclassified accordingly rather than just re-including the
   lanthanides in the plain "elements" string, which would have erased
   the real distinction between full electronic treatment and the
   cruder point-charge approximation.
7. Added a new ``sparkle_elements`` metadata field (currently
   documented only for PM7, PM7-TS, PM6) to carry this distinction
   without conflating it with genuine NDDO coverage. Deliberately did
   *not* add it to RM1, since RM1's lanthanide parameters are real NDDO
   data for the full range, not Sparkle-only -- a materially different
   situation despite both involving the same block of elements.
8. While drafting tests for the classmethod, caught that the
   classmethod itself never surfaced ``sparkle_elements`` in its
   returned dict -- the field was added to raw metadata after the
   classmethod was first drafted, and nothing had gone back to wire it
   through. Fixed and re-verified.
9. Wrote nine tests covering: full enumeration against raw metadata,
   the MDI-only and periodic-only filters independently and combined,
   the PM6-D3H4 trap specifically (MDI-capable but not periodic-safe),
   a non-MDI method's launch info being correctly empty, AM1/RM1
   appearing now that real entries exist for them, the model-chemistry
   string format, the sparkle_elements field appearing only where
   documented, and every option having a non-empty elements string.
   All nine dry-run successfully against the actual combined metadata
   and classmethod logic (not just asserted to be correct).


Open questions surfaced, not resolved here
=============================================

* **Whether SPARKLES is reachable via the MDI path at all.**
  ``mopactools``'s ``MopacSystem`` struct, as reviewed so far, has no
  free-text keyword field -- only structured attributes (model,
  charge, spin, atom, coord, lattice). The traditional ``mopac_step``
  batch path injects ``"SPARKLES"`` as extra keyword text into the
  ``.mop`` file; no equivalent has been found in the MDI path. If none
  exists, any system containing La, Lu, or Ce-Yb may be entirely
  unrunnable via ``mopac_mdi.py``, independent of the ``periodic_mdi``
  flag. Not resolved -- needs a direct check against the full
  ``mopactools`` API rather than inference from the parts already
  reviewed.
* **Z=98 "Mithril" entry** -- real (mislabeled) data or a non-functional
  placeholder, not determined.
* **PM6-ORG and the six PM6 correction variants (D3, DH+, DH2, DH2X,
  D3H4, D3H4X)** still carry their original, unverified element ranges.
  ``PM6-ORG``'s own parameter file exists in the bundle already
  provided and could be checked the same way PM6/PM7 were. The
  correction variants have no separate parameter file in what's been
  reviewed -- their core-electronic coverage should match PM6's
  corrected range, but the correction term itself (dispersion/H-bond
  coefficients) plausibly covers a narrower subset that nothing
  reviewed so far actually specifies.
* None of the above changes ``_MDI_PERIODIC_VALIDATED``. That set
  remains exactly ``{PM7, PM6-ORG, PM6}`` -- empirical, run-and-checked
  status, unaffected by any metadata correction in either direction.


Files affected (patches drafted, not yet merged)
====================================================

* ``mopac_step/metadata.py`` -- ``metadata["computational models"]``,
  extended and corrected as described above.
* ``mopac_step/mopac_step.py`` -- new ``get_model_chemistry_options()``
  classmethod plus its two supporting class attributes.
* ``tests/test_get_model_chemistry_options.py`` -- new test file.


References
==========

* :ref:`plan-model-chemistry-step`
* :ref:`notes-qm-mdi-engines-validation`
* MOPAC parameter source: ``src/models/parameters_for_*_C.F90``
  (uploaded as ``parameters.md``)
* ``mopac_step/mopac.py``'s SPARKLES handling (the source of the
  Sparkle/lanthanide explanation in this note)
