# -*- coding: utf-8 -*-

"""Main module."""

import mopac_step


class ThermodynamicsStep(object):
    my_description = {
        'description':
        'Harmonic approximation to the thermodynamic functions',
        'group': 'Calculations',
        'name': 'Thermodynamic functions'
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
        return ThermodynamicsStep.my_description

    def create_node(self, workflow=None, **kwargs):
        """Return the new node object"""
        return mopac_step.Thermodynamics(workflow=workflow, **kwargs)

    def create_tk_node(self, canvas=None, **kwargs):
        """Return the graphical Tk node object"""
        return mopac_step.TkThermodynamics(canvas=canvas, **kwargs)
