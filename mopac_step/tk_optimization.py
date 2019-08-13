# -*- coding: utf-8 -*-

"""The graphical part of a MOPAC Energy node"""

import mopac_step
import seamm_widgets as sw
import tkinter as tk


class TkOptimization(mopac_step.TkEnergy):

    def __init__(
        self,
        tk_flowchart=None,
        node=None,
        canvas=None,
        x=120,
        y=20,
        w=200,
        h=50
    ):
        '''Initialize a node

        Keyword arguments:
        '''
        super().__init__(
            tk_flowchart=tk_flowchart,
            node=node,
            canvas=canvas,
            x=x,
            y=y,
            w=w,
            h=h
        )

    def right_click(self, event):
        """Probably need to add our dialog...
        """

        super().right_click(event)
        self.popup_menu.add_command(label="Edit..", command=self.edit)

        self.popup_menu.tk_popup(event.x_root, event.y_root, 0)

    def edit(self):
        """Present a dialog for editing the input for the MOPAC energy
        calculation"""

        super().edit()

        self.dialog.title('MOPAC Optimization')

    def reset_dialog(self, widget=None):
        """Layout the widgets in the main frame

        We'll let 'TkEnergy' layout the initial set of widgets,
        then add the extra widgets for controlling optimization
        """
        row = super().reset_dialog()

        convergence = self['convergence'].get()
        method = self['method'].get()

        widgets = []
        widgets_2 = []
        self['method'].grid(row=row, column=0, columnspan=2, sticky=tk.EW)
        widgets.append(self['method'])
        row += 1
        self['cycles'].grid(row=row, column=1, sticky=tk.EW)
        widgets_2.append(self['cycles'])
        row += 1
        if convergence not in ('normal', 'precise', 'relative'):
            self['gnorm'].grid(row=row, column=1, sticky=tk.EW)
            widgets_2.append(self['gnorm'])
            row += 1
        if method[0:2] == 'EF' or method[0] == '$':
            self['recalc'].grid(row=row, column=1, sticky=tk.EW)
            widgets_2.append(self['recalc'])
            row += 1
            self['dmax'].grid(row=row, column=1, sticky=tk.EW)
            widgets_2.append(self['dmax'])
            row += 1

        sw.align_labels(widgets)
        sw.align_labels(widgets_2)

        return row

    def setup_results(self, calculation='optimization'):
        """Layout the results tab of the dialog"""
        super().setup_results(calculation)
