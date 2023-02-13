==========
MOPAC Step
==========

MOPAC is a high-performance semiempircal Hartree-Fock code that can optimize structures,
predict enthalpies of formation, calculate thermodynamic properties, vibrational
frequencies, etc. for molecular and periodic compounds containing elements through
element 83, bismuth. It cannot, however, handle systems without a band-gap, so metals
and metal clusters are not an appropriate target.

MOPAC has an order-N approach suitable for larger systems with thousands of atoms, both
molecular and periodic. The method works well for systems with a well-defined Lewis
structure, i.e. organic molecules, biological systems, MOF's, zerolites, etc. The
order-N approach out-performs the tradtional approach beyond a few hundred atoms. 

.. grid:: 1 1 2 2

   .. grid-item-card:: Getting Started
      :margin: 0 3 0 0

      A simple introduction

      .. button-link:: ./getting_started/index.html
	 :color: primary
	 :expand:

         To the Getting Started Guide

   .. grid-item-card::  User Guide
      :margin: 0 3 0 0

      A complete guide to using this step

      .. button-link:: ./user_guide/index.html
	 :color: primary
	 :expand:

         To the User Guide

   .. grid-item-card::  Developer Guide
      :margin: 0 3 0 0

      Contributing to the code. Fixing bugs, adding functionality

      .. button-link:: ./developer_guide/index.html
	 :color: primary
	 :expand:

         To the Developer Guide

   .. grid-item-card:: API Reference
      :margin: 0 3 0 0

      The API for the MOPAC Step

      .. button-link:: ./api/index.html
	 :color: primary
	 :expand:

	 To the API Reference.


.. toctree::
   :hidden:
   :maxdepth: 1
   :titlesonly:

   getting_started/index
   user_guide/index
   developer_guide/index
   api/index

More Information
================
.. toctree::
   :maxdepth: 1
   :titlesonly:

   authors
   history
