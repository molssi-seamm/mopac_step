# -*- coding: utf-8 -*-

"""Resolve MOPAC on the machine that runs it (seamm_exec's resolver hook).

The ``[local]`` section of that machine's ``<root>/mopac.ini`` (a conda
installation as the installer writes it, a module, or a path), falling back to
``mopac`` on the PATH. Unlike the MOPAC step, nothing is written: a resolver may
run on a cluster's compute node.

Registered as the entry point ``mopac`` in ``org.molssi.seamm.exec.resolvers``.
"""

import shutil


def resolve(config, cmd, env, ce, root):
    """``(config, cmd, env)`` for running MOPAC here."""
    config = dict(config)
    if not (config.get("code") or "").strip() and config.get("installation") in (
        "conda",
        "modules",
    ):
        # The environment or modules provide it: run it by name
        config["code"] = "mopac"
    if not (config.get("code") or "").strip():
        path = shutil.which("mopac")
        if path is None:
            raise RuntimeError(
                "Could not find MOPAC: there is no [local] section with 'code' in "
                f"{root}/mopac.ini and no 'mopac' on the PATH."
            )
        config = {"installation": "local", "code": path}
    env = dict(env)
    # MOPAC threads with OpenMP; one task gets its share of the machine.
    cpus = int(ce.get("CPUS_PER_TASK", 1) or 1) * int(ce.get("NTASKS", 1) or 1)
    env.setdefault("OMP_NUM_THREADS", str(max(1, cpus)))
    return config, list(cmd), env


def _available(root):
    return shutil.which("mopac") is not None


resolve.available = _available
