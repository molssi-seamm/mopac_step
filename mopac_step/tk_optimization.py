# -*- coding: utf-8 -*-

"""The graphical part of a MOPAC Energy node"""

import mopac_step
import seamm_widgets as sw
import tkinter as tk
import tkinter.ttk as ttk


class TkOptimization(mopac_step.TkEnergy):
    def __init__(
        self, tk_flowchart=None, node=None, canvas=None, x=120, y=20, w=200, h=50
    ):
        """Initialize a node

        Keyword arguments:
        """
        super().__init__(
            tk_flowchart=tk_flowchart, node=node, canvas=canvas, x=x, y=y, w=w, h=h
        )
        self.mopac_parameters = self.node.parent.parameters

    def right_click(self, event):
        """Probably need to add our dialog..."""

        super().right_click(event)
        self.popup_menu.add_command(label="Edit..", command=self.edit)

        self.popup_menu.tk_popup(event.x_root, event.y_root, 0)

    def create_dialog(self, title="MOPAC Optimization", calculation="optimization"):
        """Create the dialog!"""
        self.logger.debug("Creating the dialog")

        frame = super().create_dialog(title=title, calculation="optimization")

        P = self.node.parameters

        # Create the structure-handling widgets
        sframe = self["structure frame"] = ttk.LabelFrame(
            frame, text="Configuration Handling", labelanchor=tk.N
        )
        row = 0
        widgets = []
        for key in ("structure handling", "configuration name"):
            self[key].destroy()
            self[key] = P[key].widget(sframe)
            self[key].grid(row=row, column=0, sticky=tk.EW)
            widgets.append(self[key])
            row += 1
        sw.align_labels(widgets)

        self.logger.debug("Finished creating the dialog")

        return frame

    def reset_dialog(self, widget=None):
        """Layout the widgets in the main frame

        We'll let 'TkEnergy' layout the initial set of widgets,
        then add the extra widgets for controlling optimization
        """
        row = super().reset_dialog()

        convergence = self["convergence"].get()
        method = self["method"].get()

        widgets = []
        widgets_2 = []
        self["method"].grid(row=row, column=0, columnspan=2, sticky=tk.EW)
        widgets.append(self["method"])
        row += 1
        self["cycles"].grid(row=row, column=1, sticky=tk.EW)
        widgets_2.append(self["cycles"])
        row += 1
        if convergence not in ("normal", "precise", "relative"):
            self["gnorm"].grid(row=row, column=1, sticky=tk.EW)
            widgets_2.append(self["gnorm"])
            row += 1
        if method[0:2] == "EF" or method[0] == "$":
            self["recalc"].grid(row=row, column=1, sticky=tk.EW)
            widgets_2.append(self["recalc"])
            row += 1
            self["dmax"].grid(row=row, column=1, sticky=tk.EW)
            widgets_2.append(self["dmax"])
            row += 1

        sw.align_labels(widgets)
        sw.align_labels(widgets_2)

        self["structure frame"].grid(row=row, column=0, columnspan=2, sticky=tk.EW)
        row += 1

        return row
