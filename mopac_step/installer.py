# -*- coding: utf-8 -*-

"""Installer for the MOPAC plug-in.

This handles any further installation needed after installing the Python
package `mopac-step`.
"""

import logging
from pathlib import Path
import pkg_resources
import platform
import subprocess
import zipfile

import requests

import seamm_installer

logger = logging.getLogger(__name__)


class Installer(seamm_installer.InstallerBase):
    """Handle further installation needed after installing mopac-step.

    The Python package `MOPAC-step` should already be installed, using `pip`,
    `conda`, or similar. This plug-in-specific installer then checks for the
    MOPAC executable, installing it if needed, and registers its
    location in seamm.ini.

    There are a number of ways to determine which are the correct MOPAC
    executables to use. The aim of this installer is to help the user locate
    the executables. There are a number of possibilities:

    1. The correct executables are already available.

        1. If they are already registered in `seamm.ini` there is nothing else
           to do.
        2. They may be in the current path, in which case they need to be added
           to `seamm.ini`.
        3. If a module system is in use, a module may need to be loaded to give
           access to MOPAC.
        3. They cannot be found automatically, so the user needs to locate the
           executables for the installer.

    2. MOPAC is not installed on the machine. In this case they can be
       installed in a Conda environment. There is one choice:

        1. They can be installed in a separate environment, `seamm-mopac` by
           default.
    """

    def __init__(self, logger=logger):
        # Call the base class initialization, which sets up the commandline
        # parser, amongst other things.
        super().__init__(logger=logger)

        logger.debug("Initializing the MOPAC installer object.")

        self.section = "mopac-step"
        self.path_name = "mopac-path"
        self.executables = ["mopac"]
        self.resource_path = Path(pkg_resources.resource_filename(__name__, "data/"))
        # What Conda environment is the default?
        data = self.configuration.get_values(self.section)
        if "conda-environment" in data and data["conda-environment"] != "":
            self.environment = data["conda-environment"]
        else:
            self.environment = "seamm-mopac"

        # The environment.yaml file for Conda installations.
        path = Path(pkg_resources.resource_filename(__name__, "data/"))
        logger.debug(f"data directory: {path}")
        self.environment_file = path / "seamm-mopac.yml"

    def exe_version(self, path):
        """Get the version of the MOPAC executable.

        Parameters
        ----------
        path : pathlib.Path
            Path to the executable.

        Returns
        -------
        str
            The version reported by the executable, or 'unknown'.
        """
        try:
            result = subprocess.run(
                [str(path), "--version"],
                stdin=subprocess.DEVNULL,
                capture_output=True,
                text=True,
            )
        except Exception:
            version = "unknown"
        else:
            version = "unknown"
            lines = result.stdout.splitlines()
            for line in lines:
                line = line.strip()
                tmp = line.split()
                if len(tmp) == 1:
                    version = tmp[0]
                    break

        # MOPAC tends to leave timing.dat floating around. :-(
        timing = Path("timer.dat")
        if timing.exists():
            try:
                timing.unlink()
            except Exception:
                pass

        return version

    def install(self):
        """Currently the installation of MOPAC is a bit specialized! Have to download
        and unzip the executables.
        """
        super().install()

        # The bin directory may not exist!
        path = self.conda.path(self.environment) / "bin"
        path.mkdir(mode=0o755, exist_ok=True)

        # Now fetch the MOPAC executables.
        system = platform.system()
        if system == "Darwin":
            url = "http://openmopac.net/MOPAC2016_for_Macintosh.zip"
        elif system == "Linux":
            url = "http://openmopac.net/MOPAC2016_for_Linux_64_bit.zip"
        elif system == "Windows":
            url = "http://openmopac.net/MOPAC2016_standalone_for_WINDOWS_64_bit.zip"
        else:
            raise RuntimeError(f"Don't have executables for {system=}")

        zip_file = path / "mopac.zip"
        r = requests.get(url, stream=True)
        with open(zip_file, "wb") as fd:
            for chunk in r.iter_content(chunk_size=1024):
                fd.write(chunk)

        zip_archive = zipfile.ZipFile(zip_file)
        zip_archive.extract("MOPAC2016.exe", path)

        if system == "Linux":
            zip_archive.extract("libiomp5.so", path)
            lib_path = path / "libiomp5.so"
            lib_path.chmod(0o755)

        mopac_exe = path / "MOPAC2016.exe"
        mopac_exe.chmod(0o755)
