# -*- coding: utf-8 -*-
import json
class User:

    def __init__(self, email, name, password, role, company, profession):
        self.email = email
        self.name = name
        self.password = password
        self.role = role    # 0代表专家，1代表客户
        self.company = company
        self.profession = profession

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, 
            sort_keys=True, indent=4)