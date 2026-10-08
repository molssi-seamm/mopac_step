# -*- coding: utf-8 -*-
"""The timing records MOPAC runs write (seamm_exec campaign 2026-10-05)."""

from pathlib import Path
from types import SimpleNamespace

from mopac_step import mopac
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
    # the WALL-CLOCK TIME (0.004 s), more precise than TOTAL JOB TIME (0.01 s)
    assert d["code_seconds"] == 0.004
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


def test_timing_spec():
    from mopac_step import mopac

    assert mopac.TIMING_SPEC["klass"] == ["hamiltonian", "regime"]
    assert mopac.TIMING_SPEC["default_alpha"] == 0.0
    assert mopac.TIMING_SPEC["setup_by"] == "regime"
    assert "spec" in mopac._record_kwargs() or not hasattr(
        __import__("seamm_exec"), "TimingSpec"
    )


_TWO_JOBS = """
 *  MOZYME     - Use Localized Molecular Orbitals
 CYCLE:     1 TIME:   0.332 TIME LEFT:  2.00D  GRAD.:   371.092 HEAT: -223.3
 CYCLE:     2 TIME:   0.152 TIME LEFT:  2.00D  GRAD.:    80.000 HEAT: -300.0
     SCF FIELD WAS ACHIEVED
          WALL-CLOCK TIME         =     37.496 SECONDS
          COMPUTATION TIME        =     37.494 SECONDS
{follow}
     SCF FIELD WAS ACHIEVED
          WALL-CLOCK TIME         =     38.051 SECONDS
          COMPUTATION TIME        =     38.047 SECONDS
 TOTAL JOB TIME:            75.82 SECONDS
 == MOPAC DONE ==
"""


def test_each_job_of_a_run_is_its_own_record():
    """A MOZYME optimization and its follow-up are two calculations: each its
    regime, cycles and time (MOPAC's clock is cumulative, and its TOTAL JOB
    TIME adds the cumulative values)."""
    lines = [
        "PM7 MOZYME GRADIENTS",
        "1SCF PM7 GRADIENTS OLDGEO",  # the exact (traditional SCF) follow-up
    ]
    jobs = mopac.job_descriptors(lines, _TWO_JOBS.replace("{follow}", ""))
    assert len(jobs) == 2
    main, follow = jobs
    assert main["regime"] == "mozyme" and main["task"] == "opt"
    assert main["geometry_cycles"] == 2
    assert abs(main["code_seconds"] - 37.496) < 1e-6
    assert follow["regime"] == "scf" and follow["task"] == "gradient"
    assert follow["follow_up"] == "exact"
    assert abs(follow["code_seconds"] - 0.555) < 1e-6
    # the run as a whole: the last cumulative clock, not TOTAL JOB TIME
    whole = mopac.timing_descriptors(lines, _TWO_JOBS.replace("{follow}", ""))
    assert abs(whole["code_seconds"] - 38.051) < 1e-6


def test_a_fresh_localized_follow_up_stays_mozyme():
    lines = ["PM7 MOZYME GRADIENTS", "1SCF PM7 MOZYME GRADIENTS OLDGEO"]
    text = _TWO_JOBS.replace(
        "{follow}", " *  MOZYME     - Use Localized Molecular Orbitals"
    )
    main, follow = mopac.job_descriptors(lines, text)
    assert follow["regime"] == "mozyme" and follow["follow_up"] == "new"


def test_a_single_job_is_not_split():
    assert mopac.job_descriptors(["PM7 1SCF GRADIENTS"], "anything") is None
    # nor an output that does not match the input's jobs
    assert mopac.job_descriptors(["PM7", "1SCF PM7 OLDGEO"], "no clock") is None


def test_every_record_has_the_same_columns():
    """A change of columns sets the timing file aside, so a single-job run,
    a main job and its follow-up must all write the same columns."""
    lines = ["PM7 MOZYME GRADIENTS", "1SCF PM7 GRADIENTS OLDGEO"]
    main, follow = mopac.job_descriptors(lines, _TWO_JOBS.replace("{follow}", ""))
    single = mopac.timing_descriptors(["PM7 1SCF GRADIENTS"], _TWO_JOBS)
    assert set(main) == set(follow) == set(single)
