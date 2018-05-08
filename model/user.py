# -*- coding: utf-8 -*-
import json
class User:

    def __init__(self, email, name, password):
        self.email = email
        self.name = name
        self.password = password

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, 
            sort_keys=True, indent=4)