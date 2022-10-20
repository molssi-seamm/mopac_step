# -*- coding: utf-8 -*-

"""Main module."""

import mopac_step


class MOPACStep(object):
    my_description = {
        "description": "Setup and run MOPAC",
        "group": "Simulations",
        "name": "MolSSI MOPAC",
    }

    def __init__(self, flowchart=None, gui=None):
        """Initialize this helper class, which is used by
        the application via stevedore to get information about
        and create node objects for the flowchart
        """
        pass

    def description(self):
        """Return a description of what this extension does"""
        return MOPACStep.my_description

    def create_node(self, flowchart=None, **kwargs):
        """Return the new node object"""
        return mopac_step.MOPAC(flowchart=flowchart, **kwargs)

    def create_tk_node(self, canvas=None, **kwargs):
        """Return the graphical Tk node object"""
        return mopac_step.TkMOPAC(canvas=canvas, **kwargs)
