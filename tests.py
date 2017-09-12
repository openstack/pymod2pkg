#!/usr/bin/env python
#
# Copyright 2015 SUSE Linux GmbH
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

# py26 compat
try:
    import unittest2 as unittest
except ImportError:
    import unittest

import pymod2pkg


class Pymod2PkgTests(unittest.TestCase):
    def test_get_default_translation_func(self):
        self.assertEqual(pymod2pkg.get_default_tr_func('suse'),
                         pymod2pkg.default_suse_tr)
        self.assertEqual(pymod2pkg.get_default_tr_func('ubuntu'),
                         pymod2pkg.default_ubuntu_tr)
        self.assertEqual(pymod2pkg.get_default_tr_func('anything'),
                         pymod2pkg.default_rdo_tr)

    def test_default_translation_suse(self):
        self.assertEqual(pymod2pkg.module2package('oslo.db', 'suse'),
                         'python2-oslo.db')
        self.assertEqual(pymod2pkg.module2package('Babel', 'suse'),
                         'python2-Babel')

    def test_translation_suse(self):
        self.assertEqual(pymod2pkg.module2package('nova', 'suse'),
                         'openstack-nova')
        self.assertEqual(pymod2pkg.module2package('aodhclient',
                                                  'suse'),
                         'python2-aodhclient')
        self.assertEqual(pymod2pkg.module2package('gnocciclient',
                                                  'suse'),
                         'python2-gnocciclient')
        self.assertEqual(pymod2pkg.module2package('python-cinderclient',
                                                  'suse'),
                         'python2-cinderclient')
        self.assertEqual(pymod2pkg.module2package('python-neutronclient',
                                                  'suse'),
                         'python2-neutronclient')
        self.assertEqual(pymod2pkg.module2package('Tempest', 'suse'),
                         'openstack-tempest')

    def test_translation_ubuntu(self):
        self.assertEqual(pymod2pkg.module2package('nova', 'ubuntu'),
                         'python-nova')
        self.assertEqual(pymod2pkg.module2package('python-cinderclient',
                                                  'ubuntu'),
                         'python-cinderclient')
        self.assertEqual(pymod2pkg.module2package('python-neutronclient',
                                                  'ubuntu'),
                         'python-neutronclient')

    def test_default_translation_rdo(self):
        self.assertEqual(pymod2pkg.module2package('oslo.db', 'fedora'),
                         'python-oslo-db')
        self.assertEqual(pymod2pkg.module2package('Babel', 'fedora'),
                         'python-babel')
        self.assertEqual(pymod2pkg.module2package('nova', 'fedora'),
                         'openstack-nova')

    def test_default_translation_upstream(self):
        self.assertEqual(pymod2pkg.module2upstream('oslo.db'), 'oslo.db')
        self.assertEqual(pymod2pkg.module2upstream('python-glanceclient'),
                         'python-glanceclient')
        self.assertEqual(pymod2pkg.module2upstream('openstacksdk'),
                         'python-openstacksdk')
        self.assertNotEqual(pymod2pkg.module2upstream('keystoneauth1'),
                            'keystoneauth1')

    def test_translation_horizon_plugins(self):
        self.assertEqual(pymod2pkg.module2package('sahara-dashboard',
                                                  'fedora'),
                         'openstack-sahara-ui')
        self.assertEqual(pymod2pkg.module2package('magnum-ui', 'fedora'),
                         'openstack-magnum-ui')
        self.assertEqual(pymod2pkg.module2package('zomg-dashboard', 'fedora'),
                         'openstack-zomg-ui')

    def test_translation_tempest_plugins(self):
        self.assertEqual(pymod2pkg.module2package('keystone-tempest-plugin',
                                                  'fedora'),
                         'python-keystone-tests-tempest')
        self.assertEqual(pymod2pkg.module2package('zomg-tempest-plugin',
                         'fedora'), 'python-zomg-tests-tempest')

    def test_default_translation_py2py3_suse(self):
        self.assertEqual(pymod2pkg.module2package('oslo.db', 'suse',
                         py_vers=['py2', 'py3']),
                         ['python2-oslo.db', 'python3-oslo.db'])
        self.assertEqual(pymod2pkg.module2package('Babel', 'suse',
                         py_vers=['py2', 'py3']),
                         ['python2-Babel', 'python3-Babel'])

    def test_translation_py2py3_suse(self):
        self.assertEqual(pymod2pkg.module2package('nova', 'suse',
                         py_vers=['py2', 'py3']),
                         ['openstack-nova', ''])
        self.assertEqual(pymod2pkg.module2package('aodhclient',
                         'suse', py_vers=['py2', 'py3']),
                         ['python2-aodhclient', 'python3-aodhclient'])
        self.assertEqual(pymod2pkg.module2package('gnocciclient',
                         'suse', py_vers=['py2', 'py3']),
                         ['python2-gnocciclient', 'python3-gnocciclient'])
        self.assertEqual(pymod2pkg.module2package(
                         'python-cinderclient', 'suse',
                         py_vers=['py2', 'py3']),
                         ['python2-cinderclient', 'python3-cinderclient'])
        self.assertEqual(pymod2pkg.module2package(
                         'python-neutronclient', 'suse',
                         py_vers=['py2', 'py3']),
                         ['python2-neutronclient', 'python3-neutronclient'])
        self.assertEqual(pymod2pkg.module2package('Tempest', 'suse',
                         py_vers=['py2', 'py3']),
                         ['openstack-tempest', ''])

    def test_translation_py2py3_ubuntu(self):
        self.assertEqual(pymod2pkg.module2package('nova', 'ubuntu',
                         py_vers=['py2', 'py3']),
                         ['python-nova', 'python3-nova'])
        self.assertEqual(pymod2pkg.module2package('python-cinderclient',
                         'ubuntu', py_vers=['py2', 'py3']),
                         ['python-cinderclient', 'python3-cinderclient'])
        self.assertEqual(pymod2pkg.module2package(
                         'python-neutronclient', 'ubuntu',
                         py_vers=['py2', 'py3']),
                         ['python-neutronclient', 'python3-neutronclient'])

    def test_default_translation_py2py3_rdo(self):
        self.assertEqual(pymod2pkg.module2package('oslo.db', 'fedora',
                         py_vers=['py2', 'py3']),
                         ['python-oslo-db', 'python3-oslo-db'])
        self.assertEqual(pymod2pkg.module2package('Babel', 'fedora',
                         py_vers=['py2', 'py3']),
                         ['python-babel', 'python3-babel'])
        self.assertEqual(pymod2pkg.module2package('nova', 'fedora',
                         py_vers=['py2', 'py3']),
                         ['openstack-nova', ''])


class RegexRuleTests(unittest.TestCase):
    def test_regex_rule(self):

        def dummy_tr(mod):
            mod = mod.replace('dashboard', 'ui')
            return "openstack-{}".format(mod), ''

        rule = pymod2pkg.RegexRule(r'\w+-(dashboard|ui)', dummy_tr)
        self.assertEqual(rule('dummy-dashboard', 'rdo'),
                         ('openstack-dummy-ui', ''))
        self.assertEqual(rule('dummy-ui', 'rdo'), ('openstack-dummy-ui', ''))


if __name__ == '__main__':
    unittest.main()
