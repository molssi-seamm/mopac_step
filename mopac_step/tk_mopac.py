# -*- coding: utf-8 -*-

"""The graphical part of a MOPAC step in SEAMM"""

import configargparse
import logging
import seamm

logger = logging.getLogger(__name__)


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
        h=50,
        my_logger=logger
    ):
        """Initialize the graphical Tk node for MOPAC

        Keyword arguments:
        """
        self.namespace = namespace

        # Argument/config parsing
        self.parser = configargparse.ArgParser(
            auto_env_var_prefix='',
            default_config_files=[
                '/etc/seamm/mopac.ini',
                '/etc/seamm/seamm.ini',
                '~/.seamm/mopac.ini',
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
            "--tk-mopac-log-level",
            default=configargparse.SUPPRESS,
            choices=[
                'CRITICAL', 'ERROR', 'WARNING', 'INFO', 'DEBUG', 'NOTSET'
            ],
            type=lambda string: string.upper(),
            help="the logging level for the Tk_Mopac step"
        )

        self.options, self.unknown = self.parser.parse_known_args()

        # Set the logging level for this module if requested
        if 'tk_mopac_log_level' in self.options:
            logger.setLevel(self.options.tk_mopac_log_level)
            logger.critical(
                'Set log level to {}'.format(self.options.tk_mopac_log_level)
            )

        # Call the constructor for the energy
        super().__init__(
            tk_flowchart=tk_flowchart,
            node=node,
            canvas=canvas,
            x=x,
            y=y,
            w=w,
            h=h,
            my_logger=my_logger
        )

        self.create_dialog()

    def create_dialog(self):
        """Create the dialog!"""
        frame = super().create_dialog('Edit MOPAC Step')

        # make it large!
        sw = self.dialog.winfo_screenwidth()
        sh = self.dialog.winfo_screenheight()
        w = int(0.9 * sw)
        h = int(0.8 * sh)
        x = int(0.05 * sw / 2)
        y = int(0.1 * sh / 2)

        self.dialog.geometry('{}x{}+{}+{}'.format(w, h, x, y))

        self.tk_subflowchart = seamm.TkFlowchart(
            master=frame,
            namespace=self.namespace,
            flowchart=self.node.subflowchart
        )
        self.tk_subflowchart.draw()

    def right_click(self, event):
        """Probably need to add our dialog...
        """

        super().right_click(event)
        self.popup_menu.add_command(label="Edit..", command=self.edit)

        self.popup_menu.tk_popup(event.x_root, event.y_root, 0)

    def update_flowchart(self, tk_flowchart=None, flowchart=None):
        """Update the nongraphical flowchart. Only used in nodes that contain
        flowcharts"""

        super().update_flowchart(
            flowchart=self.node.subflowchart,
            tk_flowchart=self.tk_subflowchart
        )

    def from_flowchart(self, tk_flowchart=None, flowchart=None):
        """Recreate the graphics from the non-graphical flowchart.
        Only used in nodes that contain flowchart"""

        super().from_flowchart(
            flowchart=self.node.subflowchart,
            tk_flowchart=self.tk_subflowchart
        )
