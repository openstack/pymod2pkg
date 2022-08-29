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
import packaging.requirements
import pymod2pkg
import sys


def get_default_prefix(dist):
    d_lower = dist.lower()
    if 'ubuntu' in d_lower:
        return "Depends"
    return "Requires"


def main():
    """Process python requirements files into a list of distribution
       packages"""
    parser = argparse.ArgumentParser(
        description='Process python requirements files into a list of '
                    'distribution packages'
    )
    parser.add_argument(
        '--dist', help='distribution style (default: %(default)s)',
        default=distro.LinuxDistribution().id().partition(' ')[0])
    parser.add_argument('--pyver', help='Python versions to return. "py" is '
                        'the unversioned name',
                        action='append', choices=['py', 'py2', 'py3'],
                        default=[])
    parser.add_argument('-r', '--requirements', action="append",
                        dest='requirements', required=True, default=[],
                        help="python requirements file to parse")
    parser.add_argument('-v', '--verbose', dest='verbose', action='count',
                        default=1, help='Invrease verbosity of the program')
    parser.add_argument('-b', '--brief', dest='verbose', action='store_const',
                        const=0, help='Only generate packagenames')
    parser.add_argument('--prefix', dest='prefix', nargs='?', const=None,
                        help="Prefix the output with a string provided by "
                        "the user or one determined by the --dist value")

    args = vars(parser.parse_args())

    pyversions = args['pyver'] if args['pyver'] else ['py']
    if len(pyversions) > 1:
        print("Please select only one version of python", file=sys.stderr)
        return 1
    args['prefix'] = get_default_prefix(args['dist'])

    for reqs_file in args['requirements']:
        if args['verbose']:
            print(f'Processing: {reqs_file}')
        try:
            with open(reqs_file) as f:
                reqs_txt = [line.strip() for line in f.readlines()]
        except FileNotFoundError as ex:
            print(ex)

        reqs = []
        for line in reqs_txt:
            if line.startswith('#') or line == '':
                continue
            # TODO(tonyb): Do we need to extend this so that it does the
            # right thing when given muliple versions of python for example:
            # requirements,txt":
            # liba>2;python_version>=3
            # altlib;python_version<3
            # We should honor this based on pyversions
            req = packaging.requirements.Requirement(line.split('#')[0])
            pkg = pymod2pkg.module2package(req.name, args['dist'],
                                           py_vers=pyversions)
            # We can potentially extend this to include versions
            # specifications.  The exact output will clearly be
            # distribution specific
            reqs.append(pkg)

        # This is slightly complex but it handles the following scenarios:
        # $ reqs2pkg -r test-requirements.txt --dist ubuntu -b
        # python-stestr
        # python-testresources
        # python-testtools
        # $ reqs2pkg -r test-requirements.txt --dist ubuntu
        # Processing: test-requirements.txt
        # Depends: python-stestr, python-testresources, python-testtools
        # $ reqs2pkg -r test-requirements.txt --dist rhel -b
        # python-stestr
        # python-testresources
        # python-testtools
        # $ reqs2pkg -r test-requirements.txt --dist rhel
        # Processing: test-requirements.txt
        # Requires: python-stestr
        # Requires: python-testresources
        # Requires: python-testtools
        prefix = ''
        if args['verbose']:
            prefix = f"{args['prefix']}: "
        if args['dist'].lower() in 'ubuntu':
            delim = ", "
        else:
            delim = f"\n{prefix}"

        if args['verbose']:
            print(prefix + delim.join(reqs))
        else:
            print("\n".join(reqs))
