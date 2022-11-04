# -*- coding: utf-8 -*-

"""The graphical part of a MOPAC vibrational node"""

import mopac_step
import seamm_widgets as sw
import tkinter as tk
import tkinter.ttk as ttk


class TkForceconstants(mopac_step.TkEnergy):
    def __init__(
        self, tk_flowchart=None, node=None, canvas=None, x=120, y=20, w=200, h=50
    ):
        """Initialize a node

        Keyword arguments:
        """
        super().__init__(
            tk_flowchart=tk_flowchart, node=node, canvas=canvas, x=x, y=y, w=w, h=h
        )

    def create_dialog(self, title="MOPAC Force Constants"):
        """Create the dialog!"""
        self.logger.debug("Creating the dialog")
        frame = super().create_dialog(title=title)

        P = self.node.parameters

        # Create the vibrational widgets
        fcframe = self["forceconstant frame"] = ttk.LabelFrame(
            frame, text="Force Constants", labelanchor=tk.N
        )
        row = 0
        widgets = []
        for key in mopac_step.ForceconstantsParameters.parameters:
            self[key] = P[key].widget(fcframe)
            self[key].grid(row=row, column=0, sticky=tk.EW)
            widgets.append(self[key])
            row += 1
        sw.align_labels(widgets, sticky=tk.E)

        self.logger.debug("Finished creating the dialog")

    def reset_dialog(self, widget=None):
        """Layout the widgets in the main frame

        We'll let 'TkEnergy' layout the initial set of widgets,
        then add the extra widgets for controlling optimization
        """
        row = super().reset_dialog()

        # And our frame
        self["forceconstant frame"].grid(row=row, column=0, sticky=tk.EW, pady=10)
        row += 1

        return row
