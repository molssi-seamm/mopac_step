# -*- coding: utf-8 -*-
"""The graphical part of a MolSII MOPAC node"""

import molssi_workflow
import tkinter as tk
import tkinter.ttk as ttk


class TkMOPAC(molssi_workflow.TkNode):
    """The node_class is the class of the 'real' node that this
    class is the Tk graphics partner for
    """

    def __init__(self, node=None, canvas=None, x=None, y=None, w=None, h=None):
        '''Initialize a node

        Keyword arguments:
        '''
        super().__init__(node=node, canvas=canvas, x=x, y=y, w=w, h=h)

        self.dialog = None

    def create_dialog(self):
        """Create the dialog!"""

        self.dialog = tk.Toplevel(master=self.toplevel)
        self.dialog.transient(self.toplevel)
        self.dialog.withdraw()
        self.dialog.title('MolSSI MOPAC...')

        frame = ttk.Frame(self.dialog)
        frame.pack(side='top', fill=tk.BOTH, expand=1)

        self.flowchart = molssi_workflow.Flowchart(
            master=frame,
            extension_namespace='molssi.workflow.mopac.tk',
            main=False,
            workflow=self.node.mopac_workflow)
        self.node.mopac_workflow.gui_object = self.flowchart
        self.flowchart.draw()

        button_box = ttk.Frame(self.dialog)
        button_box.pack(side='bottom', expand=1, fill=tk.X)
        ok_button = ttk.Button(button_box, text="OK", command=self.handle_ok)
        ok_button.grid(row=0, column=0, sticky=tk.W)
        help_button = ttk.Button(
            button_box, text="Help", command=self.handle_help)
        help_button.grid(row=0, column=1)
        cancel_button = ttk.Button(
            button_box, text="Cancel", command=self.handle_cancel)
        cancel_button.grid(row=0, column=2, sticky=tk.E)
        button_box.grid_columnconfigure(0, weight=1)
        button_box.grid_columnconfigure(1, weight=1)
        button_box.grid_columnconfigure(2, weight=1)

    def right_click(self, event):
        """Probably need to add our dialog...
        """

        super().right_click(event)
        self.popup_menu.add_command(label="Edit..", command=self.edit)

        self.popup_menu.tk_popup(event.x_root, event.y_root, 0)

    def edit(self):
        """Present a dialog for editing the SMILES string
        """

        if not self.dialog:
            self.create_dialog()

        self._tmp = {'dialog': self.dialog}
        self.previous_grab = self.dialog.grab_current()
        self.dialog.grab_set()
        self.dialog.deiconify()
        self.dialog.attributes('-topmost', True)

    def handle_ok(self):
        self.dialog.grab_release()
        self.dialog.attributes('-topmost', False)
        self.dialog.withdraw()
        if self.previous_grab is not None:
            self.previous_grab().grab_set()
            self.previous_grab = None
        self._tmp = None

    def handle_help(self):
        print('Help')
        self.dialog.grab_release()
        self.dialog.attributes('-topmost', False)
        self.dialog.withdraw()
        if self.previous_grab is not None:
            self.previous_grab().grab_set()
            self.previous_grab = None
        self._tmp = None

    def handle_cancel(self):
        self.dialog.grab_release()
        self.dialog.attributes('-topmost', False)
        self.dialog.withdraw()
        if self.previous_grab is not None:
            self.previous_grab().grab_set()
            self.previous_grab = None
        self._tmp = None
