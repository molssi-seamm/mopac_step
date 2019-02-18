# -*- coding: utf-8 -*-
"""The graphical part of a MOPAC Energy node"""

import molssi_workflow
import mopac_step
import Pmw
import tkinter as tk
import tkinter.ttk as ttk

from itertools import takewhile


def lcp(*s):
    return ''.join(a for a, b in takewhile(lambda x: x[0] == x[1],
                                           zip(min(s), max(s))))


class TkEnergy(molssi_workflow.TkNode):
    def __init__(self, tk_workflow=None, node=None, canvas=None,
                 x=120, y=20, w=200, h=50):
        '''Initialize a node

        Keyword arguments:
        '''
        self.keyword_dialog = None
        self.keyword_cb = None
        self.value_cb = None
        self.set_keyword_cb = None
        self.tmp_keywords = None

        s = ttk.Style()
        s.configure('Red.TEntry', foreground='red')

        super().__init__(tk_workflow=tk_workflow, node=node,
                         canvas=canvas, x=x, y=y, w=w, h=h)

    def right_click(self, event):
        """Probably need to add our dialog...
        """

        super().right_click(event)
        self.popup_menu.add_command(label="Edit..", command=self.edit)

        self.popup_menu.tk_popup(event.x_root, event.y_root, 0)

    def create_dialog(self):
        """Create the dialog!"""
        self.dialog = Pmw.Dialog(
            self.toplevel,
            buttons=('OK', 'Help', 'Cancel'),
            master=self.toplevel,
            title='Edit Energy step',
            command=self.handle_dialog)
        self.dialog.withdraw()

        # The tabbed notebook
        notebook = ttk.Notebook(self.dialog.interior())
        notebook.pack(side='top', fill=tk.BOTH, expand=1)
        self._widget['notebook'] = notebook

        # Main frame holding the widgets
        frame = ttk.Frame(notebook)
        self._widget['frame'] = frame
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
        self._widget['structure'] = structure

        # which Hamiltonian?
        hamiltonian_label = ttk.Label(frame, text='Hamiltonian:')
        hamiltonian = ttk.Combobox(
            frame,
            state='readonly',
            values=list(mopac_step.Energy.hamiltonians))
        hamiltonian.set(self.node.hamiltonian)
        self._widget['hamiltonian'] = hamiltonian

        # What convergence?
        convergence_label = ttk.Label(frame, text='Convergence:')
        convergence = ttk.Combobox(
            frame,
            state='readonly',
            values=list(mopac_step.Energy.convergences))
        convergence.bind("<<ComboboxSelected>>", self.reset_dialog)
        convergence.set(self.node.convergence)
        self._widget['convergence'] = convergence

        structure_label.grid(row=0, column=0, columnspan=2, sticky=tk.E)
        structure.grid(row=0, column=2, sticky=tk.W)
        hamiltonian_label.grid(row=1, column=0, columnspan=2, sticky=tk.E)
        hamiltonian.grid(row=1, column=2, sticky=tk.W)
        convergence_label.grid(row=2, column=0, columnspan=2, sticky=tk.E)
        convergence.grid(row=2, column=2, sticky=tk.W)

        subframe = ttk.Frame(frame)
        self._widget['subframe'] = subframe
        subframe.grid(row=3, column=1, columnspan=5)

        frame.grid_columnconfigure(0, minsize=30)

        # Second tab for adding keywords
        add_to_input = ttk.Frame(notebook)
        self._widget['add_to_input'] = add_to_input
        notebook.add(add_to_input, text='Add to input', sticky=tk.NW)

    def edit(self):
        """Present a dialog for editing the input for the MOPAC energy
        calculation"""

        self.tmp_keywords = self.node.keywords
        # Create the dialog for editing this node if needed
        if self.dialog is None:
            self.create_dialog()
            self.reset_dialog()
            self.layout_keywords()

        self.dialog.activate(geometry='centerscreenfirst')

    def reset_dialog(self, widget=None):
        current = self._widget['convergence'].get()
        frame = self._widget['subframe']
        for slave in frame.grid_slaves():
            slave.destroy()

        if current == 'relative':
            relscf_label = ttk.Label(frame, text='Relative:')
            relscf = ttk.Entry(frame, width=15)
            relscf.insert(0, self.node.relscf)
            self._widget['relscf'] = relscf
            relscf_label.grid(row=2, column=1, sticky=tk.E)
            relscf.grid(row=2, column=2, sticky=tk.W)
        elif current == 'absolute':
            scfcrt_label = ttk.Label(frame, text='Absolute:')
            scfcrt = ttk.Entry(frame, width=15)
            scfcrt.insert(0, self.node.scfcrt)
            self._widget['scfcrt'] = scfcrt
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

        self.node.structure = self._widget['structure'].get()
        self.node.hamiltonian = self._widget['hamiltonian'].get()
        self.node.convergence = self._widget['convergence'].get()
        if self.node.convergence == 'relative':
            self.node.relscf = self._widget['relscf'].get()
        elif self.node.convergence == 'absolute':
            self.node.scfcrt = self._widget['scfcrt'].get()

    def handle_keyword(self, keyword, w_name, value, before, action, changed):
        """Handle typing in a combobox for the keyword

        Arguments:
            keyword: the MOPAC keyword
            w_name: the widget name
            value: the value *after* the keystroke
            before: the value before the keystroke
            action: 0 for deletion, 1 for insertion
            changed: the text being inserted or deleted
        """

        w = self.dialog.nametowidget(w_name)  # nopep8
        print('Validating the keyword')

        if changed == '\t':
            changed = 'TAB'
        print('\tkeyword: {}'.format(keyword))
        print('\t  value: {}'.format(value))
        print('\t before: {}'.format(before))
        print('\t action: {}'.format(action))
        print('\tchanged: {}'.format(changed))

        if value in mopac_step.keywords:
            w.configure(style='TEntry')
        else:
            w.configure(style='Red.TEntry')

        return True

    def post_cb(self, row):
        """Handle post command for the combobox 'w'

        Arguments:
            w_name: the name of the widget (from %W)
        """

        w = self._widget['keyword_'+str(row)]
        current = w.get().upper()

        keywords = []
        for keyword in mopac_step.keywords:
            if keyword.startswith(current):
                keywords.append(keyword)

        w.configure(values=sorted(keywords))

    def set_keyword_cb(self, event, w, row=None):
        print(event)
        print(w)
        print(w.get())
        print(row)

    def layout_keywords(self):
        """Layout the table of additional keywords and any arguments they
        need"""

        w = self._widget
        frame = w['add_to_input']

        # Unpack any widgets
        for slave in frame.grid_slaves():
            slave.destroy()

        # Callbacks
        if self.keyword_cb is None:
            self.keyword_cb = frame.register(self.handle_keyword)
        if self.value_cb is None:
            self.value_cb = frame.register(self.validate_keyword_value)
        if self.set_keyword_cb is None:
            self.set_keyword_cb = frame.register(self.set_keyword)

        row = -1
        for d in self.tmp_keywords:
            row += 1
            keyword = d['keyword']
            widgets = d['widgets'] = {}

            # The button to remove a row...
            w = widgets['remove'] = ttk.Button(
                frame,
                text='-',
                width=5,
                command=lambda row=row: self.remove_keyword(row),
                takefocus=False,
            )
            w.grid(row=row, column=0, sticky=tk.W)

            # the name of the keyword
            w = ttk.Entry(frame,
                          width=30,
                          validate='key',
                          validatecommand=(self.keyword_cb, keyword,
                                           '%W', '%P', '%s', '%d', '%S'),
                          takefocus=False,
                          style='Red.TEntry',
                          )
            widgets['entry'] = w
            col = 0
            w.grid(row=row, column=col, stick=tk.EW)
            w.bind('<KeyPress-Tab>',
                   lambda event=None, row=row: self.handle_tab(event, row))
            col += 1

            if keyword == '':
                continue

            definition = mopac_step.keywords[keyword]
            if 'value' in definition:
                if 'value' not in keyword:
                    if 'value optional' in keyword and \
                       keyword['value optional']:
                        keyword['value'] = ''
                    else:
                        keyword['value'] = definition['default']

                w = ttk.Entry(frame,
                              width=15,
                              validate='key',
                              validatecommand=(self.value_cb, keyword,
                                               '%W', '%P', '%s', '%d', '%S'),
                              takefocus=False,
                              )
                widgets['value'] = w
                w.insert('end', keyword['value'])
                w.grid(row=row, column=col, sticky=tk.EW)

        # The button to add a row...
        row += 1
        w = self._widget['add keyword'] = ttk.Button(
            frame,
            text='+',
            width=5,
            command=self.add_keyword,
            takefocus=False,
        )
        w.grid(row=row, column=0, sticky=tk.W)

    def add_keyword(self, keyword=''):
        """Add a keyword to the input"""
        self.node.keywords.append({'keyword': keyword})
        self.layout_keywords()

    def post_keyword_dialog(self):
        """Put up the dialog with the appropriate list of keywords"""
        if self.keyword_dialog is None:
            """Create the dialog!"""
            self.keyword_dialog = Pmw.Dialog(
                self.toplevel,
                buttons=('OK', 'Help', 'Cancel'),
                defaultbutton='OK',
                master=self.dialog,
                title='Add keyword',
                command=self.handle_keyword_dialog)
            self.keyword_dialog.withdraw()
            frame = ttk.Frame(self.keyword_dialog.interior())
            frame.pack(expand=tk.YES, fill=tk.BOTH)
            self._widget['keyword frame'] = frame

            w = self._widget['keyword tree'] = ttk.Treeview(
                frame,
                columns=('Keyword', 'Description'),
            )
            w.pack(expand=tk.YES, fill=tk.BOTH)

            w.heading('Keyword', text='Keyword')
            w.heading('Description', text='Description')
            w.column('#0', minwidth=1, width=1, stretch=False)
            w.column('Keyword', width=100, stretch=False)

            for keyword in mopac_step.keywords:
                description = mopac_step.keywords[keyword]['description']
                w.insert('', 'end', iid=keyword, values=(keyword, description))

        self.keyword_dialog.activate(geometry='centerscreenfirst')

    def handle_keyword_dialog(self, result):
        if result is None or result == 'Cancel':
            self.keyword_dialog.deactivate(result)
            return

        if result == 'Help':
            # display help!!!
            return

        if result != "OK":
            self.keyword_dialog.deactivate(result)
            raise RuntimeError(
                "Don't recognize dialog result '{}'".format(result))

        self.keyword_dialog.deactivate(result)

        keyword = self._widget['keyword tree'].selection()
        print(keyword)

    def validate_keyword_value(self, keyword, w_name, value, before, action,
                               changed):
        """Handle typing in a combobox for the keyword

        Arguments:
            keyword: the MOPAC keyword
            w_name: the widget name
            value: the value *after* the keystroke
            before: the value before the keystroke
            action: 0 for deletion, 1 for insertion
            changed: the text being inserted or deleted
        """

        w = self.dialog.nametowidget(w_name)  # nopep8
        print('Validating the value of a keyword')
        print('\tkeyword: {}'.format(keyword))
        print('\t  value: {}'.format(value))
        print('\t before: {}'.format(before))
        print('\t action: {}'.format(action))
        print('\tchanged: {}'.format(changed))

        return True

    def remove_keyword(self, row=None):
        """Remove a keyword from dd to input"""
        print('remove row {}'.format(row))

    def handle_tab(self, event=None, row=None):
        """Handle a tab in a keyword entry field"""
        print('Caught tab in row {}'.format(row))
        print(event)

        data = self.tmp_keywords[row]
        w = data['widgets']['entry']
        current = w.get()

        defs = mopac_step.keywords
        keywords = []
        for keyword in defs:
            if keyword.startswith(current):
                keywords.append(keyword)

        prefix = lcp(*keywords)
        print('prefix = "{}", current = "{}"'.format(prefix, current))

        if prefix != current:
            w.delete(0, 'end')
            w.insert('end', prefix)
            if prefix in defs:
                w.configure(style='TEntry')
        else:
            if self.popup_menu is not None:
                self.popup_menu.destroy()

            self.popup_menu = tk.Menu(self.dialog.interior(), tearoff=0)
            for keyword in keywords:
                description = defs[keyword]['description']
                self.popup_menu.add_command(
                    label='{}: {}'.format(keyword, description),
                    command=(self.set_keyword_cb, w, keyword)
                )
                x, y = w.winfo_pointerxy()
            self.popup_menu.tk_popup(x, y, 0)
        return 'break'

    def set_keyword(self, w_name, keyword):
        """Set the value in a widget to the full keyword"""
        w = self.dialog.nametowidget(w_name)
        w.delete(0, 'end')
        w.insert('end', keyword)
        w.configure(style='TEntry')
