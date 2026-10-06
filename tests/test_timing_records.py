# -*- coding: utf-8 -*-
"""The timing records MOPAC runs write (seamm_exec campaign 2026-10-05)."""

from pathlib import Path
from types import SimpleNamespace

from mopac_step.mopac import task_kind, timing_descriptors

OUT = Path(__file__).parent / "data" / "run_path" / "mopac.out"


def test_task_kind():
    assert task_kind(["PM7 1SCF"]) == "energy"
    assert task_kind(["PM7 1SCF GRADIENTS"]) == "gradient"
    assert task_kind(["PM7 GRADIENTS BONDS"]) == "opt"
    assert task_kind(["PM7 1SCF", "PM7 FORCE THERMO"]) == "force"
    assert task_kind(["PM7 1SCF", "PM7 OLDGEO"]) == "opt"


def test_descriptors():
    conf = SimpleNamespace(
        atoms=SimpleNamespace(atomic_numbers=[8, 1, 1]),
        charge=0,
        spin_multiplicity=1,
        periodicity=0,
    )
    d = timing_descriptors(
        ["PM7 GRADIENTS BONDS AUX(MOS=10,XP,XS,PRECISION=3) CHARGE=0 SINGLET"],
        OUT.read_text(),
        conf,
    )
    assert d["hamiltonian"] == "PM7"
    assert d["task"] == "opt"
    assert d["n_calculations"] == 1
    assert d["mozyme_requested"] is False
    assert d["n_atoms"] == 3 and d["n_heavy"] == 1 and d["n_basis"] == 6
    assert d["n_electrons"] == 10
    assert d["regime"] == "scf"
    assert d["scf_runs"] >= 1
    assert d["code_seconds"] == 0.01
    assert d["terminated_normally"] is True


def test_mozyme_regime_is_read_from_the_output():
    text = (
        " *  MOZYME     - USE LOCALIZED M.O.s IN SOLVING THE SCF EQUATIONS\n"
        "     SCF FIELD WAS ACHIEVED\n CYCLE:     1\n CYCLE:     2\n"
        " TOTAL JOB TIME:            35.87 SECONDS\n == MOPAC DONE ==\n"
    )
    d = timing_descriptors(["PM6-ORG MOZYME GRADIENTS"], text)
    assert d["hamiltonian"] == "PM6-ORG" and d["mozyme_requested"] is True
    assert d["regime"] == "mozyme" and d["geometry_cycles"] == 2
    assert d["code_seconds"] == 35.87
    # Asked for but not used (MOPAC fell back): the output decides
    d = timing_descriptors(["PM7 MOZYME 1SCF"], "     SCF FIELD WAS ACHIEVED\n")
    assert d["mozyme_requested"] is True and d["regime"] == "scf"
