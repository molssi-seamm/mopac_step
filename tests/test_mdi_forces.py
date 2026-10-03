# -*- coding: utf-8 -*-

"""Regression: the MOPAC MDI engine's forces are the derivative of its energy.

The engine converted MOPAC's gradient from kcal/mol/Å to hartree/bohr by
multiplying by bohr/Å instead of Å/bohr, so every force over MDI was 3.57x too
large (2026-06-23 to 2026-10-03). This drives the real engine (skipped where it
cannot start) and compares its forces with a central finite difference of its
energies.
"""

import numpy as np
import pytest

import seamm_exec

from mopac_step import MOPACStep

pytest.importorskip("mdi")
seamm_mdi = pytest.importorskip("seamm_mdi")

WATER = np.array([[0.0, 0.0, 0.117], [0.0, 0.757, -0.469], [0.0, -0.757, -0.469]])


def test_forces_are_minus_the_energy_derivative():
    def build_argv(hostname, port):
        return MOPACStep.get_mdi_engine_command(
            seamm_exec.Local(),
            {"root": "~/SEAMM"},
            method="PM6",
            port=port,
            hostname=hostname,
            n_atoms=3,
        )

    h = 1.0e-3  # Å
    try:
        engine = seamm_mdi.MDIEngine(build_argv, [8, 1, 1])
        engine.start()
    except Exception as e:
        pytest.skip(f"The MOPAC MDI engine cannot start here: {e}")
    with engine:
        engine.set_coordinates(WATER, units="Å")
        forces = np.asarray(engine.forces(units="kJ/mol/Å"), dtype=float)
        for atom, axis in ((0, 2), (1, 1), (2, 2)):
            energies = []
            for step in (h, -h):
                xyz = WATER.copy()
                xyz[atom, axis] += step
                engine.set_coordinates(xyz, units="Å")
                energies.append(engine.energy(units="kJ/mol"))
            derivative = (energies[0] - energies[1]) / (2 * h)
            # MOPAC's single-SCF gradient matches a central difference of its
            # energy to within about 1% (observed 0.1-0.7%); the bug was 257%.
            assert -forces[atom, axis] == pytest.approx(derivative, rel=2e-2)
