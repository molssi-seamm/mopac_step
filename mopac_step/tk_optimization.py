# -*- coding: utf-8 -*-

"""The graphical part of a MOPAC Energy node"""

import logging
from mopac_step import __version__, __git_revision__, keywords
from mopac_step import TkEnergy, OptimizationParameters
import seamm_widgets as sw
import tkinter as tk

logger = logging.getLogger(__name__)


class TkOptimization(TkEnergy):

    def __init__(
        self,
        title='Optimization',
        canvas=None,
        x=120,
        y=20,
        w=200,
        h=50,
        my_logger=logger,
        keyword_metadata=None
    ):
        '''Initialize a node

        Keyword arguments:
        '''

        # Call the constructor for the energy
        if keyword_metadata is None:
            keyword_metadata = keywords

        super().__init__(
            canvas=canvas,
            x=x,
            y=y,
            w=w,
            h=h,
            title=title,
            my_logger=my_logger,
            keyword_metadata=keyword_metadata
        )
        self.parameters = OptimizationParameters()

    @property
    def version(self):
        """The semantic version of this module.
        """
        return __version__

    @property
    def git_revision(self):
        """The git version of this module.
        """
        return __git_revision__

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
