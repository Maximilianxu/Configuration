# -*- coding: utf-8 -*-

class Product:

    def __init__(self, id, name, introduction, is_release, deadline, root_component_id):
        self.id = id
        self.name = name
        self.introduction = introduction
        self.is_release = is_release    #0表示产品未发布，1表示产品发布
        self.deadline = deadline
        self.root_component_id = root_component_id

    def prn_obj(self):
        print('  '.join(['%s:%s' % item for item in self.__dict__.items()]))
