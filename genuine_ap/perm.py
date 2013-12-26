# -*- coding: UTF-8 -*-
from flask.ext.principal import ItemNeed



view_vendor_list_need = ItemNeed('view', 'all', 'vendor')

permissions = {}
