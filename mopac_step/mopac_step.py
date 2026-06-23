# mopac_step/mopac_step.py
# -*- coding: utf-8 -*-

"""Main module."""

import mopac_step


class MOPACStep(object):
    my_description = {
        "description": "Setup and run MOPAC",
        "group": "Simulations",
        "name": "MolSSI MOPAC",
    }

    def __init__(self, flowchart=None, gui=None):
        """Initialize this helper class, which is used by
        the application via stevedore to get information about
        and create node objects for the flowchart
        """
        pass

    def description(self):
        """Return a description of what this extension does"""
        return MOPACStep.my_description

    def create_node(self, flowchart=None, **kwargs):
        """Return the new node object"""
        return mopac_step.MOPAC(flowchart=flowchart, **kwargs)

    def create_tk_node(self, canvas=None, **kwargs):
        """Return the graphical Tk node object"""
        return mopac_step.TkMOPAC(canvas=canvas, **kwargs)

    # Patch to mopac_step/mopac_step.py -- add to the MOPACStep class,
    # alongside description()/create_node()/create_tk_node().
    #
    # Revision 2026-06-22: now surfaces "sparkle_elements" in the returned
    # dict (added to the raw metadata for PM7/PM7-TS/PM6ants on 2026-06-22, but
    # the first draft of this classmethod predated that field and never
    # passed it through -- caught while writing tests, fixed here).

    # mopactools.api.MopacSystem.model_dict's scope -- see mopac_mdi.py's
    # --method choices. This is the authoritative source for what's
    # actually reachable via MDI; update here if mopactools changes.

    _MDI_CAPABLE_METHODS = {"PM7", "PM6-D3H4", "PM6-ORG", "PM6", "AM1", "RM1"}

    # Methods actually run periodic via MDI and confirmed working, per
    # NOTES_qm_mdi_engines_validation.rst. Cross-checked against the real
    # metadata["computational models"] entries -- PM7, PM6, and PM6-ORG are
    # the only three with both periodic=True there AND an actual validated
    # periodic MDI run this week. PM6-D3H4 is MDI-capable but deliberately
    # excluded: its own metadata entry says periodic=False, and MOPAC's
    # documentation confirms D3H4 does not work under periodic boundary
    # conditions at all.

    _MDI_PERIODIC_VALIDATED = {"PM7", "PM6-ORG", "PM6"}

    @classmethod
    def get_model_chemistry_options(cls, periodic_only=False, mdi_only=False):
        """Return the model chemistries MOPAC can provide.

        NOTE: only covers methods present in metadata["computational
        models"]. As of 2026-06-22 this includes PM7, PM7-TS, PM6,
        PM6-ORG, PM6-D3, PM6-DH+, PM6-DH2, PM6-DH2X, PM6-D3H4, PM6-D3H4X,
        AM1, RM1, PM3, MNDO, MNDOD.

        Parameters
        ----------
        periodic_only : bool
            Only return options confirmed to work for a periodic system
            via MDI -- conservative by design, a method is only included
            if it has actually been run periodic and validated, not
            because some other flag suggests it should work.
        mdi_only : bool
            Only return options actually launchable via mopac_mdi.py, as
            opposed to only available through this step's traditional
            batch/file-based path.

        Returns
        -------
        dict
            Keyed by bare method name (e.g. "PM6-ORG"). Each value has::

                model_chemistry  : str   -- "MOPAC:SQM@<name>"
                type             : str   -- always "SQM" currently
                description      : str
                periodic_native  : bool  -- this method's own metadata flag
                periodic_mdi     : bool  -- actually validated periodic via MDI
                elements         : str   -- genuine NDDO Hamiltonian coverage
                sparkle_elements : str or None -- lanthanides reachable only
                                   via the Sparkle point-charge model
                                   (currently documented for PM7/PM7-TS/PM6
                                   only; None elsewhere, which may mean "not
                                   applicable" or "not yet checked" -- see
                                   NOTES_mopac_model_chemistry_metadata.rst)
                mdi_capable      : bool
                mdi_script       : str or None
                mdi_method_arg   : str or None
        """
        options = {}
        for theory_class, class_data in mopac_step.metadata[
            "computational models"
        ].items():
            for family, family_data in class_data["models"].items():
                for name, param in family_data["parameterizations"].items():
                    mdi_capable = name in cls._MDI_CAPABLE_METHODS
                    periodic_mdi = name in cls._MDI_PERIODIC_VALIDATED

                    if periodic_only and not periodic_mdi:
                        continue
                    if mdi_only and not mdi_capable:
                        continue

                    options[name] = {
                        "model_chemistry": f"MOPAC:SQM@{name}",
                        "type": "SQM",
                        "description": param.get("description", ""),
                        "periodic_native": param.get("periodic", False),
                        "periodic_mdi": periodic_mdi,
                        "elements": param.get("elements", ""),
                        "sparkle_elements": param.get("sparkle_elements"),
                        "mdi_capable": mdi_capable,
                        "mdi_script": "mopac_mdi.py" if mdi_capable else None,
                        "mdi_method_arg": name if mdi_capable else None,
                    }
        return options
