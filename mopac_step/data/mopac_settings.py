# -*- coding: utf-8 -*-

"""The settings of MOPAC's model-chemistry calculations, for their fingerprints.

The MDI engine (``mopac_mdi.py``, through mopactools in the seamm-mopac
environment) and the task route (``mopac_step.batch``, the MOPAC binary) both
describe a calculation with :func:`settings_text`, so one calculation has one
fingerprint whichever route ran it. The engine sends its record without the hash,
which seamm_mdi adds with ``seamm_util.fingerprint.calculation_record``; the task
route adds it itself.

What changes the heat of formation at a geometry: the method, the MOZYME solver,
the SCF convergence (mopactools' relative tolerance; 1.0 is MOPAC's default, which
the task route's input uses) and MOPAC's version. The charge and spin belong to
the species. This module imports nothing outside the standard library.
"""

PROGRAM = "MOPAC"
SETTINGS_FILE = "MOPAC settings"


def settings_text(method, mozyme=False, tolerance=1.0):
    """The text hashed for a MOPAC calculation."""
    return (
        f"method {str(method).upper()}\n"
        f"mozyme {'yes' if mozyme else 'no'}\n"
        f"scf tolerance {float(tolerance)!r}\n"
    )


def settings_record(method, mozyme=False, tolerance=1.0, version="unknown"):
    """A record of a calculation, without the fingerprint (seamm_mdi, or the task
    route, adds it)."""
    return {
        "program": PROGRAM,
        "version": str(version),
        "files": {SETTINGS_FILE: settings_text(method, mozyme, tolerance)},
    }
