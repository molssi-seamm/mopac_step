# -*- coding: utf-8 -*-

"""Main module."""

import mopac_step


class MOPACStep(object):
    my_description = {
        'description':
        'Setup and run MOPAC',
        'group': 'Simulations',
        'name': 'MolSSI MOPAC'
    }

    def __init__(self, workflow=None, gui=None):
        """Initialize this helper class, which is used by
        the application via sevedore to get information about
        and create node objects for the workflow
        """
        pass

    def description(self):
        """Return a description of what this extension does
        """
        return MOPACStep.my_description

    def factory(self, graphical=False, workflow=None, canvas=None, **kwargs):
        """Return the node object or graphical node object"""
        if graphical:
            return mopac_step.TkMOPAC(canvas=canvas, **kwargs)
        else:
            return mopac_step.MOPAC(workflow=workflow, **kwargs)
