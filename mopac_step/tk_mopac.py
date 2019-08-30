# -*- coding: utf-8 -*-

"""The graphical part of a MolSII MOPAC node"""

import seamm
import Pmw
import tkinter as tk
import tkinter.ttk as ttk


class TkMOPAC(seamm.TkNode):
    """The node_class is the class of the 'real' node that this
    class is the Tk graphics partner for
    """

    def __init__(
        self,
        tk_flowchart=None,
        node=None,
        canvas=None,
        namespace='org.molssi.seamm.mopac.tk',
        x=120,
        y=20,
        w=200,
        h=50
    ):
        '''Initialize a node

        Keyword arguments:
        '''
        self.namespace = namespace

        super().__init__(
            tk_flowchart=tk_flowchart,
            node=node,
            canvas=canvas,
            x=x,
            y=y,
            w=w,
            h=h
        )

        self.create_dialog()

    def create_dialog(self):
        """Create the dialog!"""
        self.dialog = Pmw.Dialog(
            self.toplevel,
            buttons=('OK', 'Help', 'Cancel'),
            defaultbutton='OK',
            master=self.toplevel,
            title='Edit LAMMPS step',
            command=self.handle_dialog
        )
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
        self.mopac_tk_flowchart = seamm.TkFlowchart(
            master=frame,
            namespace=self.namespace,
            flowchart=self.node.subflowchart
        )
        self.mopac_tk_flowchart.draw()

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
                "Don't recognize dialog result '{}'".format(result)
            )

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

    def update_flowchart(self, tk_flowchart=None, flowchart=None):
        """Update the nongraphical flowchart. Only used in nodes that contain
        flowcharts"""

        super().update_flowchart(
            flowchart=self.node.subflowchart,
            tk_flowchart=self.mopac_tk_flowchart
        )

    def from_flowchart(self, tk_flowchart=None, flowchart=None):
        """Recreate the graphics from the non-graphical flowchart.
        Only used in nodes that contain flowchart"""

        super().from_flowchart(
            flowchart=self.node.subflowchart,
            tk_flowchart=self.mopac_tk_flowchart
        )
