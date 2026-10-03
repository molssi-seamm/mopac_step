# -*- coding: utf-8 -*-

"""MOPAC's side of the Model Chemistry batch contract.

``get_task`` writes a MOPAC input for a single SCF with gradients, in vacuum,
as the MDI engine (``data/mopac_mdi.py``, through mopactools) computes it, and
``analyze_task`` returns what the engine returns: the **heat of formation** as
the "energy" (Paul, 2026-10-03, so that the evaluator's choice of path never
changes results) and the gradients, in kJ/mol and kJ/mol/Å.

Only closed-shell (or, for an odd number of electrons, doublet) molecules run
this way for now; open-shell and periodic MOPAC stay on the MDI engine, whose
equivalence for them has not been checked.
"""

import re

import numpy as np

import seamm_exec
from seamm_exec.evaluator import AnalysisError, check_properties, structure_data
from seamm_util import Q_

_FLOAT = re.compile(r"[+-]?\d*\.\d+(?:[DdEe][+-]?\d+)?")


def can_run_task(configuration, model_chemistry, *, options=None):
    """Whether :func:`get_task` can run this structure: a molecule in its lowest
    spin state. Anything else stays on the MDI engine."""
    options = dict(options or {})
    data = structure_data(configuration)
    if data["periodicity"] != 0:
        return False
    if options.get("atom_indices") is not None or options.get("ghost_atoms"):
        return False
    charge = int(options.get("charge", data["charge"]))
    multiplicity = int(options.get("multiplicity", data["multiplicity"]))
    n_electrons = sum(data["atomic_numbers"]) - charge
    return multiplicity == (1 if n_electrons % 2 == 0 else 2)


def get_task(
    configuration,
    model_chemistry,
    *,
    key,
    properties=("energy", "gradients"),
    options=None,
    resources=None,
):
    """A :class:`seamm_exec.Task` computing MOPAC's heat of formation (and
    gradients) for one structure."""
    options = dict(options or {})
    data = structure_data(configuration)
    if data["periodicity"] != 0:
        raise ValueError(
            "Periodic MOPAC calculations cannot run as tasks; this structure runs "
            "on MOPAC's MDI engine where one is available."
        )
    for name in ("atom_indices", "ghost_atoms"):
        if options.get(name) is not None:
            raise ValueError(f"MOPAC tasks do not take '{name}'.")
    charge = int(options.get("charge", data["charge"]))
    multiplicity = int(options.get("multiplicity", data["multiplicity"]))
    n_electrons = sum(data["atomic_numbers"]) - charge
    minimum = 1 if n_electrons % 2 == 0 else 2
    if multiplicity != minimum:
        raise ValueError(
            f"MOPAC tasks support only the lowest spin state (multiplicity "
            f"{minimum} here), not {multiplicity}; this structure runs on MOPAC's "
            "MDI engine where one is available."
        )

    from seamm_exec.evaluator import mdi_method_and_basis

    method, _ = mdi_method_and_basis(model_chemistry)  # the rule lives once
    keywords = [method, "1SCF", "AUX(PRECISION=9)", f"CHARGE={charge}"]
    if "gradients" in properties:
        keywords.insert(2, "GRADIENTS")
    lines = [" ".join(keywords), str(key), ""]
    for symbol, (x, y, z) in zip(data["symbols"], data["coordinates"]):
        lines.append(f"{symbol:2s} {x:18.10f} 1 {y:18.10f} 1 {z:18.10f} 1")
    lines.append("")

    if resources is None:
        resources = seamm_exec.Resources(ntasks=1, cpus_per_task=1)
    n = len(data["symbols"])
    return seamm_exec.Task(
        key=key,
        program="mopac",
        cmd=["{code}", "mopac.dat", ">", "stdout.txt", "2>", "stderr.txt"],
        shell=True,
        files={"mopac.dat": "\n".join(lines)},
        return_files=["mopac.out", "mopac.aux"],
        resources=resources,
        estimated_seconds=0.01 + 1e-6 * n**3,
        success_text={"mopac.out": "== MOPAC DONE =="},
    )


def parse_aux(text):
    """The heat of formation (kcal/mol) and gradients (kcal/mol/Å) from the
    ``mopac.aux`` of a 1SCF calculation."""
    heat = None
    gradients = None
    lines = text.splitlines()
    i = 0
    while i < len(lines):
        line = lines[i].strip()
        if line.startswith("HEAT_OF_FORMATION:KCAL/MOL="):
            heat = float(line.split("=", 1)[1].strip().replace("D", "E"))
        elif line.startswith("GRADIENTS:KCAL/MOL/ANGSTROM["):
            n = int(line.split("[", 1)[1].split("]", 1)[0])
            values = []
            j = i + 1
            # The values follow on lines of numbers; the next KEY= ends them.
            while len(values) < n and j < len(lines) and "=" not in lines[j]:
                values.extend(
                    float(v.replace("D", "E").replace("d", "e"))
                    for v in _FLOAT.findall(lines[j])
                )
                j += 1
            if len(values) != n or n % 3 != 0:
                raise AnalysisError(
                    f"mopac.aux has {len(values)} gradient values, not {n}"
                )
            gradients = np.asarray(values, dtype=float).reshape(-1, 3)
            i = j - 1
        i += 1
    return heat, gradients


def analyze_task(
    result,
    model_chemistry,
    configuration,
    *,
    properties=("energy", "gradients"),
    options=None,
):
    """The heat of formation (kJ/mol, the MDI engine's "energy") and gradients
    ((n, 3) kJ/mol/Å) of a finished task."""
    aux = result.files.get("mopac.aux")
    if aux is None and result.directory is not None:
        from pathlib import Path

        path = Path(result.directory) / "mopac.aux"
        if path.exists():
            aux = path.read_text(errors="replace")
    if isinstance(aux, bytes):
        aux = aux.decode(errors="replace")
    data = {}
    if aux:
        heat, gradients = parse_aux(aux)
        if heat is not None:
            data["energy"] = float(Q_(heat, "kcal/mol").m_as("kJ/mol"))
        if gradients is not None and "gradients" in properties:
            n_atoms = len(configuration.atoms.atomic_numbers)
            if gradients.shape != (n_atoms, 3):
                raise AnalysisError(
                    f"The MOPAC calculation '{result.key}' has gradients for "
                    f"{gradients.shape[0]} atoms, not {n_atoms}"
                )
            data["gradients"] = Q_(gradients, "kcal/mol/Å").m_as("kJ/mol/Å")
    check_properties(data, properties, f"The MOPAC calculation '{result.key}'")
    return data
