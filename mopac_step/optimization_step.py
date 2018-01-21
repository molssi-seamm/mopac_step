# -*- coding: utf-8 -*-

"""Main module."""

import mopac_step


class OptimizationStep(object):
    my_description = {
        'description':
        'Optimization of the structure',
        'group': 'Calculations',
        'name': 'Optimization'
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
        return OptimizationStep.my_description

    def factory(self, graphical=False, workflow=None, canvas=None, **kwargs):
        """Return the node object or graphical node object"""
        if graphical:
            return mopac_step.TkOptimization(canvas=canvas, **kwargs)
        else:
            return mopac_step.Optimization(workflow=workflow, **kwargs)
