# -*- coding: utf-8 -*-

class Component:

    def __init__(self, id, father_component_id, name, introduction):
        self.id = id
        self.father_component_id = father_component_id
        self.name = name
        self.introduction = introduction

    def prn_obj(self):
        print('  '.join(['%s:%s' % item for item in self.__dict__.items()]))
