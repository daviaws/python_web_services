from enum import Enum

import os
import sqlite3

DB_PATH ='db/app.db'

class DB_STATUS(Enum):
    SQL_ERROR = 1
    OK = 0
    DATABASE_DOESNT_EXIST = -1
    DATABASE_DISCONECTED = -2

    def __str__(self):
        return str(self.value)

    def __repr__(self):
        return str(self.value)

class AppDb():

    def __init__(self, db_name=DB_PATH):
        self.db_name = db_name
        self.connection = None
        self.cursor = None
        self.connected = False
        self.status = DB_STATUS.OK
        self.open_connection()

    def get_db_name(self):
        return self.db_name

    def is_connected(self):
        return self.connected

    def check_status(self):
        if self.status != DB_STATUS.OK:
            return DB_STATUS.DATABASE_DOESNT_EXIST
        if not self.is_connected():
            return DB_STATUS.DATABASE_DISCONECTED
        return DB_STATUS.OK

    def open_connection(self):
        if not self.is_connected():
            if os.path.exists(self.db_name):
                self.connection = sqlite3.connect(self.db_name)
                self.cursor = self.connection.cursor()
                self.connected = True
            else:
                self.status = DB_STATUS.DATABASE_DOESNT_EXIST
        return self.connected

    def close_connection(self):
        if self.is_connected():
            error_msg = None
            try:
                self.connection.close()
            except sqlite3.Error as e:
                error_msg = e
            else:
                self.connection = None
                self.cursor = None
                self.connected = False
            return error_msg

    def commit(self):
        self.connection.commit()

    def rollback(self):
        self.connection.rollback()

    def fetch_person(self, search):
        data_dict = {}
        for row in search:
            cpf, name, age, height = row
            data_dict[cpf] = {'name' : name, 'age': age, 'height': height}
        return data_dict

    def insert_person(
            self,
            cpf,
            name,
            age,
            height):
        status = self.check_status()
        if status == DB_STATUS.OK:
            params = (
                cpf,
                name,
                age,
                height)
            try:
                c = self.cursor.execute(
                    'Insert into person values (?, ?, ?, ?)', params)
            except sqlite3.Error as e:
                return {'r': DB_STATUS.SQL_ERROR, 'e': e.args[0], 'd': None}
            else:
                return {'r': DB_STATUS.OK, 'd': None}
        else:
            return {'r': status, 'd': None}

    def update_person(
            self,
            cpf,
            name,
            age,
            height):
        status = self.check_status()
        if status == DB_STATUS.OK:
            params = (
                name,
                age,
                height,
                cpf)
            try:
                c = self.cursor.execute(
                    'Update person set name=?, age=?, height=? where cpf=?',
                    params)
            except sqlite3.Error as e:
                return {'r': DB_STATUS.SQL_ERROR, 'e': e.args[0], 'd': None}
            else:
                return {'r': DB_STATUS.OK, 'd': None}
        else:
            return {'r': status, 'd': None}

    def select_person(self, key=None, value=None):
        status = self.check_status()
        if status:
            try:
                if key is not None:                
                    params = (value,)
                    key = key.strip() # REMOVER DEPOIS
                    c = self.cursor.execute(
                        'Select * from person where {}=?'.format(key), params) #SQL INJECTION
                else:
                    c = self.cursor.execute(
                        'Select * from person')
            except sqlite3.Error as e:
                return {'r': DB_STATUS.SQL_ERROR, 'e': e.args[0], 'd': None}
            else:
                search = c.fetchall()
                data_dict = self.fetch_person(search)
                return {'r': DB_STATUS.OK, 'd': data_dict}
        else:
            return {'r': status, 'd': None}

    def exist_person(self, key, value):
        key = key.strip() # REMOVER DEPOIS
        status = self.check_status()
        if status:
            params = (value,)
            try:
                c = self.cursor.execute(
                    'Select * from person where {}=?'.format(key), params) #SQL INJECTION
            except sqlite3.Error as e:
                return {'r': DB_STATUS.SQL_ERROR, 'e': e.args[0], 'd': None}
            else:
                search = c.fetchall()
                data_dict = self.fetch_person(search)
                if data_dict:
                    result = True
                else:
                    result = False
                return {'r': DB_STATUS.OK, 'd': result}
        else:
            return {'r': status, 'd': None}

    def delete_person(self, cpf):
        status = self.check_status()
        if status:
            params = (cpf,)
            try:
                if cpf is not None:
                    c = self.cursor.execute(
                        'Delete from person where cpf=?', params)
                else:
                    c = self.cursor.execute(
                        'Delete from person')
            except sqlite3.Error as e:
                return {'r': DB_STATUS.SQL_ERROR, 'e': e.args[0], 'd': None}
            else:
                return {'r': DB_STATUS.OK, 'd': None}
        else:
            return {'r': status, 'd': None}