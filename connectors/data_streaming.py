# -*- coding: utf-8 -*-
""""
Data streaming from the DB.
"""
import rethinkdb as r

class DataStreaming(object): 
    def __init__(self, server, port, db_name):
        self.db_name = db_name
        self.con = r.connect(host=server, port=port,
                   db=db_name)

    def get_data(self, table_name):
        """"
        Returns a data streaming. To print the new changes iterate over it.
        """
        con = self.con
        try:
            return r.table(table_name).changes().run(con)
        except: 
            'Error reading database'