# -*- coding: utf-8 -*-

"""Regression: the MDI engine's energies are the MOPAC program's (default SCF).

MOPAC's library (mopactools) runs every SCF with PULAY, which converges to wrong
solutions for some molecules; the engine gave them for the PM6-ORG
penta-1,2,3-triene fragment (449.9 vs 421.5 kJ/mol) and the PM7 S2 triplet
(PPE1694 jobs 588/594, 2026-11-13). The library was also wrong along an S2 scan
at some bond lengths and right at others, so the scan is checked point by point
(a wrong point mid-optimization steers it). The reference heats are the MOPAC
program's, ``<method> 1SCF GRAD [UHF TRIPLET]``.

Drives the real engine; skipped where the seamm-mopac environment is missing.
"""

import importlib.resources
import shutil
import subprocess

import numpy as np
import pytest

pytest.importorskip("mdi")
seamm_mdi = pytest.importorskip("seamm_mdi")


def _engine_available():
    if shutil.which("conda") is None:
        return False
    result = subprocess.run(
        ["conda", "run", "-n", "seamm-mopac", "python", "-c",
         "import mdi, mopactools.api"],
        capture_output=True,
    )  # fmt: skip
    return result.returncode == 0


pytestmark = pytest.mark.skipif(
    not _engine_available(), reason="seamm-mopac MDI engine environment not available"
)


def _engine(method, multiplicity, elements):
    script = str(importlib.resources.files("mopac_step") / "data" / "mopac_mdi.py")

    def build_argv(hostname, port):
        return [
            "conda", "run", "--live-stream", "-n", "seamm-mopac", "python", script,
            "-mdi",
            f"-role ENGINE -name MOPAC -method TCP -port {port} "
            f"-hostname {hostname}",
            "--method", method, "--charge", "0",
            "--multiplicity", str(multiplicity),
        ]  # fmt: skip

    return seamm_mdi.MDIEngine(build_argv, elements=elements, timeout=120.0)


#: PM7 S2 triplet: S-S distance (Å) -> the program's heat (kJ/mol). The library
#: gave 732.5, 687.6 and 675.1 at 1.80, 1.883 and 1.90 Å
S2_SCAN = {
    1.70: 149.487,
    1.80: 127.187,
    1.85: 127.345,
    1.883: 130.801,
    1.90: 133.507,
    1.95: 144.695,
    2.00: 160.048,
    2.10: 200.303,
}


def test_s2_triplet_along_a_scan():
    with _engine("PM7", 3, [16, 16]) as engine:
        heats = {}
        for r in S2_SCAN:
            engine.set_coordinates([[0.0, 0.0, 0.0], [r, 0.0, 0.0]], units="Å")
            heats[r] = engine.energy(units="kJ/mol")
    for r, expected in S2_SCAN.items():
        assert heats[r] == pytest.approx(expected, abs=0.05), r


#: The PM6-ORG penta-1,2,3-triene fragment of PPE1694 job 594 (Å)
PENTATRIENE = (
    [6, 6, 6, 6, 6, 1, 1, 1, 1, 1, 1],
    [
        [2.832500, 0.112700, 0.372300],
        [1.556200, -0.156700, 0.157000],
        [0.291600, -0.441200, -0.061600],
        [-0.996500, -0.665300, -0.270600],
        [-2.050800, 0.385600, -0.165000],
        [3.287100, 0.033800, 1.345900],
        [3.499600, 0.425900, -0.413800],
        [-1.370000, -1.656600, -0.538800],
        [-2.584600, 0.486500, -1.119100],
        [-2.800000, 0.099200, 0.584700],
        [-1.665200, 1.376200, 0.108900],
    ],
)


def test_pentatriene_is_the_programs_solution():
    elements, xyz = PENTATRIENE
    xyz = np.array(xyz)
    with _engine("PM6-ORG", 1, elements) as engine:
        energies = []
        # The stored geometry and two displaced ones, as an optimization visits
        for shift in (0.0, 0.02, -0.02):
            moved = xyz.copy()
            moved[2, 0] += shift
            engine.set_coordinates(moved, units="Å")
            energies.append(engine.energy(units="kJ/mol"))
            forces = engine.forces(units="kJ/mol/Å")
            assert np.all(np.isfinite(forces))
    # The library's PULAY solution was 449.879 at the stored geometry
    assert energies == pytest.approx([421.539, 429.905, 433.351], abs=0.05)
