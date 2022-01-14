# !/usr/bin/env python
# -*- coding: utf-8 -*-

"""Handle the installation of the MOPAC step."""

from .installer import Installer


def run():
    """Handle the extra installation needed.

    * Find and/or install the MOPAC executable.
    * Add or update information in the SEAMM.ini file for MOPAC
    """

    # Create an installer object
    installer = Installer()
    installer.run()


if __name__ == "__main__":
    run()
