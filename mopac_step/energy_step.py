# -*- coding: utf-8 -*-

"""Main module."""

import mopac_step


class EnergyStep(object):
    my_description = {
        'description':
        'A single-point energy calculation',
        'group': 'Calculations',
        'name': 'Energy'
    }

    def __init__(self, workflow=None, gui=None):
        """Initialize this helper class, which is used by
        the application via stevedore to get information about
        and create node objects for the workflow
        """
        pass

    def description(self):
        """Return a description of what this extension does
        """
        return EnergyStep.my_description

    def factory(self, graphical=False, workflow=None, canvas=None, **kwargs):
        """Return the node object or graphical node object"""
        if graphical:
            return mopac_step.TkEnergy(canvas=canvas, **kwargs)
        else:
            return mopac_step.Energy(workflow=workflow, **kwargs)
