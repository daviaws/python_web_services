from enum import Enum

import db.sqlite_service as sqlite_service

class CONTROLLER_RESULT(Enum):
    SUCCESS = 0
    INVALID_RESOURCE = -1

class Controller():

    def __init__(self):
        self.resources = {}

    def add_handler(self, name, handler):
        self.resources[name] = handler

    def add(self, name, representation):
        if name in self.resources:
            resource = self.resources[name]
            resource.add(representation)
            return CONTROLLER_RESULT.SUCCESS
        else:
            return CONTROLLER_RESULT.INVALID_RESOURCE

    def get(self, name, r_id):
        if name in self.resources:
            resource = self.resources[name]
            response = resource.get(r_id)
            return response
        else:
            return CONTROLLER_RESULT.INVALID_RESOURCE

    def get_all(self, name):
        if name in self.resources:
            resource = self.resources[name]
            response = resource.get_all()
            return response
        else:
            return CONTROLLER_RESULT.INVALID_RESOURCE

    def delete(self, name, r_id):
        if name in self.resources:
            resource = self.resources[name]
            resource.delete(r_id)
            return CONTROLLER_RESULT.SUCCESS
        else:
            return CONTROLLER_RESULT.INVALID_RESOURCE

class PersonHandler():

    def __init__(self):
        self.db = sqlite_service.AppDb()
        print("DB Connected: {}".format(self.db.is_connected()))

    def add(self, representation):
        cpf = representation['cpf']
        name = representation['name']
        age = representation['age']
        height = representation['height']

        if self.db.exist_person('cpf', cpf):
            self.db.insert_person(cpf, name, age, height)
        else:
            self.db.update_person(cpf, name, age, height)

    def get(self, r_id):
        return self.db.select_person('cpf', cpf)['d']

    def get_all(self):
        return self.db.select_person()['d']

    def delete(self, r_id):
        self.db.delete_person(r_id)
