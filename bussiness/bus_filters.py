
"""
Bus filter handler
"""

from marshmallow import Schema, fields
from bussiness.db_handler import DBHandler


class BusFilterSchema(Schema):
    """
    Bus filter schema to validate bus filters
    """
    id = fields.Str()
    exchange = fields.Str(required=True)
    key = fields.Str()
    exchange_type = fields.Str(required=True)
    durable = fields.Boolean(required=True)
    description = fields.Str()
    category = fields.Str()
    template_id = fields.Str()


class BusFiltersHandler():
    """
    Bus filters handlers class to get, edit, and streaming
    bus filters from the database
    """

    def __init__(self):
        self.db_handler = DBHandler("bus_filters")
        self.db_handler.create_table()

    def get(self, key=None):
        """
        Get all the bus_filters from the database
        :key: Key to search for if is provided
        """
        return self.db_handler.get_data(key)

    def get_realtime(self):
        """
        Get all bus_filters from the database in realtime.
        If bus filter is edited in the db it returns the change.
        This method blocks the curren thread
        Use this method in a separated thread
        """
        return self.db_handler.get_data_streaming()

    def insert(self, bus_filter):
        """
        Insert bus_filter to the database
        :bus_filter: Bus filter or bus filters to insert
        """
        if isinstance(bus_filter, list):
            keys = []
            for bfilter in bus_filter:
                bus_filter_exits = self.get_by_exchange_key(
                    bfilter.get('exchange'), bfilter.get('key'))
                if bus_filter_exits:
                    keys.append(bus_filter_exits['id'])
                else:
                    keys = keys + self.db_handler.insert_data(bfilter)
            return keys

        bus_filter_to_insert = self.get_by_exchange_key(
            bus_filter.get('exchange'), bus_filter.get('key'))
        if bus_filter_to_insert:
            return bus_filter_to_insert['id']
        return self.db_handler.insert_data(bus_filter)

    def edit(self, bus_filter, bus_filter_id):
        """
        Modify bus_filter by his email
        :bus_filter: Bus filter with data edited
        :bus_filter_id: Id of the bus filter to search
        """
        self.db_handler.edit_data(bus_filter, bus_filter_id)

    def delete(self, bus_filter_id):
        """
        Delete bus_filter by his id
        :bus_filter_id: Id of the bus filter to delete
        """
        self.db_handler.delete_data(bus_filter_id)

    def get_by_exchange_key(self, exchange, key):
        """
        Get bus filter by his exhange and key
        :exchange: Exchange param to search
        :key: Key param to search
        """
        bus_filters = self.db_handler.filter_data(
            {'exchange': exchange, 'key': key})
        if bus_filters:
            return bus_filters[0]
        return None

    def delete_template(self, template_id):
        """
        Delete bus filter template and replace in the database
        """
        bus_filters = self.db_handler.filter_data({'template_id': template_id})
        if bus_filters:
            for bus_filter in bus_filters:
                del bus_filter['template_id']
                self.db_handler.replace_data(bus_filter, bus_filter['id'])
