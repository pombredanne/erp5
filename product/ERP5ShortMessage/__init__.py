##############################################################################
#                                                                             
# Copyright (c) 2010 Nexedi SA and Contributors. All Rights Reserved.       
#                    François-Xavier Algrain <fxalgrain@tiolive.com>                  
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
    ERP5ShortMessage is a product containing everything needed to implement 
    Short Message management in ERP5.
"""# Update ERP5 Globals
from Products.ERP5Type.Utils import initializeProduct, updateGlobals
import sys, Permissions
this_module = sys.modules[ __name__ ]
document_classes = updateGlobals(this_module, globals(),
                                 permissions_module=Permissions)


from Tool import SMSTool

# Define object classes and tools
object_classes = ()
portal_tools = (SMSTool.SMSTool,
                )

content_classes = ()
content_constructors = ()

# Finish installation
def initialize(context):
  import Document
  initializeProduct(context, this_module, globals(),
                    document_module=Document,
                    document_classes=document_classes,
                    object_classes=object_classes,
                    portal_tools=portal_tools,
                    content_constructors=content_constructors,
                    content_classes=content_classes)
from AccessControl.SecurityInfo import allow_module

allow_module('Products.ERP5ShortMessage.Errors')
