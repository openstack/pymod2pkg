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

from __future__ import print_function

import argparse
import platform
import re


class TranslationRule(object):
    pass


class SingleRule(TranslationRule):
    def __init__(self, mod, pkg, distmap=None):
        self.mod = mod
        self.pkg = pkg
        self.distmap = distmap

    def __call__(self, mod, dist):
        if mod != self.mod:
            return None
        if self.distmap and dist:
            for distrex in self.distmap:
                if re.match(distrex, dist):
                    return self.distmap[distrex]
        return self.pkg


class MultiRule(TranslationRule):
    def __init__(self, mods, pkgfun):
        self.mods = mods
        self.pkgfun = pkgfun

    def __call__(self, mod, dist):
        if mod in self.mods:
            return self.pkgfun(mod)
        return None


def default_rdo_tr(mod):
    pkg = mod.rsplit('-python')[0]
    pkg = pkg.replace('_', '-').replace('.', '-').lower()
    if not pkg.startswith('python-'):
        pkg = 'python-' + pkg
    return pkg


def default_suse_tr(mod):
    return 'python-' + mod


def openstack_prefix_tr(mod):
    return 'openstack-' + mod


RDO_PKG_MAP = [
    # This demonstrates per-dist filter
    # SingleRule('sphinx', 'python-sphinx',
    #           distmap={'epel-6': 'python-sphinx10'}),
    SingleRule('distribute', 'python-setuptools'),
    SingleRule('pyopenssl', 'pyOpenSSL'),
    SingleRule('IPy', 'python-IPy'),
    SingleRule('pycrypto', 'python-crypto'),
    SingleRule('pyzmq', 'python-zmq'),
    SingleRule('mysql-python', 'MySQL-python'),
    SingleRule('PyMySQL', 'python-PyMySQL'),
    SingleRule('MySQL-python', 'MySQL-python'),
    SingleRule('PasteDeploy', 'python-paste-deploy'),
    SingleRule('sqlalchemy-migrate', 'python-migrate'),
    SingleRule('qpid-python', 'python-qpid'),
    SingleRule('posix_ipc', 'python-posix_ipc'),
    SingleRule('oslosphinx', 'python-oslo-sphinx'),
    SingleRule('pyinotify', 'python-inotify'),
    MultiRule(
        mods=['PyYAML', 'm2crypto', 'numpy', 'pyflakes', 'pylint', 'pyparsing',
              'pytz', 'pysendfile', 'libvirt-python'],
        pkgfun=lambda x: x),
    MultiRule(
        mods=['nova', 'keystone', 'glance', 'swift', 'neutron'],
        pkgfun=openstack_prefix_tr),
]


SUSE_PKG_MAP = [
    # OpenStack services
    MultiRule(
        # keep lists in alphabetic order
        mods=['ceilometer', 'cinder', 'designate', 'glance',
              'heat', 'ironic', 'keystone', 'manila',
              'neutron', 'nova', 'rally', 'sahara', 'swift',
              'tempest', 'trove', 'tuskar', 'zaqar'],
        pkgfun=openstack_prefix_tr),
    # OpenStack clients
    MultiRule(
        mods=['python-ceilometerclient', 'python-cinderclient',
              'python-designateclient', 'python-glanceclient',
              'python-heatclient', 'python-ironicclient',
              'python-keystoneclient', 'python-manilaclient',
              'python-neutronclient', 'python-novaclient',
              'python-saharaclient', 'python-swiftclient',
              'python-troveclient', 'python-tuskarclient',
              'python-zaqarclient'],
        pkgfun=lambda x: x),
]


def get_pkg_map(dist):
    if dist.lower().find('suse') != -1:
        return SUSE_PKG_MAP
    return RDO_PKG_MAP


def get_default_tr_func(dist):
    if dist.lower().find('suse') != -1:
        return default_suse_tr
    return default_rdo_tr


def module2package(mod, dist, pkg_map=None):
    """Return a corresponding package name for a python module.

    mod  -- python module name
    dist -- a linux distribution as returned by
            `platform.linux_distribution()[0]`
    """
    if not pkg_map:
        pkg_map = get_pkg_map(dist)
    for rule in pkg_map:
        pkg = rule(mod, dist)
        if pkg:
            return pkg
    tr_func = get_default_tr_func(dist)
    return tr_func(mod)


def main():
    """for resolving names from command line"""
    parser = argparse.ArgumentParser(description='Python module name to'
                                     'package name')
    parser.add_argument('--dist', help='distribution style '
                        '(default: %(default)s)',
                        default=platform.linux_distribution()[0])
    parser.add_argument('modulename', help='python module name')
    args = vars(parser.parse_args())
    print(module2package(args['modulename'], args['dist']))


# for debugging to call the file directly
if __name__ == "__main__":
    main()
