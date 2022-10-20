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

    def create_dialog(self, title="MOPAC Optimization"):
        """Create the dialog!"""
        self.logger.debug("Creating the dialog")

        frame = super().create_dialog(title=title)

        P = self.node.parameters

        # Create the optimization widgets
        oframe = self["optimization frame"] = ttk.LabelFrame(
            frame, text="Optimization", labelanchor=tk.N
        )
        row = 0
        for key in mopac_step.OptimizationParameters.parameters:
            self[key] = P[key].widget(oframe)
            row += 1
        for key in mopac_step.structure_handling_parameters:
            self[key] = P[key].widget(oframe)
            row += 1

        # Set the callbacks for changes
        for widget in ("method", "convergence", "LatticeOpt"):
            w = self[widget]
            w.combobox.bind(
                "<<ComboboxSelected>>", self.reset_optimization_frame, add="+"
            )
            w.combobox.bind("<Return>", self.reset_optimization_frame, add="+")
            w.combobox.bind("<FocusOut>", self.reset_optimization_frame, add="+")

        self.logger.debug("Finished creating the dialog")

        return frame

    def reset_dialog(self, widget=None):
        row = super().reset_dialog()

        self["optimization frame"].grid(row=row, column=0, sticky=tk.EW)
        row += 1

        # And the widgets in our frame
        self.reset_optimization_frame()

        return row

    def reset_optimization_frame(self, widget=None):
        """Layout the widgets in the optimization frame

        We'll let 'TkEnergy' layout the initial set of widgets,
        then add the extra widgets for controlling optimization
        """
        frame = self["optimization frame"]
        for slave in frame.grid_slaves():
            slave.grid_forget()

        convergence = self["convergence"].get()
        method = self["method"].get()
        lattice_opt = self["LatticeOpt"].get()

        widgets = []
        widgets_2 = []
        row = 0

        self["LatticeOpt"].grid(row=row, column=0, columnspan=2, sticky=tk.EW)
        widgets.append(self["LatticeOpt"])
        row += 1

        if lattice_opt == "Yes":
            self["pressure"].grid(row=row, column=1, sticky=tk.EW)
            row += 1

        self["method"].grid(row=row, column=0, columnspan=2, sticky=tk.EW)
        widgets.append(self["method"])
        row += 1

        self["cycles"].grid(row=row, column=1, sticky=tk.EW)
        widgets_2.append(self["cycles"])
        row += 1

        if convergence not in ("normal", "precise"):
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

        for key in ("structure handling", "configuration name"):
            self[key].grid(row=row, column=0, columnspan=2, sticky=tk.EW)
            widgets.append(self[key])
            row += 1

        sw.align_labels(widgets, sticky=tk.E)
        sw.align_labels(widgets_2, sticky=tk.E)

        frame.columnconfigure(0, minsize=100)

        return row
