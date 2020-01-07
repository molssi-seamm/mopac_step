# -*- coding: utf-8 -*-

"""The graphical part of a MOPAC Energy node"""

import configargparse
import logging
import seamm
import seamm_widgets as sw
import mopac_step
import tkinter as tk

logger = logging.getLogger(__name__)


class TkEnergy(seamm.TkNode):

    def __init__(
        self,
        tk_flowchart=None,
        node=None,
        canvas=None,
        x=120,
        y=20,
        w=200,
        h=50,
        my_logger=logger,
        keyword_metadata=None
    ):
        """Initialize the graphical Tk MOPAC energy step

        Keyword arguments:
        """
        self.results_widgets = []

        # Argument/config parsing
        self.parser = configargparse.ArgParser(
            auto_env_var_prefix='',
            default_config_files=[
                '/etc/seamm/mopac_energy.ini',
                '/etc/seamm/seamm.ini',
                '~/.seamm/mopac_energy.ini',
                '~/.seamm/seamm.ini',
            ]
        )

        self.parser.add_argument(
            '--seamm-configfile',
            is_config_file=True,
            default=None,
            help='a configuration file to override others'
        )

        # Options for this plugin
        self.parser.add_argument(
            "--mopac-tk-energy-log-level",
            default=configargparse.SUPPRESS,
            choices=[
                'CRITICAL', 'ERROR', 'WARNING', 'INFO', 'DEBUG', 'NOTSET'
            ],
            type=lambda string: string.upper(),
            help="the logging level for the MOPAC Tk_energy step"
        )

        self.options, self.unknown = self.parser.parse_known_args()

        # Set the logging level for this module if requested
        if 'mopac_tk_energy_log_level' in self.options:
            my_logger.setLevel(self.options.mopac_tk_energy_log_level)
            my_logger.critical(
                'Set log level to {}'.format(
                    self.options.mopac_tk_energy_log_level
                )
            )

        # Call the constructor for the energy
        if keyword_metadata is None:
            keyword_metadata = mopac_step.keyword_metadata

        super().__init__(
            tk_flowchart=tk_flowchart,
            node=node,
            canvas=canvas,
            x=x,
            y=y,
            w=w,
            h=h,
            my_logger=my_logger,
            keyword_metadata=keyword_metadata
        )

    def right_click(self, event):
        """Probably need to add our dialog...
        """

        super().right_click(event)
        self.popup_menu.add_command(label="Edit..", command=self.edit)

        self.popup_menu.tk_popup(event.x_root, event.y_root, 0)

    def create_dialog(
        self,
        title='Edit MOPAC Energy Step',
        calculation='single point energy'
    ):
        """Create the dialog!"""
        self.logger.debug('Creating the dialog')
        frame = super().create_dialog(
            title=title, widget='notebook', results_tab=True
        )

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

        self.logger.debug('Finished creating the dialog')

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
