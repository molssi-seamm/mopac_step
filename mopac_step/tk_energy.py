# -*- coding: utf-8 -*-
"""The graphical part of a MOPAC Energy node"""

import molssi_workflow
import mopac_step
import Pmw
import tkinter as tk
import tkinter.ttk as ttk


class TkEnergy(molssi_workflow.TkNode):
    def __init__(self, tk_workflow=None, node=None,
                 canvas=None, x=None, y=None, w=None, h=None):
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

        # Create the dialog for editing this node
        self.dialog = Pmw.Dialog(
            self.toplevel,
            buttons=('OK', 'Help', 'Cancel'),
            defaultbutton='OK',
            master=self.toplevel,
            title='Edit Energy step',
            command=self.handle_dialog)
        self.dialog.withdraw()

        # The tabbed notebook
        notebook = ttk.Notebook(self.dialog.interior())
        notebook.pack(side='top', fill=tk.BOTH, expand=1)
        self._tmp['notebook'] = notebook

        # Main frame holding the widgets
        frame = ttk.Frame(self.dialog)
        self._tmp['frame'] = frame
        notebook.add(frame, text='Parameters', sticky=tk.NW)

        # which structure? may need to set default first...
        if not self.node.structure:
            if isinstance(self.node.previous(), molssi_workflow.StartNode):
                self.node.structure = 'initial'
            else:
                self.node.structure = 'current'

        structure_label = ttk.Label(frame, text='Structure:')
        structure = ttk.Combobox(
            frame,
            state='readonly',
            values=list(mopac_step.Energy.structures))
        structure.set(self.node.structure)
        self._tmp['structure'] = structure

        # which Hamiltonian?
        hamiltonian_label = ttk.Label(frame, text='Hamiltonian:')
        hamiltonian = ttk.Combobox(
            frame,
            state='readonly',
            values=list(mopac_step.Energy.hamiltonians))
        hamiltonian.set(self.node.hamiltonian)
        self._tmp['hamiltonian'] = hamiltonian

        # What convergence?
        convergence_label = ttk.Label(frame, text='Convergence:')
        convergence = ttk.Combobox(
            frame,
            state='readonly',
            values=list(mopac_step.Energy.convergences))
        convergence.bind("<<ComboboxSelected>>", self.reset_dialog)
        convergence.set(self.node.convergence)
        self._tmp['convergence'] = convergence

        structure_label.grid(row=0, column=0, columnspan=2, sticky=tk.E)
        structure.grid(row=0, column=2, sticky=tk.W)
        hamiltonian_label.grid(row=1, column=0, columnspan=2, sticky=tk.E)
        hamiltonian.grid(row=1, column=2, sticky=tk.W)
        convergence_label.grid(row=2, column=0, columnspan=2, sticky=tk.E)
        convergence.grid(row=2, column=2, sticky=tk.W)

        subframe = ttk.Frame(frame)
        self._tmp['subframe'] = subframe
        subframe.grid(row=3, column=1, columnspan=5)

        frame.grid_columnconfigure(0, minsize=30)

        # Second tab for adding keywords
        add_to_input = ttk.Frame(self.dialog)
        self._tmp['add_to_input'] = add_to_input
        notebook.add(add_to_input, text='Add to input', sticky=tk.NW)

        # And finally, lay the wodgets out
        self.reset_dialog()

    def reset_dialog(self, widget=None):
        current = self._tmp['convergence'].get()
        frame = self._tmp['subframe']
        for slave in frame.grid_slaves():
            slave.destroy()

        if current == 'relative':
            relscf_label = ttk.Label(frame, text='Relative:')
            relscf = ttk.Entry(frame, width=15)
            relscf.insert(0, self.node.relscf)
            self._tmp['relscf'] = relscf
            relscf_label.grid(row=2, column=1, sticky=tk.E)
            relscf.grid(row=2, column=2, sticky=tk.W)
        elif current == 'absolute':
            scfcrt_label = ttk.Label(frame, text='Absolute:')
            scfcrt = ttk.Entry(frame, width=15)
            scfcrt.insert(0, self.node.scfcrt)
            self._tmp['scfcrt'] = scfcrt
            scfcrt_units = ttk.Label(frame, text='kcal/mol')
            scfcrt_label.grid(row=2, column=1, sticky=tk.E)
            scfcrt.grid(row=2, column=2, sticky=tk.W)
            scfcrt_units.grid(row=2, column=3, sticky=tk.W)

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

        self.node.structure = self._tmp['structure'].get()
        self.node.hamiltonian = self._tmp['hamiltonian'].get()
        self.node.convergence = self._tmp['convergence'].get()
        if self.node.convergence == 'relative':
            self.node.relscf = self._tmp['relscf'].get()
        elif self.node.convergence == 'absolute':
            self.node.scfcrt = self._tmp['scfcrt'].get()
