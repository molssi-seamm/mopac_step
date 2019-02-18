# -*- coding: utf-8 -*-
"""The graphical part of a MOPAC Energy node"""

import mopac_step
# import tkinter as tk
# import tkinter.ttk as ttk


class TkIR(mopac_step.TkEnergy):
    def __init__(self, tk_workflow=None, node=None, canvas=None,
                 x=120, y=20, w=200, h=50):
        '''Initialize a node

        Keyword arguments:
        '''
        super().__init__(tk_workflow=tk_workflow, node=node,
                         canvas=canvas, x=x, y=y, w=w, h=h)

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

        self.dialog.title('MOPAC Infrared (Vibrational) Spectrum')
