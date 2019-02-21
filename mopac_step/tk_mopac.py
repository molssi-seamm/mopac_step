# -*- coding: utf-8 -*-
"""The graphical part of a MolSII MOPAC node"""

import molssi_workflow
import Pmw
import tkinter as tk
import tkinter.ttk as ttk


class TkMOPAC(molssi_workflow.TkNode):
    """The node_class is the class of the 'real' node that this
    class is the Tk graphics partner for
    """

    def __init__(self, tk_workflow=None, node=None, canvas=None,
                 namespace='org.molssi.workflow.mopac.tk',
                 x=120, y=20, w=200, h=50):
        '''Initialize a node

        Keyword arguments:
        '''
        self.namespace = namespace

        super().__init__(tk_workflow=tk_workflow, node=node,
                         canvas=canvas, x=x, y=y, w=w, h=h)

        self.create_dialog()

    def create_dialog(self):
        """Create the dialog!"""
        self.dialog = Pmw.Dialog(
            self.toplevel,
            buttons=('OK', 'Help', 'Cancel'),
            defaultbutton='OK',
            master=self.toplevel,
            title='Edit LAMMPS step',
            command=self.handle_dialog)
        self.dialog.withdraw()

        # make it large!
        sw = self.dialog.winfo_screenwidth()
        sh = self.dialog.winfo_screenheight()
        w = int(0.9 * sw)
        h = int(0.8 * sh)
        x = int(0.05 * sw / 2)
        y = int(0.1 * sh / 2)

        self.dialog.geometry('{}x{}+{}+{}'.format(w, h, x, y))

        frame = ttk.Frame(self.dialog.interior())
        frame.pack(expand=tk.YES, fill=tk.BOTH)
        self.mopac_tk_workflow = molssi_workflow.TkWorkflow(
            master=frame,
            namespace=self.namespace,
            workflow=self.node.mopac_workflow)
        self.mopac_tk_workflow.draw()

    def handle_dialog(self, result):
        if result is None or result == 'Cancel':
            self.dialog.deactivate(result)
            return

        if result == 'Help':
            # display help!!!
            return

        if result != "OK":
            self.dialog.deactivate(result)
            raise RuntimeError(
                "Don't recognize dialog result '{}'".format(result))

        self.dialog.deactivate(result)

    def right_click(self, event):
        """Probably need to add our dialog...
        """

        super().right_click(event)
        self.popup_menu.add_command(label="Edit..", command=self.edit)

        self.popup_menu.tk_popup(event.x_root, event.y_root, 0)

    def edit(self):
        """Present a dialog for editing the SMILES string
        """

        if self.dialog is None:
            self.create_dialog()

        self.dialog.activate(geometry='centerscreenfirst')

    def update_workflow(self, tk_workflow=None, workflow=None):
        """Update the nongraphical workflow. Only used in nodes that contain
        workflows"""

        super().update_workflow(
            workflow=self.node.mopac_workflow,
            tk_workflow=self.mopac_tk_workflow
        )

    def from_workflow(self, tk_workflow=None, workflow=None):
        """Recreate the graphics from the non-graphical workflow.
        Only used in nodes that contain workflow"""

        super().from_workflow(
            workflow=self.node.mopac_workflow,
            tk_workflow=self.mopac_tk_workflow
        )
