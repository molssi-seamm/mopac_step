# -*- coding: utf-8 -*-
"""The graphical part of a MOPAC Energy node"""

import mopac_step
# import tkinter as tk
# import tkinter.ttk as ttk


class TkThermodynamics(mopac_step.TkEnergy):
    def __init__(self, node=None, canvas=None, x=None, y=None, w=None, h=None):
        '''Initialize a node

        Keyword arguments:
        '''
        super().__init__(node=node, canvas=canvas, x=x, y=y, w=w, h=h)

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

        self.dialog.title('MOPAC Thermodynamic Functions')
