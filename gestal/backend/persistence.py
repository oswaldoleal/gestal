from uuid import uuid4
from core import info, config as cfg
from os import path
import sqlite3

class Persistence():
    storage_methods = []

    def __init__(self):
        ds = DefaultStorage()
        self.storage_methods.append(ds)

    def insert(self, obj):
        # TODO return [storage.insert(obj) for storage in self.storage_methods].all()
        for storage in self.storage_methods:
            storage.insert(obj)

    def update(self, obj):
        # TODO return [storage.update(obj) for storage in self.storage_methods].all()
        for storage in self.storage_methods:
            storage.update(obj)

    def delete(self, obj):
        # TODO return [storage.delete(obj) for storage in self.storage_methods].all()
        for storage in self.storage_methods:
            storage.delete(obj)

    def get(self, type, id):
        pass # TODO

    def get_all(self, type):
        pass # TODO

class BaseStorage():
    name = None
    
    def insert(self, obj):
        pass # To be implemented in the other classes

    def update(self, obj):
        pass # To be implemented in the other classes

    def delete(self, obj):
        pass # To be implemented in the other classes

    def get_attribute_names(self, type):
        return [a for a in dir(type) if (not a.startswith('__')) and ('function' not in str(getattr(type, a)))]

    def get_data(self, obj):
        # the id always goes first
        attributes = self.get_attribute_names(type(obj))

        data = []
        for attribute in attributes:
            if (attribute == 'id'):
                data.insert(0, getattr(obj, attribute))
            else:
                data.append(getattr(obj, attribute))

        return data

class DefaultStorage(BaseStorage):
    name = 'default_storage'

    def __init__(self):
        DB_NAME = f'{info.NAME}_{self.name}.db'
        
        if (path.isfile(f'{cfg.DB_PATH}{DB_NAME}')):
            return
        
        con = sqlite3.connect(DB_NAME)

        # TODO: register the models databases

        con.close()

    def insert(self, obj):
        id = self.get_new_id(type(obj))
        data = self.get_data(obj)
        data[0] = id

        query = f'insert into {type(obj).__name__} values (' + ','.join(['?'] * (len(data))) + ')'
        self.execute(query, data)

    def update(self, obj):
        attributes = ','.join([a + ' = ?' for a in self.get_attribute_names(type(obj)) if (a != 'id')])
        data = self.get_data(obj)
        data = data[1:] + data[:1]

        query = f'update {type(obj).__name__} set {attributes} where id = ?'
        self.execute(query, data)

    def delete(self, obj):
        query = f'delete from {type(obj).__name__} where id = ?'
        self.execute(query, (obj.id,))

    def get_new_id(self, type):
        id = str(uuid4())
        query = f'select id from {type.__name__} where id = ?'
        
        while (True):
            result = self.execute(query, (id,))
            if (len(result) == 0):
                return id
            else:
                id = str(uuid4())

    def execute(self, query, data):
        # TODO
        return True