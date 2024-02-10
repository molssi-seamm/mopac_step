===================
SEAMM MOPAC plug-in
===================

.. image:: https://img.shields.io/github/issues-pr-raw/molssi-seamm/mopac_step
   :target: https://github.com/molssi-seamm/mopac_step/pulls
   :alt: GitHub pull requests

.. image:: https://github.com/molssi-seamm/mopac_step/workflows/CI/badge.svg
   :target: https://github.com/molssi-seamm/mopac_step/actions
   :alt: Build Status

.. image:: https://codecov.io/gh/molssi-seamm/mopac_step/branch/master/graph/badge.svg
   :target: https://codecov.io/gh/molssi-seamm/mopac_step
   :alt: Code Coverage

.. image:: https://github.com/molssi-seamm/mopac_step/workflows/CodeQL/badge.svg
   :target: https://github.com/molssi-seamm/mopac_step/security/code-scanning
   :alt: Code Quality

.. image:: https://github.com/molssi-seamm/mopac_step/workflows/Release/badge.svg
   :target: https://molssi-seamm.github.io/mopac_step/index.html
   :alt: Documentation Status

.. image:: https://img.shields.io/pypi/v/mopac_step.svg
   :target: https://pypi.python.org/pypi/mopac_step
   :alt: PyPi VERSION

A SEAMM plug-in to setup, run and analyze semiempirical calculations
with MOPAC.

This plug-in provides a graphical user interface (GUI) for setting up
and running simulations using the semiempirical quantum chemistry code
MOPAC_.

* Free software: BSD license
* Documentation: https://molssi-seamm.github.io/mopac_step/index.html
* Code: https://github.com/molssi-seamm/mopac_step

.. _MOPAC: http://openmopac.net

Features
--------

* Single-point energies
* Structural optimization
* IR and Raman vibrational frequencies
* Temperature dependent thermodynamic functions
* Results can be stored in flowchart variables or tables_.

.. _tables: https://molssi-seamm.github.io/table_step/index.html

seamm-mopac Docker image
------------------------
There is a Docker image available for the SEAMM MOPAC plug-in for running mopac. It is
available at the Github Container Registry (ghcr.io) as

.. code-block:: bash

    ghcr.io/molssi-seamm/seamm-mopac:<version>

Where <version> is the explicit version tag for the desired image. The tag `latest` is
quite confusing, and does not mean the latest version of the image, so we recomend using
explcit versions rather than `latest`.

The container can also be run standalone with the following command:

.. code-block:: bash

    docker run --rm -v $PWD:/home ghcr.io/molssi-seamm/seamm-mopac:<version> ?mopac <input file>?

where `<input file>` is the input file for the MOPAC calculation. By default, mopac is
run using the input file `mopac.dat`. The output files will be written to the current
directory. The `--rm` option removes the container after it exits, and the `-v` option
mounts the current directory to the `/home` directory in the container.

Acknowledgements
----------------

This package was created with Cookiecutter_ and the `molssi-seamm/cookiecutter-seamm-plugin`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`molssi-seamm/cookiecutter-seamm-plugin`: https://github.com/molssi-seamm/cookiecutter-seamm-plugin

Developed by the Molecular Sciences Software Institute (MolSSI_),
which receives funding from the `National Science Foundation`_ under
awards OAC-1547580 and CHE-2136142.

.. _MolSSI: https://www.molssi.org
.. _`National Science Foundation`: https://www.nsf.gov
