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

    def insert(self, name, representation):
        if name in self.resources:
            resource = self.resources[name]
            response = resource.insert(representation)
            return response
        else:
            return CONTROLLER_RESULT.INVALID_RESOURCE.value

    def get(self, name, r_id):
        if name in self.resources:
            resource = self.resources[name]
            response = resource.get(r_id)
            return response
        else:
            return CONTROLLER_RESULT.INVALID_RESOURCE.value

    def get_all(self, name):
        if name in self.resources:
            resource = self.resources[name]
            response = resource.get_all()
            return response
        else:
            return CONTROLLER_RESULT.INVALID_RESOURCE.value

    def delete(self, name, r_id):
        if name in self.resources:
            resource = self.resources[name]
            return resource.delete(r_id)
        else:
            return CONTROLLER_RESULT.INVALID_RESOURCE.value

    def delete_all(self, name):
        if name in self.resources:
            resource = self.resources[name]
            resource.delete_all()
            return CONTROLLER_RESULT.SUCCESS.value
        else:
            return CONTROLLER_RESULT.INVALID_RESOURCE.value

class PersonHandler():

    def __init__(self):
        self.db = sqlite_service.AppDb()
        print("DB Connected: {}".format(self.db.is_connected()))

    def insert(self, representation):
        try:
            cpf = int(representation['cpf'])
            name = str(representation['name'])
            age = int(representation['age'])
            height = float(representation['height'])
        except Exception as e:
            print(e)
            return {'cpf' : None}

        if self.db.exist_person('cpf', cpf)['d']:
            self.db.update_person(cpf, name, age, height)
        else:
            self.db.insert_person(cpf, name, age, height)
        self.db.commit()
        return {'cpf' : cpf}

    def get(self, cpf):
        return self.db.select_person('cpf', cpf)['d']

    def get_all(self):
        return self.db.select_person()['d']

    def delete(self, cpf):
        self.db.delete_person(cpf)
        self.db.commit()
        return {'cpf' : cpf}

    def delete_all(self):
        self.db.delete_person()
        self.db.commit()
