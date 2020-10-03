from core.log import Log
from datetime import datetime
from os import path
from uuid import uuid4
from .models import Project, Task, Team, TeamPermission, User, Tag, TagAssignment
import sqlite3
import core.config as cfg
import core.info as info

class Persistence():
    storage_methods = []

    def __init__(self):
        ds = DefaultStorage()
        self.storage_methods.append(ds)

    def insert(self, obj):
        Log.info(f'Performed INSERT into {type(obj).__name__}', origin = 'Persistence')

        # TODO return [storage.insert(obj) for storage in self.storage_methods].all()
        for storage in self.storage_methods:
            storage.insert(obj)

    def update(self, obj):
        Log.info(f'Performed UPDATE into {type(obj).__name__}', origin = 'Persistence')

        # TODO return [storage.update(obj) for storage in self.storage_methods].all()
        for storage in self.storage_methods:
            storage.update(obj)

    def delete(self, obj):
        Log.info(f'Performed DELETE from {type(obj).__name__}', origin = 'Persistence')

        # TODO return [storage.delete(obj) for storage in self.storage_methods].all()
        for storage in self.storage_methods:
            storage.delete(obj)

    def get(self, type, id):
        pass # TODO

    def get_all(self, type, filter = None):
        Log.info(f'Performed SELECT * from {type.__name__}', origin = 'Persistence')

        return self.storage_methods[0].get_all(type, filter = filter, persistence = self)

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
        id_ind = 0
        i = 0
        for attribute in attributes:
            if (attribute == 'id'):
                data.insert(0, getattr(obj, attribute))
                id_ind = i
            else:
                data.append(getattr(obj, attribute))
            
            i += 1

        return data, id_ind

class DefaultStorage(BaseStorage):
    name = 'default_storage'
    DB_NAME = ''

    def __init__(self):
        Log.info('Initialized Storage', origin = 'DefaultStorage')

        self.DB_NAME = f'{info.NAME}_{self.name}.db'
        Log.debug(f'Database name {self.DB_NAME}', origin = 'DefaultStorage', level = 1)
        
        if (path.isfile(path.join(cfg.DB_PATH, self.DB_NAME))):
            return
        
        # TODO: move the relevant code to the 'execute' function
        con = sqlite3.connect(path.join(cfg.DB_PATH, self.DB_NAME))

        cur = con.cursor()
        for query in self.get_table_queries():
            cur.execute(query)

        query = f'INSERT INTO {Project.__name__} VALUES (?, ?, ?, ?, ?)'
        # TODO: set the proper user id to handle the correct username avoiding clashes with the cloud
        cur.execute(query, (datetime.now().isoformat(), 'Ungrouped tasks', '1', 'Ungrouped', '1'))

        con.commit()

        con.close()

    def get_table_queries(self):
        queries = []

        for type in [Task, Project, Team, TeamPermission, User, Tag, TagAssignment]:
            attributes = self.get_attribute_names(type)
            attributes_type = [a + ' ' + ('INTEGER' if isinstance(getattr(type, a), int) else 'TEXT' if isinstance(getattr(type, a), str) else 'REAL' if isinstance(getattr(type, a), float) else 'NULL') for a in attributes]
            table_name = type.__name__

            attributes = ', '.join(attributes_type)
            query = f'CREATE TABLE {table_name} ({attributes})'
            queries.append(query)

        return queries

    def insert(self, obj):
        id = self.get_new_id(type(obj))
        data, id_ind = self.get_data(obj)
        data = data[1:]
        data.insert(id_ind, id)

        query = f'insert into {type(obj).__name__} values (' + ','.join(['?'] * (len(data))) + ')'
        self.execute(query, data)

    def update(self, obj):
        attributes = ','.join([a + ' = ?' for a in self.get_attribute_names(type(obj)) if (a != 'id')])
        data, _ = self.get_data(obj)
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

    def get_all(self, type, filter = None, persistence = None):
        query = f'select * from {type.__name__}'
        data = []
        if (filter):
            query += ' where'
            for key in filter.keys():
                query += f' {key} = ?'
                data.append(filter[key])
        
        rows = self.execute(query, data = data)

        attribute_names = self.get_attribute_names(type)
        objects = []
        for row in rows:
            data = {}
            for i in range(len(attribute_names)):
                data[attribute_names[i]] = row[i]
            obj = type(data = data, persistence = persistence)
            objects.append(obj)

        return objects

    def execute(self, query, data = ()):
        con = sqlite3.connect(self.DB_NAME)
        cur = con.cursor()

        ret_data = True
        cur.execute(query, data)

        if (query.startswith('select')):
            ret_data = cur.fetchall()
    
        con.commit()
        con.close()
        return ret_data