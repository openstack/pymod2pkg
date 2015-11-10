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
        self.assertEqual(pymod2pkg.get_default_tr_func('anything'),
                         pymod2pkg.default_rdo_tr)

    def test_default_translation_suse(self):
        self.assertEqual(pymod2pkg.module2package('oslo.db', 'suse'),
                         'python-oslo.db')
        self.assertEqual(pymod2pkg.module2package('Babel', 'suse'),
                         'python-Babel')

    def test_translation_suse(self):
        self.assertEqual(pymod2pkg.module2package('nova', 'suse'),
                         'openstack-nova')
        self.assertEqual(pymod2pkg.module2package('python-neutronclient',
                                                  'suse'),
                         'python-neutronclient')

    def test_default_translation_rdo(self):
        self.assertEqual(pymod2pkg.module2package('oslo.db', 'fedora'),
                         'python-oslo-db')
        self.assertEqual(pymod2pkg.module2package('Babel', 'fedora'),
                         'python-babel')
        self.assertEqual(pymod2pkg.module2package('nova', 'fedora'),
                         'openstack-nova')


if __name__ == '__main__':
    unittest.main()
