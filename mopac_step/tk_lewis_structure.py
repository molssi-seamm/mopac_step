# -*- coding: utf-8 -*-

"""The graphical part of the Lewsi structure node"""

import logging
import tkinter as tk

import mopac_step
import seamm
import seamm_widgets as sw

logger = logging.getLogger(__name__)


class TkLewisStructure(seamm.TkNode):
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

    def create_dialog(self, title="Edit Lewis Structure Step"):
        """Create the dialog!"""
        self.logger.debug("Creating the dialog")
        frame = super().create_dialog(title=title)

        # Create all the widgets
        P = self.node.parameters
        row = 0
        widgets = []
        for key in mopac_step.LewisStructureParameters.parameters:
            if key not in ("results",):
                w = self[key] = P[key].widget(frame)
                w.grid(row=row, column=0, sticky=tk.EW)
                widgets.append(w)
                row += 1
        sw.align_labels(widgets, sticky=tk.E)

        self.setup_results()

        self.logger.debug("Finished creating the dialog")

        return frame
