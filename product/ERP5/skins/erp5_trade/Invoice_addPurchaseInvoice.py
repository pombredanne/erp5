## Script (Python) "Invoice_addPurchaseInvoice"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=folder, id
##title=
##
product = container.manage_addProduct[ 'ERP5' ]

product.addInvoice(id) 
my_transaction = folder[id]

my_transaction.newContent(portal_type='Purchase Invoice Transaction Line',
                          source='account/dette_fournisseur',
                          id='expense')
my_transaction.newContent(portal_type='Purchase Invoice Transaction Line',
                          source='account/achat_pc_storever',
                          id='payable')
my_transaction.newContent(portal_type='Purchase Invoice Transaction Line',
                          source='account/tva_collectee_196',
                          id='collected_vat')
my_transaction.newContent(portal_type='Purchase Invoice Transaction Line',
                          source='account/tva_recuperable_196',
                          id='refundable_vat')

return my_transaction
