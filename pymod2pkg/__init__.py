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


class RegexRule(TranslationRule):
    def __init__(self, pattern, pkgfun):
        self.pattern = pattern
        self.pkgfun = pkgfun

    def __call__(self, mod, dist):
        if re.match(self.pattern, mod):
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
    return 'openstack-' + mod.lower()


def rdo_horizon_plugins_tr(mod):
    mod = mod.replace('dashboard', 'ui')
    return 'openstack-' + mod


RDO_PKG_MAP = [
    # This demonstrates per-dist filter
    # SingleRule('sphinx', 'python-sphinx',
    #           distmap={'epel-6': 'python-sphinx10'}),
    SingleRule('Babel', 'python-babel'),
    SingleRule('distribute', 'python-setuptools'),
    SingleRule('google-api-python-client', 'python-google-api-client'),
    SingleRule('pyOpenSSL', 'pyOpenSSL'),
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
    SingleRule('tripleo-incubator', 'openstack-tripleo'),
    SingleRule('pika-pool', 'python-pika_pool'),
    SingleRule('suds-jurko', 'python-suds'),
    SingleRule('wsgi_intercept', 'python-wsgi_intercept'),
    SingleRule('mistral', 'openstack-mistral-all'),
    MultiRule(
        mods=['PyYAML', 'm2crypto', 'numpy', 'pyflakes', 'pylint', 'pyparsing',
              'pytz', 'pysendfile', 'libvirt-python'],
        pkgfun=lambda x: x),
    # OpenStack services
    MultiRule(
        # keep lists in alphabetic order
        mods=['aodh', 'barbican', 'ceilometer', 'cinder', 'cloudkitty',
              'designate', 'ec2-api', 'glance', 'heat', 'heat-templates',
              'ironic', 'ironic-discoverd', 'ironic-inspector',
              'ironic-python-agent', 'keystone', 'magnum', 'manila',
              'murano', 'neutron', 'neutron-fwaas', 'neutron-lbaas',
              'neutron-vpnaas', 'nova', 'octavia', 'rally', 'sahara', 'swift',
              'Tempest', 'trove', 'tuskar', 'vitrage', 'zaqar'],
        pkgfun=openstack_prefix_tr),
    # Horizon plugins (normalized to openstack-<project>-ui)
    RegexRule(pattern=r'\w+-(dashboard|ui)', pkgfun=rdo_horizon_plugins_tr)
]


SUSE_PKG_MAP = [
    # OpenStack services
    MultiRule(
        # keep lists in alphabetic order
        mods=['ceilometer', 'cinder', 'designate', 'glance',
              'heat', 'ironic', 'keystone', 'manila',
              'neutron', 'nova', 'rally', 'sahara', 'swift',
              'Tempest', 'trove', 'tuskar', 'zaqar'],
        pkgfun=openstack_prefix_tr),
    # OpenStack clients
    MultiRule(
        mods=['python-%sclient' % c for c in (
            'k8s', 'barbican',
            'ceilometer', 'cinder', 'cloudkitty', 'congress', 'cue',
            'designate', 'distil', 'drac', 'fuel', 'freezer', 'heat',
            'glance', 'ironic', 'ironic-inspector-',
            'karbor', 'k8s', 'keystone',
            'magnum', 'manila', 'mistral', 'monasca',
            'murano', 'nimble', 'neutron', 'nova', 'oneview',
            'openstack', 'sahara', 'scci', 'searchlight',
            'senlin', 'smaug', 'solum', 'swift', 'tacker',
            'tripleo', 'trove', 'vitrage', 'watcher', 'zaqar')],
        pkgfun=lambda x: x),
]

OPENSTACK_UPSTREAM_PKG_MAP = [
    SingleRule('openstacksdk', 'python-openstacksdk'),
    SingleRule('gnocchiclient', 'python-gnocchiclient'),
    SingleRule('aodhclient', 'python-aodhclient'),
    SingleRule('keystoneauth1', 'keystoneauth'),
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


def module2upstream(mod):
    """Return a corresponding OpenStack upstream name  for a python module.

    mod  -- python module name
    """
    for rule in OPENSTACK_UPSTREAM_PKG_MAP:
        pkg = rule(mod, None)
        if pkg:
            return pkg
    return mod


def main():
    """for resolving names from command line"""
    parser = argparse.ArgumentParser(description='Python module name to'
                                     'package name')
    group = parser.add_mutually_exclusive_group()
    group.add_argument('--dist', help='distribution style '
                       '(default: %(default)s)',
                       default=platform.linux_distribution()[0])
    group.add_argument('--upstream', help='map to OpenStack project name',
                       action='store_true')
    parser.add_argument('modulename', help='python module name')
    args = vars(parser.parse_args())
    if args['upstream']:
        print(module2upstream(args['modulename']))
    else:
        print(module2package(args['modulename'], args['dist']))


# for debugging to call the file directly
if __name__ == "__main__":
    main()
