delivery_portal_type = movement.getDeliveryValue().getPortalType()
assert delivery_portal_type # XXX debug
if delivery_portal_type.startswith('Purchase Packing List'):
  if movement.getDestination() == 'organisation_module/supplier':
    return ['source/account_module/variation_parts']
elif delivery_portal_type.startswith('Internal Packing List'):
  return ['source/account_module/variation_cars']
else:
  raise NotImplementedError

return []