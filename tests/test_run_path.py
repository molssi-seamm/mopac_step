# -*- coding: utf-8 -*-

"""MOPAC's run path, end to end: a flowchart built from a spec and run by
``run_flowchart``, through ``MOPAC.run()`` -- input, the ini file, the task, the
output files and their analysis.

No unit test reaches ``run()``; a variable left behind there once would have
crashed every MOPAC run and only lint caught it (phase 7). Two versions:

* a fake ``mopac`` that copies a real run's output, so the whole path runs in CI;
* the real MOPAC, when it is installed (skipped otherwise, as in CI).

Each run has its own HOME and SEAMM_ROOT, so the user's timing files and
``mopac.ini`` are never touched. A tiny step plug-in on PYTHONPATH makes the water
molecule, so no structure step is needed.
"""

import configparser
import os
from pathlib import Path
import shutil
import subprocess
import sys
import textwrap

import pytest

# The source under test first
SOURCE = Path(__file__).resolve().parents[1]
DATA = Path(__file__).resolve().parent / "data" / "run_path"
BUILD = "import sys; from seamm.flowchart_cli import main; sys.exit(main())"
RUN = "import sys; from seamm_exec import run; sys.argv[0] = 'run_flowchart'; run()"

WATER_STEP = textwrap.dedent('''
    """A step for testing: water at a fixed geometry."""

    import seamm


    class Water(seamm.Node):
        def __init__(self, flowchart=None, extension=None):
            super().__init__(flowchart=flowchart, title="Water", extension=extension)

        @property
        def version(self):
            return "0.1"

        def description_text(self, P=None):
            return self.header + "\\n    Water."

        def run(self):
            next_node = super().run(None)
            db = self.get_variable("_system_db")
            system = db.create_system(name="water")
            configuration = system.create_configuration(name="water")
            configuration.atoms.append(
                x=[0.0, 0.757, -0.757],
                y=[0.0, 0.586, 0.586],
                z=[0.0, 0.0, 0.0],
                symbol=["O", "H", "H"],
            )
            db.system = system
            return next_node


    class WaterStep:
        my_description = {
            "description": "Water for tests",
            "group": "Building",
            "name": "Water",
        }

        def __init__(self, flowchart=None, gui=None):
            pass

        def description(self):
            return WaterStep.my_description

        def create_node(self, flowchart=None, **kwargs):
            return Water(flowchart=flowchart, **kwargs)

        def create_tk_node(self, canvas=None, **kwargs):
            raise NotImplementedError("no GUI for the test step")
''')

SPEC = textwrap.dedent("""\
    title: MOPAC run-path test
    steps:
    - Water: {}
    - MOPAC:
        steps:
        - Energy
    """)

# Copies the recorded output beside the input, as MOPAC writes it; fails, as
# MOPAC would, if the input is missing or empty.
FAKE_MOPAC = textwrap.dedent("""\
    #!{python}
    import shutil
    import sys
    from pathlib import Path

    inp = Path(sys.argv[1])
    if not inp.exists() or inp.read_text().strip() == "":
        sys.exit("no input")
    for name in ("mopac.out", "mopac.aux", "mopac.arc"):
        shutil.copy(Path("{data}") / name, inp.parent / name)
    """)


def real_mopac():
    """The installed MOPAC executable, or None: ``$MOPAC_EXE``, else ``mopac`` on
    the PATH, else what the installation's ``mopac.ini`` names (the root is
    ``$SEAMM_ROOT`` or ``~/SEAMM``), as SEAMM itself finds it."""
    path = os.environ.get("MOPAC_EXE") or shutil.which("mopac")
    if path:
        return path
    root = Path(os.environ.get("SEAMM_ROOT", "").strip() or "~/SEAMM").expanduser()
    config = configparser.ConfigParser()
    try:
        config.read(root / "mopac.ini")
        local = config["local"]
    except (configparser.Error, KeyError):
        return None
    code = local.get("code", "").split()[0] if local.get("code") else ""
    candidates = [Path(code)] if code else []
    if local.get("conda") and local.get("conda-environment"):
        prefix = Path(local["conda"]).parents[1] / "envs" / local["conda-environment"]
        candidates.append(prefix / "bin" / (Path(code).name if code else "mopac"))
    for candidate in candidates:
        if candidate.is_absolute() and candidate.exists():
            return str(candidate)
    return None


def run_water(tmp_path, code):
    """Build and run the flowchart with ``code`` as MOPAC; return the job dir."""
    site = tmp_path / "site"
    info = site / "fakewater-0.1.dist-info"
    info.mkdir(parents=True)
    (site / "fakewater.py").write_text(WATER_STEP)
    (info / "METADATA").write_text(
        "Metadata-Version: 2.1\nName: fakewater\nVersion: 0.1\n"
    )
    (info / "entry_points.txt").write_text(
        "[org.molssi.seamm]\nWater = fakewater:WaterStep\n\n"
        "[org.molssi.seamm.tk]\nWater = fakewater:WaterStep\n"
    )
    root = tmp_path / "root"
    root.mkdir()
    (root / "mopac.ini").write_text(f"[local]\ninstallation = local\ncode = {code}\n")
    home = tmp_path / "home"
    home.mkdir()
    job = tmp_path / "job"
    job.mkdir()
    (job / "spec.yaml").write_text(SPEC)

    env = {
        k: v
        for k, v in os.environ.items()
        if not k.startswith(("SEAMM_", "OMP_NUM_THREADS"))
    }
    env["HOME"] = str(home)
    env["SEAMM_ROOT"] = str(root)
    env["PYTHONPATH"] = os.pathsep.join(
        [str(SOURCE), str(site), *filter(None, [os.environ.get("PYTHONPATH")])]
    )
    for args in (
        ["-c", BUILD, "build", "spec.yaml", "-o", "test.flow"],
        ["-c", RUN, "test.flow"],
    ):
        result = subprocess.run(
            [sys.executable, *args],
            cwd=job,
            env=env,
            capture_output=True,
            text=True,
            timeout=300,
        )
        assert result.returncode == 0, result.stdout[-3000:] + result.stderr[-3000:]
    return job


def check_job(job, enthalpy):
    """The input written, the task run, the output analyzed and reported."""
    text = (job / "2" / "mopac.dat").read_text()
    keywords = text.splitlines()[0].split()
    assert "1SCF" in keywords and "CHARGE=0" in keywords and "SINGLET" in keywords
    assert (job / "2" / "success.dat").exists()
    for name in ("mopac.out", "mopac.aux", "mopac.arc"):
        assert (job / "2" / name).stat().st_size > 0
    out = (job / "job.out").read_text()
    lines = [line for line in out.splitlines() if "Enthalpy of Formation" in line]
    assert lines, out[-3000:]
    value = float(lines[-1].split("|")[2])
    assert value == pytest.approx(enthalpy, abs=0.1)
    assert "Dipole Moment" in out


def test_run_path_with_a_fake_mopac(tmp_path):
    fake = tmp_path / "fake_mopac"
    fake.write_text(FAKE_MOPAC.format(python=sys.executable, data=DATA))
    fake.chmod(0o755)
    check_job(run_water(tmp_path, fake), enthalpy=-55.03)


@pytest.mark.skipif(real_mopac() is None, reason="MOPAC is not installed")
def test_run_path_with_the_real_mopac(tmp_path):
    check_job(run_water(tmp_path, real_mopac()), enthalpy=-55.03)
