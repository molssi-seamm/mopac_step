# -*- coding: utf-8 -*-

"""The graphical part of a MOPAC Energy node"""

import logging
import seamm
import seamm_widgets as sw
import mopac_step
import Pmw
import tkinter as tk
import tkinter.ttk as ttk

from itertools import takewhile

logger = logging.getLogger(__name__)


def lcp(*s):
    """Longest common prefix of strings"""
    return ''.join(
        a for a, b in takewhile(lambda x: x[0] == x[1], zip(min(s), max(s)))
    )


class TkEnergy(seamm.TkNode):

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
        self.keyword_dialog = None
        self.keyword_cb = None
        self.value_cb = None
        self.set_keyword_cb = None
        self.tmp_keywords = None
        self.results_widgets = []

        s = ttk.Style()
        s.configure('Red.TEntry', foreground='red')

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

    def create_dialog(self):
        """Create the dialog!"""
        self.dialog = Pmw.Dialog(
            self.toplevel,
            buttons=('OK', 'Help', 'Cancel'),
            master=self.toplevel,
            title='Edit Energy step',
            command=self.handle_dialog
        )
        self.dialog.withdraw()

        # The tabbed notebook
        notebook = ttk.Notebook(self.dialog.interior())
        notebook.pack(side='top', fill=tk.BOTH, expand=tk.YES)
        self['notebook'] = notebook

        # Main frame holding the widgets
        frame = ttk.Frame(notebook)
        self['frame'] = frame
        notebook.add(frame, text='Parameters', sticky=tk.NW)

        # Create all the widgets
        P = self.node.parameters
        for key in P:
            if key not in ('results', 'extra keywords', 'create tables'):
                self[key] = P[key].widget(frame)

        # bindings...
        self['convergence'].combobox.bind(
            "<<ComboboxSelected>>", self.reset_dialog
        )
        self['convergence'].combobox.bind("<Return>", self.reset_dialog)
        self['convergence'].combobox.bind("<FocusOut>", self.reset_dialog)

        # Second tab for results
        rframe = self['results frame'] = ttk.Frame(notebook)
        notebook.add(rframe, text='Results', sticky=tk.NSEW)

        var = self.tk_var['create tables'] = tk.IntVar()
        if P['create tables'].value == 'yes':
            var.set(1)
        else:
            var.set(0)
        self['create tables'] = ttk.Checkbutton(
            rframe, text='Create tables if needed', variable=var
        )
        self['create tables'].grid(row=0, column=0, sticky=tk.W)

        self['results'] = sw.ScrolledColumns(
            rframe,
            columns=[
                'Result',
                'Save',
                'Variable name',
                'In table',
                'Column name',
            ]
        )
        self['results'].grid(row=1, column=0, sticky=tk.NSEW)
        rframe.columnconfigure(0, weight=1)
        rframe.rowconfigure(1, weight=1)

        self.setup_results()

        # Third tab for adding keywords
        self['add_to_input'] = ttk.Frame(notebook)
        notebook.add(self['add_to_input'], text='Add to input', sticky=tk.NW)

    def setup_results(self, calculation='single point energy'):
        """Layout the results tab of the dialog"""
        results = self.node.parameters['results'].value

        self.results_widgets = []
        table = self['results']
        frame = table.interior()

        row = 0
        for key, entry in mopac_step.properties.items():
            if 'calculation' not in entry:
                continue
            if calculation not in entry['calculation']:
                continue
            if 'dimensionality' not in entry:
                continue
            if entry['dimensionality'] != 'scalar':
                continue

            widgets = []
            widgets.append(key)

            table.cell(row, 0, entry['description'])

            # variable
            var = self.tk_var[key] = tk.IntVar()
            var.set(0)
            w = ttk.Checkbutton(frame, variable=var)
            table.cell(row, 1, w)
            widgets.append(w)
            e = ttk.Entry(frame, width=15)
            e.insert(0, key.lower())
            table.cell(row, 2, e)
            widgets.append(e)

            if key in results:
                if 'variable' in results[key]:
                    var.set(1)
                    e.delete(0, tk.END)
                    e.insert(0, results[key]['variable'])

            # table
            w = ttk.Combobox(frame, width=10)
            table.cell(row, 3, w)
            widgets.append(w)
            e = ttk.Entry(frame, width=15)
            e.insert(0, key.lower())
            table.cell(row, 4, e)
            widgets.append(e)

            if key in results:
                if 'table' in results[key]:
                    w.set(results[key]['table'])
                    e.delete(0, tk.END)
                    e.insert(0, results[key]['column'])

            self.results_widgets.append(widgets)
            row += 1

        # And make the dialog wide enough
        frame.update_idletasks()
        width = frame.winfo_width() + 70  # extra space for frame, etc.
        height = frame.winfo_height()
        sw = frame.winfo_screenwidth()
        sh = frame.winfo_screenheight()

        if width > sw:
            width = int(0.9 * sw)
        if height > sh:
            height = int(0.9 * sh)

        self.dialog.geometry('{}x{}'.format(width, height))

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
        convergence = self['convergence'].get()

        frame = self['frame']
        for slave in frame.grid_slaves():
            slave.grid_forget()

        widgets = []
        row = 0
        self['structure'].grid(row=row, column=0, columnspan=2, sticky=tk.EW)
        widgets.append(self['structure'])
        row += 1
        self['hamiltonian'].grid(row=row, column=0, columnspan=2, sticky=tk.EW)
        widgets.append(self['hamiltonian'])
        row += 1
        self['convergence'].grid(row=row, column=0, columnspan=2, sticky=tk.EW)
        widgets.append(self['convergence'])
        row += 1
        sw.align_labels(widgets)

        if convergence == 'relative':
            self['relative'].grid(row=row, column=1, sticky=tk.W)
            row += 1
        elif convergence == 'absolute':
            self['absolute'].grid(row=row, column=1, sticky=tk.W)
            row += 1
        elif convergence not in ('normal', 'precise'):
            # variable ... so put in all possibilities
            self['relative'].grid(row=row, column=1, sticky=tk.W)
            row += 1
            self['absolute'].grid(row=row, column=1, sticky=tk.W)
            row += 1
            sw.align_labels((self['relative'], self['absolute']))

        frame.columnconfigure(0, minsize=30)

        return row

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

        # Shortcut for parameters
        P = self.node.parameters

        for key in P:
            if key not in ('results', 'extra keywords', 'create tables'):
                P[key].set_from_widget()

        # and from the results tab...
        if self.tk_var['create tables'].get():
            P['create tables'].value = 'yes'
        else:
            P['create tables'].value = 'no'

        results = P['results'].value = {}
        for key, w_check, w_variable, w_table, w_column \
                in self.results_widgets:

            if self.tk_var[key].get():
                tmp = results[key] = dict()
                tmp['variable'] = w_variable.get()
            table = w_table.get()
            if table != '':
                if key not in results:
                    tmp = results[key] = dict()
                tmp['table'] = table
                tmp['column'] = w_column.get()

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
        logger.debug('\tkeyword: {}'.format(keyword))
        logger.debug('\t  value: {}'.format(value))
        logger.debug('\t before: {}'.format(before))
        logger.debug('\t action: {}'.format(action))
        logger.debug('\tchanged: {}'.format(changed))

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

        w = self['keyword_' + str(row)]
        current = w.get().upper()

        keywords = []
        for keyword in mopac_step.keywords:
            if keyword.startswith(current):
                keywords.append(keyword)

        w.configure(values=sorted(keywords))

    def set_keyword_cb(self, event, w, row=None):
        logger.debug(event)
        logger.debug(w)
        logger.debug(w.get())
        logger.debug(row)

    def layout_keywords(self):
        """Layout the table of additional keywords and any arguments they
        need"""

        frame = self['add_to_input']

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
            w = ttk.Entry(
                frame,
                width=30,
                validate='key',
                validatecommand=(
                    self.keyword_cb, keyword, '%W', '%P', '%s', '%d', '%S'
                ),
                takefocus=False,
                style='Red.TEntry',
            )
            widgets['entry'] = w
            col = 0
            w.grid(row=row, column=col, stick=tk.EW)
            w.bind(
                '<KeyPress-Tab>',
                lambda event=None, row=row: self.handle_tab(event, row)
            )
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

                w = ttk.Entry(
                    frame,
                    width=15,
                    validate='key',
                    validatecommand=(
                        self.value_cb, keyword, '%W', '%P', '%s', '%d', '%S'
                    ),
                    takefocus=False,
                )
                widgets['value'] = w
                w.insert('end', keyword['value'])
                w.grid(row=row, column=col, sticky=tk.EW)

        # The button to add a row...
        row += 1
        w = self['add keyword'] = ttk.Button(
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
                command=self.handle_keyword_dialog
            )
            self.keyword_dialog.withdraw()
            frame = ttk.Frame(self.keyword_dialog.interior())
            frame.pack(expand=tk.YES, fill=tk.BOTH)
            self['keyword frame'] = frame

            w = self['keyword tree'] = ttk.Treeview(
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
                "Don't recognize dialog result '{}'".format(result)
            )

        self.keyword_dialog.deactivate(result)

        keyword = self['keyword tree'].selection()
        logger.debug(keyword)

    def validate_keyword_value(
        self, keyword, w_name, value, before, action, changed
    ):
        """Handle typing in a combobox for the keyword

        Arguments:
            keyword: the MOPAC keyword
            w_name: the widget name
            value: the value *after* the keystroke
            before: the value before the keystroke
            action: 0 for deletion, 1 for insertion
            changed: the text being inserted or deleted
        """

        # w = self.dialog.nametowidget(w_name)
        logger.debug('Validating the value of a keyword')
        logger.debug('\tkeyword: {}'.format(keyword))
        logger.debug('\t  value: {}'.format(value))
        logger.debug('\t before: {}'.format(before))
        logger.debug('\t action: {}'.format(action))
        logger.debug('\tchanged: {}'.format(changed))

        return True

    def remove_keyword(self, row=None):
        """Remove a keyword from dd to input"""
        logger.debug('remove row {}'.format(row))

    def handle_tab(self, event=None, row=None):
        """Handle a tab in a keyword entry field"""
        logger.debug('Caught tab in row {}'.format(row))
        logger.debug(event)

        data = self.tmp_keywords[row]
        w = data['widgets']['entry']
        current = w.get()

        defs = mopac_step.keywords
        keywords = []
        for keyword in defs:
            if keyword.startswith(current):
                keywords.append(keyword)

        prefix = lcp(*keywords)
        logger.debug('prefix = "{}", current = "{}"'.format(prefix, current))

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
