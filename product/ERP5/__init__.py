##############################################################################
#
# Copyright (c) 2002 Nexedi SARL and Contributors. All Rights Reserved.
#                    Jean-Paul Smets-Solane <jp@nexedi.com>
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
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA  02111-1307, USA.
#
##############################################################################
"""
    ERP5 Free Software ERP
"""

# First import the minimal number of packages required by the code generation
from Products.ERP5Type.InitGenerator import generateInitFiles
import sys

# Update the self generated code for Document, PropertySheet and Interface
this_module = sys.modules[ __name__ ]
document_classes = generateInitFiles(this_module, globals())

# Update ERP5 Globals
from Products.ERP5Type.Utils import initializeProduct, updateGlobals
import Interface, PropertySheet, Permissions, Constraint
updateGlobals( this_module, globals(),
                   property_sheet_module = PropertySheet,
                   interface_module = Interface,
                   permissions_module = Permissions,
                   constraint_module = Constraint)

# Define object classes and tools
from Tool import Category, CategoryTool, SimulationTool, RuleTool, IdTool, TemplateTool
import ERP5Site
object_classes = ( Category.Category,
                   Category.BaseCategory,
                   ERP5Site.ERP5Site,
                 )
portal_tools = ( CategoryTool.CategoryTool,
                 SimulationTool.SimulationTool,
                 RuleTool.RuleTool,
                 IdTool.IdTool,
                 TemplateTool.TemplateTool
                )
content_classes = ()
content_constructors = ()

# Import Interaction Workflow
from InteractionWorkflow import InteractionWorkflowDefinition

# Finish installation
def initialize( context ):
  import Document
  initializeProduct(context, this_module, globals(),
                         document_module = Document,
                         document_classes = document_classes,
                         object_classes = object_classes,
                         portal_tools = portal_tools,
                         content_constructors = content_constructors,
                         content_classes = content_classes)
