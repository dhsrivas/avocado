# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
#
# See LICENSE for more details.
#
# Copyright: Red Hat Inc. 2015
# Author: Cleber Rosa <cleber@redhat.com>
"""
Plugins information plugin
"""

from .base import CLICmd
from avocado.core import output
from avocado.core import dispatcher
from avocado.utils import astring


class Plugins(CLICmd):

    """
    Plugins information
    """

    name = 'plugins'
    description = 'Displays plugin information'

    def configure(self, parser):
        parser = super(Plugins, self).configure(parser)
        parser.add_argument('--paginator',
                            choices=('on', 'off'), default='on',
                            help='Turn the paginator on/off. '
                            'Current: %(default)s')

    def run(self, args):
        view = output.View(app_args=args,
                           use_paginator=args.paginator == 'on')

        cli_cmds = dispatcher.CLICmdDispatcher()
        msg = 'Plugins that add new commands (avocado.plugins.cli.cmd):'
        view.notify(event='message', msg=msg)
        plugin_matrix = []
        for plugin in sorted(cli_cmds):
            plugin_matrix.append((plugin.name, plugin.obj.description))

        for line in astring.iter_tabular_output(plugin_matrix):
            view.notify(event='minor', msg=line)

        msg = 'Plugins that add new options to commands (avocado.plugins.cli):'
        cli = dispatcher.CLIDispatcher()
        view.notify(event='message', msg=msg)
        plugin_matrix = []
        for plugin in sorted(cli):
            plugin_matrix.append((plugin.name, plugin.obj.description))

        for line in astring.iter_tabular_output(plugin_matrix):
            view.notify(event='minor', msg=line)