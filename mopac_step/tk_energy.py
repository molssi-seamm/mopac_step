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

        # Which controls to show come from the parameters' rules
        # (mopac_step.EnergyParameters), which the flowchart builder uses too. The
        # order and indentation stay here.
        P = self.node.parameters
        values = self._widget_values()

        def applies(key):
            return P.applies(key, values)

        widgets = []
        row = 0

        def add_full(key):
            nonlocal row
            self[key].grid(row=row, column=0, columnspan=2, sticky=tk.EW)
            widgets.append(self[key])
            row += 1

        def add_indented(keys):
            """Indented controls below their parent, aligned among themselves."""
            nonlocal row
            subwidgets = []
            for key in keys:
                if applies(key):
                    self[key].grid(row=row, column=1, sticky=tk.W)
                    subwidgets.append(self[key])
                    row += 1
            if len(subwidgets) > 0:
                sw.align_labels(subwidgets, sticky=tk.E)

        add_full("hamiltonian")
        add_full("calculation")

        # UHF for the SCF calculation; the CI controls for the CI calculations.
        for key in (
            "uhf",
            "number ci orbitals",
            "number doubly occupied ci orbitals",
            "ci root",
            "print ci details",
        ):
            if applies(key):
                add_full(key)

        # The convergence, with its relative or absolute value, or both when it is
        # given by a variable.
        add_full("convergence")
        add_indented(("relative", "absolute"))

        # Localized orbitals (MOZYME) for the SCF calculation
        if applies("MOZYME"):
            add_full("MOZYME")
            add_indented(("nMOZYME", "MOZYME follow-up"))

        add_full("COSMO")
        add_indented(("eps", "rsolve", "nspa", "disex"))

        add_full("calculate gradients")
        add_full("bond orders")

        sw.align_labels(widgets, sticky=tk.E)
        frame.columnconfigure(0, minsize=100)

        return row

    def _widget_values(self):
        """The dialog's current values, {name: value}, for the parameters' rules."""
        values = {}
        for key in self.node.parameters:
            if key == "results" or key not in self:
                continue
            try:
                value = self[key].get()
            except Exception:
                continue
            values[key] = value[0] if isinstance(value, tuple) else value
        return values
