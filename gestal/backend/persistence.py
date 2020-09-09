from core import config as cfg, info
from datetime import datetime
from os import path
from uuid import uuid4
from .models import Project, Task, Team, TeamPermission, User
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

    def get_all(self, type, filter = None):
        return self.storage_methods[0].get_all(type, filter = filter)

class BaseStorage():
    name = None
    
    def insert(self, obj):
        pass # To be implemented in the other classes

    def update(self, obj):
        pass # To be implemented in the other classes

    def delete(self, obj):
        pass # To be implemented in the other classes

    def get_attribute_names(self, type):
        return [a for a in dir(type) if ('__' not in a) and ('function' not in str(getattr(type, a)))]

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
    DB_NAME = ''

    def __init__(self):
        self.DB_NAME = f'{info.NAME}_{self.name}.db'
        
        if (path.isfile(f'{cfg.DB_PATH}{self.DB_NAME}')):
            return
        
        # TODO: move the relevant code to the 'execute' function
        con = sqlite3.connect(self.DB_NAME)

        cur = con.cursor()
        for query in self.get_table_queries():
            cur.execute(query)

        query = f'INSERT INTO {Project.__name__} VALUES (?, ?, ?, ?, ?)'
        # TODO: set the proper user id to handle the correct username avoiding clashes with the cloud
        cur.execute(query, (datetime.now().isoformat(), 'Ungrouped tasks', 1, 'Ungrouped', 1))

        con.commit()

        con.close()

    def get_table_queries(self):
        queries = []

        for type in [Task, Project, Team, TeamPermission, User]:
            attributes = self.get_attribute_names(type)
            attributes_type = [a + ' ' + ('INTEGER' if isinstance(getattr(type, a), int) else 'TEXT' if isinstance(getattr(type, a), str) else 'REAL' if isinstance(getattr(type, a), float) else 'NULL') for a in attributes]
            table_name = type.__name__

            attributes = ', '.join(attributes_type)
            query = f'CREATE TABLE {table_name} ({attributes})'
            queries.append(query)

        return queries

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

    def get_all(self, type, filter = None):
        query = f'select * from {type.__name__}'
        if (filter):
            query += ' where'
            for key in filter.keys():
                query += f' {key} = {filter[key]}'
        
        rows = self.execute(query)

        attribute_names = self.get_attribute_names(type)
        objects = []
        for row in rows:
            data = {}
            for i in range(len(attribute_names)):
                data[attribute_names[i]] = row[i]
            obj = type(data = data)
            objects.append(obj)

        return objects

    def execute(self, query, data = ()):
        # TODO

        con = sqlite3.connect(self.DB_NAME)
        cur = con.cursor()

        ret_data = True
        cur.execute(query, data)

        if (query.startswith('select')):
            ret_data = cur.fetchall()
    
        con.commit()
        con.close()
        return ret_data