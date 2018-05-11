# -*- coding: utf-8 -*-

import sys
sys.path.append("../..")
from Configuration.model.variable import Variable


class Property(Variable):

    def __init__(self, val, dom, id, name, introduction, datatype, dataunit, domin_display):
        Variable.__init__(self, val, dom)
        self.id = id
        self.name = name
        self.introduction = introduction
        self.datatype = datatype
        self.dataunit = dataunit
        self.domin_display = domin_display

    def prn_obj(self):
        print('  '.join(['%s:%s' % item for item in self.__dict__.items()]))
