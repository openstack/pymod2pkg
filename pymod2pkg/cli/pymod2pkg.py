#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

import argparse
import distro

import pymod2pkg


def main():
    """for resolving names from command line"""
    parser = argparse.ArgumentParser(description='Python module name to'
                                     'package name')
    group = parser.add_mutually_exclusive_group()
    group.add_argument(
        '--dist', help='distribution style (default: %(default)s)',
        default=distro.LinuxDistribution().id().partition(' ')[0])
    group.add_argument('--upstream', help='map to OpenStack project name',
                       action='store_true')
    parser.add_argument('--pyver', help='Python versions to return. "py" is '
                        'the unversioned name',
                        action='append', choices=['py', 'py2', 'py3'],
                        default=[])
    parser.add_argument('modulename', help='python module name')
    args = vars(parser.parse_args())

    pyversions = args['pyver'] if args['pyver'] else ['py']

    if args['upstream']:
        print(pymod2pkg.module2upstream(args['modulename']))
    else:
        pylist = pymod2pkg.module2package(args['modulename'], args['dist'],
                                          py_vers=pyversions)
        # When only 1 version is requested, it will be returned as a string,
        # for backwards compatibility. Else, it will be a list.
        if type(pylist) is list:
            print(' '.join(pylist))
        else:
            print(pylist)
