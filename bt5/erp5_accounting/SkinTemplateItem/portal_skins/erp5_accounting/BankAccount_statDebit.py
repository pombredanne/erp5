"""Total debit (in local currency) of all accounting transactions having this
bank account as payment
"""
kw['payment_uid'] = context.getUid()
kw['omit_asset_decrease'] = 1
kw['asset_price'] = False
kw['node_category'] = 'account_type/asset/cash/bank'

kw.update(
  **context.getPortalObject().portal_selections.getSelectionParamsFor(selection_name, REQUEST=kw.get('REQUEST', None)))

return context.Node_statAccountingBalance(**kw)
