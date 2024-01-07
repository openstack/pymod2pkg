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

import re


class TranslationRule(object):
    pass


class SingleRule(TranslationRule):
    """
    Translate a given module name

    mod: the python module name (usually the pypi name)
    pkg: the unversioned translated package name
    py2pkg: the python2 versioned translated package name
    py3pkg: the python3 versioned translated package name
    """
    def __init__(self, mod, pkg, py2pkg=None, py3pkg=None, distmap=None):
        self.mod = mod
        self.pkg = pkg
        self.py2pkg = py2pkg if py2pkg else pkg
        self.py3pkg = py3pkg if py3pkg else pkg
        self.distmap = distmap

    def __call__(self, mod, dist):
        if mod != self.mod:
            return None
        if self.distmap and dist:
            for distrex in self.distmap:
                if re.match(distrex, dist):
                    return self.distmap[distrex]
        return (self.pkg, self.py2pkg, self.py3pkg)


class MultiRule(TranslationRule):
    def __init__(self, mods, pkgfun):
        self.mods = mods
        self.pkgfun = pkgfun

    def __call__(self, mod, dist):
        if mod in self.mods:
            pkg, py2pkg, py3pkg = self.pkgfun(mod)
            return (pkg, py2pkg, py3pkg)
        return None


class RegexRule(TranslationRule):
    def __init__(self, pattern, pkgfun):
        self.pattern = pattern
        self.pkgfun = pkgfun

    def __call__(self, mod, dist):
        if re.match(self.pattern, mod):
            pkg, py2pkg, py3pkg = self.pkgfun(mod)
            return (pkg, py2pkg, py3pkg)
        return None


def default_rdo_tr(mod):
    """
    Default translation function for Fedora/RDO based systems
    """
    pkg = mod.rsplit('-python')[0]
    pkg = pkg.replace('_', '-').replace('.', '-').lower()
    if not pkg.startswith('python-'):
        pkg = 'python-' + pkg
    py2pkg = pkg
    py3pkg = re.sub('python', 'python3', pkg)
    return (pkg, py2pkg, py3pkg)


def default_ubuntu_tr(mod):
    """
    Default translation function for Ubuntu based systems
    """
    pkg = 'python-%s' % mod.lower()
    py2pkg = pkg
    py3pkg = 'python3-%s' % mod.lower()
    return (pkg, py2pkg, py3pkg)


def default_suse_tr(mod):
    """
    Default translation function for openSUSE, SLES, and other
    SUSE based systems

    Returns a tuple of 3 elements - the unversioned name, the python2 versioned
    name and the python3 versioned name.
    """
    pkg = 'python-%s' % mod
    py2pkg = 'python2-%s' % mod
    py3pkg = 'python3-%s' % mod
    return (pkg, py2pkg, py3pkg)


def default_suse_py39_tr(mod):
    """
    Default translation function for openSUSE, SLES, and other
    SUSE based systems that have python 3.9

    Returns a tuple of 3 elements - the unversioned name, the python2 versioned
    name and the python3 versioned name.
    """
    pkg = 'python-%s' % mod
    py2pkg = 'python2-%s' % mod
    py3pkg = 'python39-%s' % mod
    return (pkg, py2pkg, py3pkg)


def default_suse_py311_tr(mod):
    """
    Default translation function for openSUSE, SLES, and other
    SUSE based systems that have python 3.11

    Returns a tuple of 3 elements - the unversioned name, the python2 versioned
    name and the python3 versioned name.
    """
    pkg = 'python-%s' % mod
    py2pkg = 'python2-%s' % mod
    py3pkg = 'python311-%s' % mod
    return (pkg, py2pkg, py3pkg)


def openstack_prefix_tr(mod):
    pkg = 'openstack-' + mod.lower()
    return (pkg, pkg, pkg)


def rdo_horizon_plugins_tr(mod):
    mod = mod.replace('dashboard', 'ui')
    pkg = 'openstack-' + mod
    return (pkg, pkg, pkg)


def suse_horizon_plugins_tr(mod):
    mod = mod.replace('dashboard', 'ui')
    pkg = 'openstack-horizon-plugin-' + mod
    return (pkg, pkg, pkg)


def rdo_xstatic_tr(mod):
    mod = mod.replace('_', '-').replace('.', '-')
    pkg = 'python-' + mod
    py3pkg = 'python3-' + mod
    return (pkg, pkg, py3pkg)


def same_name_python_subst_python3(mod):
    py3pkg = re.sub('python', 'python3', mod)
    return (mod, mod, py3pkg)


def subst_python2_python3(mod):
    pkg = mod
    py2pkg = re.sub('python', 'python2', mod)
    py3pkg = re.sub('python', 'python3', mod)
    return (pkg, py2pkg, py3pkg)


def rdo_tempest_plugins_tr(mod):
    mod = mod.replace('tempest-plugin', 'tests-tempest')
    pkg = 'python-' + mod
    py2pkg = pkg
    py3pkg = 'python3-' + mod
    return (pkg, py2pkg, py3pkg)


# keep lists in alphabetic order
SERVICES_MAP = [
    'Tempest', 'aodh', 'barbican', 'ceilometer', 'cinder',
    'cloudkitty', 'cyborg', 'designate', 'ec2-api', 'freezer', 'freezer-api',
    'freezer-dr', 'glance', 'heat', 'heat-templates', 'ironic',
    'ironic-discoverd', 'ironic-inspector', 'ironic-python-agent',
    'keystone', 'magnum', 'manila', 'masakari', 'masakari-monitors',
    'mistral', 'monasca-agent', 'monasca-api', 'monasca-ceilometer',
    'monasca-log-api', 'monasca-notification', 'monasca-persister',
    'monasca-transform', 'murano', 'neutron', 'neutron-fwaas',
    'neutron-lbaas', 'neutron-vpnaas', 'nova', 'octavia', 'placement',
    'rally', 'sahara', 'swift', 'tempest', 'tripleo-common', 'trove', 'tuskar',
    'vitrage', 'watcher', 'zaqar', 'zun']


RDO_PKG_MAP = [
    # This demonstrates per-dist filter
    # SingleRule('sphinx', 'python-sphinx',
    #           distmap={'epel-6': 'python-sphinx10'}),
    SingleRule('ansible', 'ansible'),
    SingleRule('ansible-runner', 'python-ansible-runner',
               py3pkg='python3-ansible-runner'),
    SingleRule('APScheduler', 'python-APScheduler',
               py3pkg='python3-APScheduler'),
    SingleRule('Babel', 'python-babel', py3pkg='python3-babel'),
    SingleRule('bandit', 'bandit'),
    SingleRule('distribute', 'python-setuptools', py3pkg='python3-setuptools'),
    SingleRule('dnspython', 'python-dns', py3pkg='python3-dns'),
    SingleRule('google-api-python-client', 'python-google-api-client',
               py3pkg='python3-google-api-client'),
    SingleRule('GitPython', 'GitPython', py3pkg='python3-GitPython'),
    SingleRule('heat-agents', 'openstack-heat-agents',
               py3pkg='openstack-heat-agents'),
    SingleRule('IPy', 'python-IPy', py3pkg='python-IPy-python3'),
    SingleRule('pycrypto', 'python-crypto', py3pkg='python3-crypto'),
    SingleRule('pyzmq', 'python-zmq', py3pkg='python3-zmq'),
    SingleRule('mysql-python', 'MySQL-python', py3pkg='python3-mysql'),
    SingleRule('PyMySQL', 'python-PyMySQL', py3pkg='python3-PyMySQL'),
    SingleRule('PyJWT', 'python-jwt', py3pkg='python3-jwt'),
    SingleRule('MySQL-python', 'MySQL-python', py3pkg='python3-mysql'),
    SingleRule('PasteDeploy', 'python-paste-deploy',
               py3pkg='python3-paste-deploy'),
    SingleRule('sqlalchemy-migrate', 'python-migrate',
               py3pkg='python3-migrate'),
    SingleRule('qpid-python', 'python-qpid'),
    SingleRule('nosexcover', 'python-nose-xcover',
               py3pkg='python3-nose-xcover'),
    SingleRule('posix_ipc', 'python-posix_ipc', py3pkg='python3-posix_ipc'),
    SingleRule('prometheus-client', 'python-prometheus_client',
               py3pkg='python3-prometheus_client'),
    SingleRule('sysv_ipc', 'python-sysv_ipc', py3pkg='python3-sysv_ipc'),
    SingleRule('oslosphinx', 'python-oslo-sphinx',
               py3pkg='python3-oslo-sphinx'),
    SingleRule('ovs', 'python-openvswitch', py3pkg='python3-openvswitch'),
    SingleRule('psycopg2-binary', 'python-psycopg2',
               py3pkg='python3-psycopg2'),
    SingleRule('pyinotify', 'python-inotify', py3pkg='python3-inotify'),
    SingleRule('pyScss', 'python-scss', py3pkg='python3-scss'),
    SingleRule('tripleo-incubator', 'openstack-tripleo'),
    SingleRule('pika-pool', 'python-pika_pool', py3pkg='python3-pika_pool'),
    SingleRule('suds-community', 'python-suds', py3pkg='python3-suds'),
    SingleRule('suds-jurko', 'python-suds', py3pkg='python3-suds'),
    SingleRule('supervisor', 'supervisor', py3pkg='python3-supervisor'),
    SingleRule('wsgi_intercept', 'python-wsgi_intercept',
               py3pkg='python3-wsgi_intercept'),
    SingleRule('Sphinx', 'python-sphinx', py3pkg='python3-sphinx'),
    SingleRule('sphinx_rtd_theme', 'python-sphinx_rtd_theme',
               py3pkg='python3-sphinx_rtd_theme'),
    SingleRule('xattr', 'pyxattr', py3pkg='python3-pyxattr'),
    SingleRule('XStatic-term.js', 'python-XStatic-termjs',
               py3pkg='python3-XStatic-termjs'),
    SingleRule('heat-cfntools', 'heat-cfntools'),
    SingleRule('horizon', 'openstack-dashboard'),
    SingleRule('openstack-placement', 'openstack-placement'),
    SingleRule('networking-vsphere', 'openstack-neutron-vsphere'),
    SingleRule('networking-l2gw', 'openstack-neutron-l2gw'),
    SingleRule('neutron-dynamic-routing', 'openstack-neutron-dynamic-routing'),
    SingleRule('m2crypto', 'm2crypto'),
    SingleRule('libvirt-python', 'python-libvirt', py3pkg='python3-libvirt'),
    SingleRule('tempest-horizon', 'python-horizon-tests-tempest'),
    SingleRule('rtslib-fb', 'python-rtslib', py3pkg='python3-rtslib'),
    SingleRule('PyYAML', 'python-pyyaml', py3pkg='python3-pyyaml'),
    SingleRule('pyOpenSSL', 'python-pyOpenSSL', py3pkg='python3-pyOpenSSL'),
    SingleRule('semantic_version', 'python-semantic_version',
               py3pkg='python3-semantic_version'),
    SingleRule('semantic-version', 'python-semantic_version',
               py3pkg='python3-semantic_version'),
    SingleRule('sphinxcontrib-svg2pdfconverter',
               'python-sphinxcontrib-rsvgconverter',
               py3pkg='python3-sphinxcontrib-rsvgconverter'),
    SingleRule('systemd-python', 'python-systemd', py3pkg='python3-systemd'),
    # simple direct mapping no name change
    MultiRule(
        mods=['dib-utils', 'diskimage-builder'],
        pkgfun=lambda mod: ((mod, mod, mod))),
    # simple direct mapping no name change - except for python3
    MultiRule(
        mods=['numpy', 'pyflakes', 'pylint',
              'graphviz',
              'instack-undercloud',
              'os-apply-config',
              'os-collect-config',
              'os-net-config',
              'os-refresh-config',
              'pexpect',
              'watchdog',
              'pystache', 'pysendfile'],
        pkgfun=lambda mod: ((mod, mod, 'python3-' + mod))),
    # OpenStack services
    MultiRule(mods=SERVICES_MAP, pkgfun=openstack_prefix_tr),
    # XStatic projects (name is python-pypi_name, no lowercase conversion)
    RegexRule(pattern=r'^XStatic.*', pkgfun=rdo_xstatic_tr),
    # Horizon plugins (normalized to openstack-<project>-ui)
    RegexRule(pattern=r'^(neutron-)?\w+-(dashboard|ui)',
              pkgfun=rdo_horizon_plugins_tr),
    # Tempest plugins (normalized to python-<project>-tests-tempest)
    RegexRule(pattern=r'\w+-tempest-plugin', pkgfun=rdo_tempest_plugins_tr)
]


SUSE_COMMON_PKG_MAP = [
    # not following SUSE naming policy
    SingleRule('ansible', 'ansible'),
    SingleRule('ansible-runner', 'ansible-runner'),
    SingleRule('python-ldap', 'python-ldap'),
    # OpenStack services
    MultiRule(mods=SERVICES_MAP, pkgfun=openstack_prefix_tr),
    # OpenStack clients
    MultiRule(
        mods=['python-%sclient' % c for c in (
            'barbican', 'ceilometer', 'cinder', 'cloudkitty',
            'congress', 'cue', 'cyborg', 'designate', 'distil', 'drac', 'fuel',
            'freezer', 'heat', 'glance', 'glare', 'ironic',
            'ironic-inspector-', 'k8s', 'keystone',
            'magnum', 'manila', 'masakari', 'mistral', 'monasca',
            'murano', 'nimble', 'neutron', 'nova', 'octavia', 'oneview',
            'openstack', 'sahara', 'scci', 'senlin',
            'smaug', 'solum', 'swift', 'tacker', 'tripleo', 'trove',
            'vitrage', 'watcher', 'zaqar', 'zun')],
        pkgfun=subst_python2_python3),
    SingleRule('devel', 'python-devel', py3pkg='python3-devel'),
    SingleRule('openstack-placement', 'openstack-placement'),
    # ui components
    SingleRule('designate-dashboard', 'openstack-horizon-plugin-designate-ui'),
    SingleRule('freezer-web-ui', 'openstack-horizon-plugin-freezer-ui'),
    SingleRule('group-based-policy-ui', 'openstack-horizon-plugin-gbp-ui'),
    SingleRule('heat-agents', 'openstack-heat-agents',
               py3pkg='openstack-heat-agents'),
    SingleRule('horizon', 'openstack-dashboard'),
    SingleRule('ironic-ui', 'openstack-horizon-plugin-ironic-ui'),
    SingleRule('magnum-ui', 'openstack-horizon-plugin-magnum-ui'),
    SingleRule('manila-ui', 'openstack-horizon-plugin-manila-ui'),
    SingleRule('monasca-ui', 'openstack-horizon-plugin-monasca-ui'),
    SingleRule('murano-dashboard', 'openstack-horizon-plugin-murano-ui'),
    SingleRule('networking-vsphere', 'openstack-neutron-vsphere'),
    SingleRule('networking-l2gw', 'openstack-neutron-l2gw'),
    SingleRule('neutron-dynamic-routing', 'openstack-neutron-dynamic-routing'),
    RegexRule(pattern=r'^(neutron-)?\w+-(dashboard|ui)',
              pkgfun=suse_horizon_plugins_tr),
]

SUSE_PKG_MAP = SUSE_COMMON_PKG_MAP

SUSE_PY39_PKG_MAP = SUSE_COMMON_PKG_MAP
SUSE_PY39_PKG_MAP.extend([
    SingleRule('devel', 'python-devel', 'python39-devel'),
])

SUSE_PY311_PKG_MAP = SUSE_COMMON_PKG_MAP
SUSE_PY311_PKG_MAP.extend([
    SingleRule('devel', 'python-devel', 'python311-devel'),
])

UBUNTU_PKG_MAP = [
    SingleRule('glance_store', 'python-glance-store'),
    SingleRule('GitPython', 'python-git'),
    SingleRule('libvirt-python', 'python-libvirt'),
    SingleRule('PyMySQL', 'python-mysql'),
    SingleRule('pyOpenSSL', 'python-openssl'),
    SingleRule('PyYAML', 'python-yaml'),
    SingleRule('sqlalchemy-migrate', 'python-migrate'),
    SingleRule('suds-jurko', 'python-suds'),

    # Openstack clients
    MultiRule(
        mods=['python-%sclient' % c for c in (
            'barbican', 'ceilometer', 'cinder', 'cloudkitty', 'congress',
            'designate', 'fuel', 'heat', 'glance', 'ironic',
            'keystone',
            'magnum', 'manila', 'masakari', 'mistral', 'monasca',
            'murano', 'neutron', 'nova', 'octavia',
            'openstack', 'sahara',
            'senlin', 'swift',
            'trove',  'zaqar', 'zun')],
        pkgfun=same_name_python_subst_python3),

]

OPENSTACK_UPSTREAM_PKG_MAP = [
    SingleRule('openstack-placement', 'placement'),
    SingleRule('gnocchiclient', 'python-gnocchiclient'),
    SingleRule('aodhclient', 'python-aodhclient'),
    SingleRule('keystoneauth1', 'keystoneauth'),
    SingleRule('microversion_parse', 'microversion-parse'),
    SingleRule('XStatic-smart-table', 'xstatic-angular-smart-table'),
]


def get_pkg_map(dist):
    d_lower = dist.lower()
    if 'suse_py39' in d_lower:
        return SUSE_PY39_PKG_MAP
    if 'suse_py311' in d_lower:
        return SUSE_PY311_PKG_MAP
    if 'suse' in d_lower or 'sles' in d_lower:
        return SUSE_PKG_MAP
    if 'ubuntu' in d_lower:
        return UBUNTU_PKG_MAP
    return RDO_PKG_MAP


def get_default_tr_func(dist):
    d_lower = dist.lower()
    if 'suse_py39' in d_lower:
        return default_suse_py39_tr
    if 'suse_py311' in d_lower:
        return default_suse_py311_tr
    if 'suse' in d_lower or 'sles' in d_lower:
        return default_suse_tr
    if 'ubuntu' in d_lower:
        return default_ubuntu_tr
    return default_rdo_tr


def module2package(mod, dist, pkg_map=None, py_vers=('py',)):
    """Return a corresponding package name for a python module.

    mod: python module name
    dist: a linux distribution as returned by
          `distro.LinuxDistribution().id().partition(' ')[0]`
    pkg_map: a custom package mapping. None means autodetected based on the
             given dist parameter
    py_vers: a list of python versions the function should return. Default is
             'py' which is the unversioned translation. Possible values are
             'py', 'py2' and 'py3'
    """
    if not pkg_map:
        pkg_map = get_pkg_map(dist)
    for rule in pkg_map:
        pkglist = rule(mod, dist)
        if pkglist:
            break
    else:
        tr_func = get_default_tr_func(dist)
        pkglist = tr_func(mod)

    output = []
    for v in py_vers:
        if v == 'py':
            output.append(pkglist[0])
        elif v == 'py2':
            output.append(pkglist[1])
        elif v == 'py3':
            output.append(pkglist[2])
        else:
            raise Exception('Invalid version "%s"' % (v))

    if len(output) == 1:
        # just return a single value (backwards compatible)
        return output[0]
    else:
        return output


def module2upstream(mod):
    """Return a corresponding OpenStack upstream name for a python module.

    mod  -- python module name
    """
    for rule in OPENSTACK_UPSTREAM_PKG_MAP:
        pkglist = rule(mod, dist=None)
        if pkglist:
            return pkglist[0]
    return mod
