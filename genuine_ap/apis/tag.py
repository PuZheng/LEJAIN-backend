# -*- coding: UTF-8 -*-


class TagMixin(object):

    @property
    def spu(self):
        return self.sku.spu

    @property
    def vendor(self):
        return self.spu.vendor
