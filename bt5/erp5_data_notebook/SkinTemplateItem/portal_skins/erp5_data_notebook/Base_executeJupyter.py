"""
Python script to create Data Notebook or update existing Data Notebooks
identifying notebook by reference from user.

Expected behaviour from this script:-
1. Return unauthorized message for non-developer user.
2. Create new 'Data Notebook' for new reference.
3. Add new 'Data Notebook Line'to the existing Data Notebook on basis of reference.
4. Return python dictionary containing list of all notebooks for 'request_reference=True'
"""

portal = context.getPortalObject()
# Check permissions for current user and display message to non-authorized user 
if not portal.Base_checkPermission('portal_components', 'Manage Portal'):
  return "You are not authorized to access the script"

import json

# Convert the request_reference argument string to their respeced boolean values
request_reference = {'True': True, 'False': False}.get(request_reference, False)

# Return python dictionary with title and reference of all notebooks
# for request_reference=True
if request_reference:
  data_notebook_list = portal.portal_catalog(portal_type='Data Notebook')
  notebook_detail_list = [{'reference': obj.getReference(), 'title': obj.getTitle()} for obj in data_notebook_list]
  return notebook_detail_list

if not reference:
  message = "Please set or use reference for the notebook you want to use"
  return message

# Take python_expression as '' for empty code from jupyter frontend
if not python_expression:
  python_expression = ''

# Get Data Notebook with the specific reference
data_notebook = portal.portal_catalog.getResultValue(portal_type='Data Notebook',
                      reference=reference)

# Create new Data Notebook if reference doesn't match with any from existing ones
if not data_notebook:
  notebook_module = portal.getDefaultModule(portal_type='Data Notebook')
  data_notebook = notebook_module.DataNotebookModule_addDataNotebook(
    title=title,
    reference=reference,
    batch_mode=True
  )

# Add new Data Notebook Line to the Data Notebook
data_notebook_line = data_notebook.DataNotebook_addDataNotebookLine(
  notebook_code=python_expression,
  batch_mode=True
)

# Gets the context associated to the data notebook being used
#
old_notebook_context = data_notebook.getNotebookContext()
if not old_notebook_context:
  old_notebook_context = portal.Base_createNotebookContext()

# Pass all to code Base_runJupyter external function which would execute the code
# and returns a dict of result
final_result = context.Base_runJupyter(python_expression, old_notebook_context)
code_result = final_result['result_string']
new_local_variable_dict = final_result['notebook_context']
ename = final_result['ename']
evalue = final_result['evalue']
traceback = final_result['traceback']
status = final_result['status']
mime_type = final_result['mime_type']

# Updates the context in the notebook with the resulting context of code 
# execution.
#
try:
  data_notebook.setNotebookContext(new_local_variable_dict)
except Exception as e:
  return context.Base_getErrorMessageForException(e, new_local_variable_dict)

result = {
  u'code_result': code_result,
  u'ename': ename,
  u'evalue': evalue,
  u'traceback': traceback,
  u'status': status,
  u'mime_type': mime_type
}

# Catch exception while seriaizing the result to be passed to jupyter frontend
# and in case of error put code_result as None and status as 'error' which would
# be shown by Jupyter frontend
try:
  serialized_result = json.dumps(result)
except UnicodeDecodeError:
  result = {
    u'code_result': None,
    u'ename': u'UnicodeDecodeError',
    u'evalue': None,
    u'traceback': None,
    u'status': u'error',
    u'mime_type': mime_type
  }
  serialized_result = json.dumps(result)

data_notebook_line.edit(notebook_code_result=code_result, mime_type=mime_type)

return serialized_result
