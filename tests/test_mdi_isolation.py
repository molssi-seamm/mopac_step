# -*- coding: utf-8 -*-

"""The MDI engine's guard against MOPAC's library crashing on open-shell systems
(data/mopac_mdi.py): each calculation of an open-shell system runs in a forked
child, and one whose child dies is done by the standalone MOPAC program. MOPAC
23.2.5's library (mopactools 0.1.4) aborts at random in some open-shell
calculations (PPE1694 job 588: Si2, the vinyl radical, NO2), which took the
engine and the step with it ("MDI_Recv failed")."""

import importlib.resources
import importlib.util
import os
import signal
import sys

import numpy as np
import pytest

pytestmark = pytest.mark.skipif(
    not hasattr(os, "fork"), reason="the engine's isolation needs os.fork"
)


@pytest.fixture(scope="module")
def engine():
    """The engine script as a module, without running it (it needs mopactools
    and mdi only in main())."""
    path = importlib.resources.files("mopac_step") / "data" / "mopac_mdi.py"
    spec = importlib.util.spec_from_file_location("mopac_mdi_under_test", path)
    module = importlib.util.module_from_spec(spec)
    saved = list(sys.path)
    try:
        spec.loader.exec_module(module)
    finally:
        sys.path[:] = saved
    return module


def test_the_result_comes_back(engine):
    value = engine.run_isolated(
        lambda: {"heat": 1.5, "coord_deriv": np.arange(6.0), "error_msg": []}
    )
    assert value["heat"] == 1.5
    assert value["coord_deriv"].tolist() == [0.0, 1.0, 2.0, 3.0, 4.0, 5.0]


def test_a_crash_is_reported_not_fatal(engine):
    """A child that dies by a signal (MOPAC's abort) raises CalculationCrashed
    here; this process carries on."""

    def abort():
        os.kill(os.getpid(), signal.SIGABRT)

    with pytest.raises(engine.CalculationCrashed, match="signal 6"):
        engine.run_isolated(abort)

    def leave():
        os._exit(3)

    with pytest.raises(engine.CalculationCrashed, match="no result"):
        engine.run_isolated(leave)
    assert engine.run_isolated(lambda: 42) == 42


def test_an_exception_is_an_error(engine):
    def broken():
        raise ValueError("bad input")

    with pytest.raises(RuntimeError, match="ValueError: bad input") as info:
        engine.run_isolated(broken)
    assert not isinstance(info.value, engine.CalculationCrashed)


def test_standalone_keywords(engine):
    assert engine.standalone_keywords("PM7", 0, 1) == (
        "PM7 1SCF GRAD AUX(PRECISION=9) GEO-OK THREADS=1 CHARGE=0"
    )
    doublet = engine.standalone_keywords("PM6-ORG", -1, 2, tolerance=0.1)
    assert doublet.endswith("CHARGE=-1 UHF DOUBLET RELSCF=0.1")
    assert engine.standalone_keywords("PM7", 0, 9).endswith("UHF MS=4.0")


AUX = """ HEAT_OF_FORMATION:KCAL/MOL=+0.582266568271234D+02
 GRADIENT_NORM:KCAL/MOL/ANGSTROM=+0.418491923833519D+02
 GRADIENTS:KCAL/MOL/ANGSTROM[006]=
 -30.3766748554598   4.5150878923513   0.0000000396862  25.7715938863059
  -2.6141776639267   0.0000000275361
 OVERLAP_MATRIX[0015]=
"""


def test_parse_aux(engine):
    heat, gradients = engine.parse_aux(AUX, 2)
    assert heat == pytest.approx(58.2266568271234)
    assert gradients == pytest.approx(
        [-30.3766748554598, 4.5150878923513, 3.96862e-8, 25.7715938863059,
         -2.6141776639267, 2.75361e-8]
    )  # fmt: skip
    with pytest.raises(RuntimeError, match="6 gradients for 3 atoms"):
        engine.parse_aux(AUX, 3)
    with pytest.raises(RuntimeError, match="no heat"):
        engine.parse_aux("nothing", 2)
