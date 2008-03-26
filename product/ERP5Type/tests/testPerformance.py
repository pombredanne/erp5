##############################################################################
#
# Copyright (c) 2006 Nexedi SARL and Contributors. All Rights Reserved.
#          Aurelien Calonne <aurel@nexedi.com>
#
# WARNING: This program as such is intended to be used by professional
# programmers who take the whole responsability of assessing all potential
# consequences resulting from its eventual inadequacies and bugs
# End users who are looking for a ready-to-use solution with commercial
# garantees and support are strongly adviced to contract a Free Software
# Service Company
#
# This program is Free Software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA 02111-1307, USA.
#
##############################################################################

import unittest
from time import time
import gc

from DateTime import DateTime
from Products.ERP5Type.tests.ERP5TypeTestCase import ERP5TypeTestCase
from zLOG import LOG
from Products.CMFCore.tests.base.testcase import LogInterceptor

# Define variable to chek if performance are good or not
# XXX These variable are specific to the testing environment
# (which has 31645.6 pystones/second)
MIN_OBJECT_VIEW=0.112
MAX_OBJECT_VIEW=0.122
MIN_OBJECT_PROXYFIELD_VIEW=0.2390
MAX_OBJECT_PROXYFIELD_VIEW=0.2490
CURRENT_MIN_OBJECT_VIEW=0.1220
CURRENT_MAX_OBJECT_VIEW=0.1280
MIN_MODULE_VIEW=0.125
MAX_MODULE_VIEW=0.175
MIN_OBJECT_CREATION=0.0070
MAX_OBJECT_CREATION=0.0090
MIN_TIC=0.0260
MAX_TIC=0.0355
LISTBOX_COEF=0.02472
DO_TEST = 1

class TestPerformance(ERP5TypeTestCase, LogInterceptor):

    # Some helper methods
    quiet = 0
    run_all_test = 1

    def getTitle(self):
      return "Performance"

    def getBusinessTemplateList(self):
      """
        Return the list of business templates.
      """
      return ('erp5_base',
              'erp5_ui_test',)

    def getBarModule(self):
      """
      Return the bar module
      """
      return self.getPortal()['bar_module']

    def afterSetUp(self):
      """
        Executed before each test_*.
      """
      self.login()
      self.bar_module = self.getBarModule()
      self.foo_module = self.portal.foo_module

    def beforeTearDown(self):
      get_transaction().abort()
      self.bar_module.manage_delObjects(list(self.bar_module.objectIds()))
      self.foo_module.manage_delObjects(list(self.foo_module.objectIds()))
      gender = self.getPortal().portal_categories['gender']
      gender.manage_delObjects(list(gender.objectIds()))
      gender = self.getPortal().portal_caches.clearAllCache()
      get_transaction().commit()
      self.tic()

    def checkViewBarObject(self, min, max, quiet=quiet, prefix=None):
      # Some init to display form with some value
      if prefix is None:
        prefix = ''
      gender = self.getPortal().portal_categories['gender']
      gender.newContent(id='male', title='Male', portal_type='Category')
      gender.newContent(id='female', title='Female', portal_type='Category')

      bar = self.bar_module.newContent(id='bar',
                                       portal_type='Bar',
                                       title='Bar Test',
                                       quantity=10000,)
      bar.setReference(bar.getRelativeUrl())
      get_transaction().commit()
      self.tic()
      # Check performance
      before_view = time()
      for x in xrange(100):
          bar.Bar_viewPerformance()
      after_view = time()
      req_time = (after_view - before_view)/100.
      if not quiet:
          print "%s time to view object form %.4f < %.4f < %.4f\n" % \
              (prefix, min, req_time, max)
      if DO_TEST:
          self.failUnless(min < req_time < max,
                          '%.4f < %.4f < %.4f' % (min, req_time, max))

    def test_00_viewBarObject(self, quiet=quiet, run=run_all_test,
                              min=None, max=None):
      """
      Estimate average time to render object view
      """
      if not run : return
      if not quiet:
        message = 'Test form to view Bar object'
        LOG('Testing... ', 0, message)
      self.checkViewBarObject(MIN_OBJECT_VIEW, MAX_OBJECT_VIEW,
                              prefix='objective')

#    def test_00b_currentViewBarObject(self, quiet=quiet, run=run_all_test):
#      """
#      Estimate average time to render object view and check with current values
#      """
#      if not run : return
#      if not quiet:
#        message = 'Test form to view Bar object with current values'
#        LOG('Testing... ', 0, message)
#      self.checkViewBarObject(CURRENT_MIN_OBJECT_VIEW, CURRENT_MAX_OBJECT_VIEW,
#                              prefix='current')

    def test_01_viewBarModule(self, quiet=quiet, run=run_all_test):
      """
      Estimate average time to render module view
      """
      if not run : return
      if not quiet:
        message = 'Test form to view Bar module'
        LOG('Testing... ', 0, message)
      get_transaction().commit()
      self.tic()
      view_result = {}
      tic_result = {}
      add_result = {}
      gc.collect()
      # add object in bar module
      for i in xrange(10):
          before_add = time()
          for x in xrange(100):
            p = self.bar_module.newContent(portal_type='Bar',
                                           title='Bar Test',
                                           quantity="%4d" %(x,))
          after_add = time()
          get_transaction().commit()
          before_tic = time()
          self.tic()
          after_tic = time()

          # Explicit collect of the garbage collector,
          # So no garbage collection will happen while reindexing,
          # like this we prevent random garbage collection wich 
          # was making the test failing randomly
          gc.collect()

          before_form = time()
          for x in xrange(100):
            self.bar_module.BarModule_viewBarList()
          after_form = time()
          # store result
          key = "%06d" %(100*i+100,)
          view_result[key] = (after_form - before_form)/100.
          tic_result[key] = (after_tic - before_tic)/100.
          add_result[key] = (after_add - before_add)/100.

      # check result
      keys = view_result.keys()
      keys.sort()
      i = 0
      for key in keys:
        module_value = view_result[key]
        tic_value = tic_result[key]
        add_value = add_result[key]
        min_view = MIN_MODULE_VIEW + LISTBOX_COEF * i
        max_view = MAX_MODULE_VIEW + LISTBOX_COEF * i
        if not quiet:
            print "nb objects = %s\n\tadd = %.4f < %.4f < %.4f" %(key, MIN_OBJECT_CREATION, add_value, MAX_OBJECT_CREATION)
            print "\ttic = %.4f < %.4f < %.4f" %(MIN_TIC, tic_value, MAX_TIC)
            print "\tview = %.4f < %.4f < %.4f" %(min_view, module_value, max_view)
            print
        if DO_TEST:
            self.failUnless(min_view < module_value < max_view,
                            'View: %.4f < %.4f < %.4f' % (
                            min_view, module_value, max_view))
            self.failUnless(
                 MIN_OBJECT_CREATION < add_value < MAX_OBJECT_CREATION,
                'Create: %.4f < %.4f < %.4f' % (
                 MIN_OBJECT_CREATION, add_value, MAX_OBJECT_CREATION))
            self.failUnless(MIN_TIC < tic_value < MAX_TIC,
                            'Tic: %.4f < %.4f < %.4f' % (
                            MIN_TIC, tic_value, MAX_TIC))
        i += 1


    def test_viewProxyField(self, quiet=quiet):
      # render a form with proxy fields: Foo_viewProxyField
      foo = self.foo_module.newContent(
                           portal_type='Foo',
                           title='Bar Test',
                           quantity=10000,
                           price=32,
                           start_date=DateTime(2008,1,1))
      foo.newContent(portal_type='Foo Line',
                     title='Line 1')
      foo.newContent(portal_type='Foo Line',
                     title='Line 2')
      get_transaction().commit()
      self.tic()
      # Check performance
      before_view = time()
      for x in xrange(100):
        foo.Foo_viewProxyField()
      after_view = time()
      req_time = (after_view - before_view)/100.

      if not quiet:
        print "time to view proxyfield form %.4f < %.4f < %.4f\n" % \
              ( MIN_OBJECT_PROXYFIELD_VIEW,
                req_time,
                MAX_OBJECT_PROXYFIELD_VIEW )
      if DO_TEST:
        self.failUnless( MIN_OBJECT_PROXYFIELD_VIEW < req_time
                                    < MAX_OBJECT_PROXYFIELD_VIEW,
          '%.4f < %.4f < %.4f' % (
              MIN_OBJECT_PROXYFIELD_VIEW,
              req_time,
              MAX_OBJECT_PROXYFIELD_VIEW))

def test_suite():
  suite = unittest.TestSuite()
  suite.addTest(unittest.makeSuite(TestPerformance))
  return suite
