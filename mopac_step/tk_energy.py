# -*- coding: utf-8 -*-

"""The graphical part of a MOPAC Energy node"""

import logging
import tkinter as tk
import tkinter.ttk as ttk

import mopac_step
import seamm
import seamm_widgets as sw

logger = logging.getLogger(__name__)


class TkEnergy(seamm.TkNode):
    def __init__(
        self,
        tk_flowchart=None,
        node=None,
        canvas=None,
        x=120,
        y=20,
        w=200,
        h=50,
        my_logger=logger,
    ):
        """Initialize the graphical Tk MOPAC energy step

        Keyword arguments:
        """
        self.results_widgets = []

        super().__init__(
            tk_flowchart=tk_flowchart,
            node=node,
            canvas=canvas,
            x=x,
            y=y,
            w=w,
            h=h,
            my_logger=my_logger,
        )

    def right_click(self, event):
        """Probably need to add our dialog..."""

        super().right_click(event)
        self.popup_menu.add_command(label="Edit..", command=self.edit)

        self.popup_menu.tk_popup(event.x_root, event.y_root, 0)

    def create_dialog(self, title="Edit MOPAC Energy Step"):
        """Create the dialog!"""
        self.logger.debug("Creating the dialog")
        frame = super().create_dialog(title=title, widget="notebook", results_tab=True)

        P = self.node.parameters

        # Just write input
        self["input only"] = P["input only"].widget(frame)

        # Frame to isolate widgets
        e_frame = self["energy frame"] = ttk.LabelFrame(
            frame,
            borderwidth=4,
            relief="sunken",
            text="Hamiltonian Parameters",
            labelanchor="n",
            padding=10,
        )

        # Create all the widgets
        for key in mopac_step.EnergyParameters.parameters:
            if key not in ("results", "extra keywords", "create tables", "input only"):
                self[key] = P[key].widget(e_frame)

        # Set the callbacks for changes
        for widget in ("calculation", "convergence", "MOZYME", "COSMO"):
            w = self[widget]
            w.combobox.bind("<<ComboboxSelected>>", self.reset_energy_frame)
            w.combobox.bind("<Return>", self.reset_energy_frame)
            w.combobox.bind("<FocusOut>", self.reset_energy_frame)

        self.setup_results()

        self.logger.debug("Finished creating the dialog")

        return frame

    def reset_dialog(self, widget=None):
        frame = self["frame"]
        for slave in frame.grid_slaves():
            slave.grid_forget()

        row = 0
        # Whether to just write input
        self["input only"].grid(row=row, column=0, sticky=tk.W)
        row += 1

        # Put in the energy frame
        self["energy frame"].grid(row=row, column=0, sticky=tk.EW)
        row += 1

        # and the widgets in it
        self.reset_energy_frame()

        return row

    def reset_energy_frame(self, widget=None):
        frame = self["energy frame"]
        for slave in frame.grid_slaves():
            slave.grid_forget()

        calculation = self["calculation"].get()
        convergence = self["convergence"].get()
        cosmo = self["COSMO"].get()
        mozyme = self["MOZYME"].get()

        widgets = []
        row = 0
        for key in ("hamiltonian", "calculation"):
            self[key].grid(row=row, column=0, columnspan=2, sticky=tk.EW)
            widgets.append(self[key])
            row += 1

        if "hf" in calculation.lower():
            for key in ("uhf",):
                self[key].grid(row=row, column=0, columnspan=2, sticky=tk.EW)
                widgets.append(self[key])
                row += 1

        if "ci" in calculation.lower():
            for key in (
                "number ci orbitals",
                "number doubly occupied ci orbitals",
                "ci root",
                "print ci details",
            ):
                self[key].grid(row=row, column=0, columnspan=2, sticky=tk.EW)
                widgets.append(self[key])
                row += 1

        for key in ("convergence",):
            self[key].grid(row=row, column=0, columnspan=2, sticky=tk.EW)
            widgets.append(self[key])
            row += 1

        if convergence == "relative":
            self["relative"].grid(row=row, column=1, sticky=tk.W)
            row += 1
        elif convergence == "absolute":
            self["absolute"].grid(row=row, column=1, sticky=tk.W)
            row += 1
        elif convergence not in ("normal", "precise"):
            # variable ... so put in all possibilities
            self["relative"].grid(row=row, column=1, sticky=tk.W)
            row += 1
            self["absolute"].grid(row=row, column=1, sticky=tk.W)
            row += 1
            sw.align_labels((self["relative"], self["absolute"]), sticky=tk.E)

        if "hf" in calculation.lower():
            self["MOZYME"].grid(row=row, column=0, columnspan=2, sticky=tk.EW)
            widgets.append(self["MOZYME"])
            row += 1
            subwidgets = []
            if mozyme != "always" and mozyme != "never":
                self["nMOZYME"].grid(row=row, column=1, sticky=tk.W)
                subwidgets.append(self["nMOZYME"])
                row += 1
            if mozyme != "never":
                self["MOZYME follow-up"].grid(row=row, column=1, sticky=tk.W)
                subwidgets.append(self["MOZYME follow-up"])
                row += 1
            sw.align_labels(subwidgets, sticky=tk.E)

        self["COSMO"].grid(row=row, column=0, columnspan=2, sticky=tk.EW)
        widgets.append(self["COSMO"])
        row += 1
        if cosmo == "yes":
            widgets1 = []

            for key in ("eps", "rsolve", "nspa", "disex"):
                self[key].grid(row=row, column=1, sticky=tk.W)
                widgets1.append(self[key])
                row += 1
            sw.align_labels(widgets1, sticky=tk.E)

        for key in ("calculate gradients", "bond orders"):
            self[key].grid(row=row, column=0, columnspan=2, sticky=tk.EW)
            widgets.append(self[key])
            row += 1

        sw.align_labels(widgets, sticky=tk.E)
        frame.columnconfigure(0, minsize=100)

        return row
