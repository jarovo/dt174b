#!/bin/python
#
#    Python tool for interfacing the CEM DT-174B Weather Datalogger.
#    Copyright (C) 2013 Jaroslav Henner
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#

from abc import ABCMeta, abstractmethod
import argparse
from datetime import datetime
import logging
import logging.config
import os.path
import sys
import usb
import yaml

import dt174b


DESCRIPTION = (
    "Python tool for interfacing the CEM DT-174B Weather Datalogger."
)


class AbstractAction(object):
    __metaclass__ = ABCMeta
    name = None
    help = None

    def register(self, subparser):
        parser = subparser.add_parser(self.name,
                    formatter_class=argparse.ArgumentDefaultsHelpFormatter,
                    help=self.help)
        parser.set_defaults(func=self)
        self.add_options(parser)

    def add_options(self, parser):
        pass

    @abstractmethod
    def __call__(self, *args, **kwargs):
        pass


class SetAction(AbstractAction):
    name = 'set'
    help = 'Set and start the logging.'

    def add_options(self, parser):
        parser.add_argument(
            '--rec_int', type=int, default=10,
            help='REC LED blinking interval')
        parser.add_argument(
            '--alm_int', type=int, default=10,
            help='ALM LED bLinking interval')
        parser.add_argument(
            '--smpl_int', type=int, default=1,
            help='Sampling interval')
        parser.add_argument(
            '--auto', action='store_true',
            help='Whether to automaticaly start loging.')
        parser.add_argument(
            '--temp', type=float, nargs=2, metavar=('LOW', 'HIGH'),
            default=(5.5, 40.5),
            help='Temperature alarm thresholds.')
        parser.add_argument(
            '--humidity', type=float, nargs=2, metavar=('LOW', 'HIGH'),
            default=(30.5, 90.5),
            help='Humidity alarm thresholds.')
        parser.add_argument(
            '--pressure', type=float, nargs=2, metavar=('LOW', 'HIGH'),
            default=(700, 1100),
            help='Pressure alarm thresholds.')
        parser.add_argument(
            '--altitude', type=float, dest='alt', default=0,
            help='Altitude adjustment.')
        parser.add_argument(
            '--samples', type=int, default=10000,
            help='How many samples to take.')

    def __call__(self, args):
        settings = vars(args)
        settings['temp_low'], settings['temp_high'] = settings['temp']
        settings['hum_low'], settings['hum_high'] = settings['humidity']
        settings['pressure_low'], settings['pressure_high'] = settings['pressure']
        del settings['func']
        del settings['temp'], settings['humidity'], settings['pressure']
        now = datetime.now().timetuple()
        p = dt174b.SettingsPacket(*now[:6], **settings)
        logger = dt174b.DT174B()
        logger.reset()
        logger.send_settings(p)


class DownloadAction(AbstractAction):
    name = 'download'
    help = 'Download the log.'

    def __call__(self, args):
        logger = dt174b.DT174B()
        logger.reset()
        for line in logger.read_log():
            print line.encode('hex')


def module_relative_path(path):
    return os.path.join(os.path.dirname(__file__), path)


def setup_logging():
    with open(module_relative_path('logging.conf'), 'r') as logging_config:
        D = yaml.load(logging_config)
    D.setdefault('version', 1)
    logging.config.dictConfig(D)


def main():
    setup_logging()

    parser = argparse.ArgumentParser(description=DESCRIPTION,
                        formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    subparsers = parser.add_subparsers(help='sub-command help')
    for action in (SetAction(), DownloadAction()):
        action.register(subparsers)
    opts = parser.parse_args()
    try:
        opts.func(opts)
    except usb.core.USBError as err:
        if 'Access denied' in unicode(err):
            print >> sys.stderr
            print >> sys.stderr, err
            print >> sys.stderr, ('Perhaps you need to get added to the user '
                                 'group "datalogger", or you need root '
                                 'priviledges.')
            print >> sys.stderr
            sys.exit(err.args[0])
        else:
            raise


if __name__ == '__main__':
    main()

