# -*- coding: utf-8 -*-

"""The graphical part of a MOPAC vibrational node"""

import mopac_step
import seamm_widgets as sw
import tkinter as tk
import tkinter.ttk as ttk


class TkIR(mopac_step.TkEnergy):
    def __init__(
        self, tk_flowchart=None, node=None, canvas=None, x=120, y=20, w=200, h=50
    ):
        """Initialize a node

        Keyword arguments:
        """
        super().__init__(
            tk_flowchart=tk_flowchart, node=node, canvas=canvas, x=x, y=y, w=w, h=h
        )

    def create_dialog(self, title="MOPAC Infrared (Vibrational) Spectrum"):
        """Create the dialog!"""
        self.logger.debug("Creating the dialog")
        frame = super().create_dialog(title=title)

        P = self.node.parameters

        # Create the vibrational widgets
        vframe = self["vibrational frame"] = ttk.LabelFrame(
            frame, text="Vibrational Analysis", labelanchor=tk.N
        )
        row = 0
        widgets = []
        for key in mopac_step.IRParameters.parameters:
            self[key] = P[key].widget(vframe)
            self[key].grid(row=row, column=0, sticky=tk.EW)
            widgets.append(self[key])
            row += 1
        sw.align_labels(widgets, sticky=tk.E)

        # Create the structure-handling widgets
        sframe = self["structure frame"] = ttk.LabelFrame(
            frame, text="Configuration Handling", labelanchor=tk.N
        )
        row = 0
        widgets = []
        for key in ("structure handling", "configuration name"):
            self[key] = P[key].widget(sframe)
            self[key].grid(row=row, column=0, sticky=tk.EW)
            widgets.append(self[key])
            row += 1
        sw.align_labels(widgets)

        self.logger.debug("Finished creating the dialog")

    def reset_dialog(self, widget=None):
        """Layout the widgets in the main frame

        We'll let 'TkEnergy' layout the initial set of widgets,
        then add the extra widgets for controlling optimization
        """
        row = super().reset_dialog()

        # And our frame
        self["vibrational frame"].grid(row=row, column=0, sticky=tk.EW, pady=10)
        row += 1

        # And how to handle the configuration
        self["structure frame"].grid(row=row, column=0, sticky=tk.EW, pady=10)
        row += 1

        return row
