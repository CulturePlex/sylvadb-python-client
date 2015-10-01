# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
import os

import slumber

HOST = "http://api.sylvadb.com/v1/"
SYLVADB_API = os.environ.get("SYLVADB_API", HOST)
NODE = "node"
RELATIONSHIP = "relationship"


# Extracted from Six for Python 2 and 3 compatibility
def add_metaclass(metaclass):
    """Class decorator for creating a class with a metaclass."""
    def wrapper(cls):
        orig_vars = cls.__dict__.copy()
        slots = orig_vars.get('__slots__')
        if slots is not None:
            if isinstance(slots, str):
                slots = [slots]
            for slots_var in slots:
                orig_vars.pop(slots_var)
        orig_vars.pop('__dict__', None)
        orig_vars.pop('__weakref__', None)
        return metaclass(cls.__name__, cls.__bases__, orig_vars)
    return wrapper


class BaseMeta(type):
    """Metaclass to populate resources properties by looking up _properties"""

    def __new__(metaname, classname, baseclasses, attrs):  # noqa
        cls = type.__new__(metaname, classname, baseclasses, attrs)
        for attr in cls._properties.keys():
            setattr(cls, attr, property(
                # Getter
                lambda self: self._properties.get(attr, None),
                # Setter
                lambda self, value: self._properties.__setitem__(attr, value),
            ))
        return cls


@add_metaclass(BaseMeta)
class Graph(object):
    """Graph class with properties and access to data and schema"""

    _properties = {"name": None, "description": None}  # For the metaclass

    def __init__(self, graph_slug, auth):
        self._api = API(auth=auth, graph_slug=graph_slug)
        self.nodes = Data(api=self._api, mode=NODE)
        self.relationships = Data(api=self._api, mode=RELATIONSHIP)
        self.rels = self.relationships

        self.pull()

    def push(self):
        """Push changes from the Graph properties to the server"""
        self._api.patch_graph(params=self._properties)

    def pull(self):
        """Pull changes to the Graph properties from the server"""
        _properties = self._api.get_graph()
        for prop in self._properties:
            self._properties[prop] = _properties[prop]

    def destroy(self):
        """Delete all contents and remove the Graph"""
        return self._api.delete_graph()

    def export(self, data=True, schema=True):
        """Export Graph data, schema or both"""
        if data and not schema:
            return self._api.export_data()
        elif not data and schema:
            return self._api.export_schema()
        else:
            return self._api.export_graph()


class Data(object):
    """Data class to handle nodes and relationships"""

    def __init__(self, api, mode):
        self._api = api
        self._mode = mode
        self._types = None
        self._schema = None
        self._datacols = {}

    def pull(self):
        """Pull data types from the server"""
        self._types = getattr(self._api, "get_{}types".format(self._mode))()

    @property
    def types(self):
        """Lazy loading property to list data types (node and rel types)"""
        if self._types is None:
            self.pull()
        return self._types

    def schema(self, datatype):
        """Get the schema for the type"""
        _key = self.__keytransform__(datatype)
        if self._schema is None:
            self._schema = getattr(
                self._api, "get_{}type_schema".format(self._mode))(_key)
        return self._schema

    def __getitem__(self, datatype):
        """
        Return a `DataCollection` of type `datatype`, referring to a node type
        or relationship type. If not found, a `KeyError` is returned
        """
        _key = self.__keytransform__(datatype)
        if _key in self.types or _key in [t["slug"] for t in self.types]:
            if _key not in self._datacols:
                # Required step to keep track of new data to add in collections
                data_collections = DataCollection(self._api, self._mode, _key)
                self._datacols[_key] = data_collections
            return self._datacols[_key]
        else:
            raise KeyError("{}type '{}' not found".format(self._mode, _key))

    def get(self, datatype, *args, **kwargs):
        """
        Return a `DataCollection` of type `datatype`, referring to a node type
        or relationship type. If not found, a `KeyError` is returned.
        An optional `default` value can be passed.
        """
        _key = self.__keytransform__(datatype)
        try:
            return self.__getitem__(_key)
        except KeyError as e:
            if args or kwargs:
                return kwargs.get("default", args[0])
            else:
                raise e

    def properties(self, datatype):
        """
        Return the properties from the type of `type_slug`
        """
        _key = self.__keytransform__(datatype)
        return getattr(
            self._api,
            "get_{}type_schema_properties".format(self._mode))(_key)

    def delete_properties(self, datatype):
        """
        Return the properties from the type of `type_slug`
        """
        _key = self.__keytransform__(datatype)
        return getattr(
            self._api,
            "delete_{}type_schema_properties".format(self._mode))(_key)

    def __iter__(self):
        """Return an interator over the types"""
        return iter(self.types)

    def __len__(self):
        """Return the number of types"""
        return len(self.types)

    def __keytransform__(self, key):
        """
        Extract the right key, `key` can be a string containing a slug,
        an object with a `_slug` attribute, or a dictionary with a 'slug' key.
        """
        if isinstance(key, dict):
            return key.get("slug")
        elif hasattr(key, "_slug"):
            return key._slug
        return key


class DataCollection(object):
    """DataCollection class to handle collection of nodes or relationships"""

    def __init__(self, api, mode, datatype_slug):
        self._api = api
        self._mode = mode
        self._slug = datatype_slug
        self._data = None
        self._to_add = []  # Tracks new data to add in push

    def push(self):
        """Push new data to the server for the datatype `datatype_slug`"""
        if self._to_add:
            func = getattr(self._api, "post_{}s".format(self._mode))
            func(self._slug, params=self._to_add)
            self._to_add = []

    def pull(self):
        """Pull data from the server"""
        func = getattr(self._api, "get_{}s".format(self._mode))
        self._data = func(self._slug)
        self._to_add = []

    @property
    def data(self):
        """Lazy loading the data (list of nodes and relationships)"""
        if self._data is None:
            self.pull()
        return self._data

    def append(self, data_dict):
        """Add a new data dictionary to be added on a push"""
        self._to_add.append(data_dict)

    def all(self):
        """Return all the elements in the collection"""
        return self.data.get("{}s".format(self._mode), []) + self._to_add

    def single(self):
        """Return the first item dictionary in the collection"""
        if self.data.get("{}s".format(self._mode), []):
            return self.data["{}s".format(self._mode)][0]

    def __iter__(self):
        """Return an interator over the data"""
        return iter(self.all())

    def __len__(self):
        """Return the number of elements in the data"""
        return len(self.all())


class API(object):

    def __init__(self, auth, graph_slug=None):
        self._api = slumber.API(SYLVADB_API, auth=auth)
        self._slug = graph_slug

    def use(self, graph_slug):
        """Change the graph over with the API works"""
        self._slug = graph_slug

    # Graphs methods

    def filter_graphs(self, params=None):
        # TODO: Filter and search
        return self._api.graphs.filter(params)

    def get_graphs(self):
        return self._api.graphs.get()

    def post_graph(self, params=None):
        # The params available are:
        # - name
        # - description
        return self._api.graphs.post(params)

    def get_graph(self):
        return self._api.graphs(self._slug).get()

    def put_graph(self, params=None):
        # The params available are:
        # - name
        # - description
        # - public
        return self._api.graphs(self._slug).put(params)

    def patch_graph(self, params=None):
        # The params available are:
        # - name
        # - description
        # - public
        return self._api.graphs(self._slug).patch(params)

    def delete_graph(self):
        return self._api.graphs(self._slug).delete()

    # Export and import methods
    # The methods that allow export are all GET
    def export_graph(self):
        return self._api.graphs(self._slug).export.graph.get()

    def export_schema(self):
        return self._api.graphs(self._slug).export.schema.get()

    def export_data(self):
        return self._api.graphs(self._slug).export.data.get()

    # The methods that allow export are all PUT
    # def import_graph(self, params=None):
    #     return self._api.graphs(self._slug).import.graph.put(params)

    # def import_schema(self, params=None):
    #     return self._api.graphs(self._slug).import.schema.put(params)

    # def import_data(self, params=None):
    #     return self._api.graphs(self._slug).import.data.put(params)

    # Schema methods
    def get_nodetypes(self):
        return (self._api
                    .graphs(self._slug)
                    .types.nodes.get())

    def post_nodetypes(self, params):
        # The params available are:
        # - name
        # - description
        return (self._api
                    .graphs(self._slug)
                    .types.nodes.post(params=params))

    def get_relationshiptypes(self):
        return (self._api
                    .graphs(self._slug)
                    .types.relationships.get())

    def post_relationshiptypes(self, params):
        # The params available are:
        # - name
        # - description
        return (self._api
                    .graphs(self._slug)
                    .types.relationships.post(params=params))

    def get_nodetype(self, nodetype_slug):
        return (self._api
                    .graphs(self._slug)
                    .types.nodes(nodetype_slug).get())

    def delete_nodetype(self, nodetype_slug):
        return (self._api
                    .graphs(self._slug)
                    .types.nodes(nodetype_slug).delete())

    def get_nodetype_schema(self, nodetype_slug):
        return (self._api
                    .graphs(self._slug)
                    .types.nodes(nodetype_slug)
                    .schema.get())

    def put_nodetype_schema(self, nodetype_slug, params=None):
        # The params available are:
        # - name
        # - description
        return (self._api
                    .graphs(self._slug)
                    .types.nodes(nodetype_slug)
                    .schema.put(params))

    def patch_nodetype_schema(self, nodetype_slug, params=None):
        # The params available are:
        # - name
        # - description
        return (self._api
                    .graphs(self._slug)
                    .types.nodes(nodetype_slug)
                    .schema.patch(params))

    def get_nodetype_schema_properties(self, nodetype_slug):
        return (self._api
                    .graphs(self._slug)
                    .types.nodes(nodetype_slug)
                    .schema.properties.get())

    def post_nodetype_schema_properties(self, nodetype_slug, params=None):
        # The params available are:
        # - name
        # - description
        return (self._api
                    .graphs(self._slug)
                    .types.nodes(nodetype_slug)
                    .schema.properties.post(params))

    def get_relationshiptype(self, relationshiptype_slug):
        return (self._api
                    .graphs(self._slug)
                    .types.relationships(relationshiptype_slug).get())

    def delete_relationshiptype(self, relationshiptype_slug):
        return (self._api
                    .graphs(self._slug)
                    .types.relationships(relationshiptype_slug).delete())

    def get_relationshiptype_schema(self, relationshiptype_slug):
        return (self._api
                    .graphs(self._slug)
                    .types.relationships(relationshiptype_slug)
                    .schema.get())

    def put_relationshiptype_schema(self, relationshiptype_slug, params=None):
        # The params available are:
        # - name
        # - description
        return (self._api
                    .graphs(self._slug)
                    .types.relationships(relationshiptype_slug)
                    .schema.put(params))

    def patch_relationshiptype_schema(self, relationshiptype_slug,
                                      params=None):
        # The params available are:
        # - name
        # - description
        return (self._api
                    .graphs(self._slug)
                    .types.relationships(relationshiptype_slug)
                    .schema.patch(params))

    def get_relationshiptype_schema_properties(self, relationshiptype_slug):
        return (self._api
                    .graphs(self._slug)
                    .types.relationships(relationshiptype_slug)
                    .schema.properties.get())

    def post_relationshiptype_schema_properties(self, relationshiptype_slug,
                                                params=None):
        # The params available are:
        # - name
        # - description
        return (self._api
                    .graphs(self._slug)
                    .types.relationships(relationshiptype_slug)
                    .schema.properties.post(params))

    # Data methods
    def get_nodes(self, nodetype_slug):
        return (self._api
                    .graphs(self._slug)
                    .types.nodes(nodetype_slug)
                    .nodes.get())

    def post_nodes(self, nodetype_slug, params=None):
        return (self._api
                    .graphs(self._slug)
                    .types.nodes(nodetype_slug)
                    .nodes.post(params))

    def get_node(self, nodetype_slug, node_id):
        return (self._api
                    .graphs(self._slug)
                    .types.nodes(nodetype_slug)
                    .nodes(node_id).get())

    def put_node(self, nodetype_slug, node_id, params=None):
        return (self._api
                    .graphs(self._slug)
                    .types.nodes(nodetype_slug)
                    .nodes(node_id).put(params))

    def patch_node(self, nodetype_slug, node_id, params=None):
        return (self._api
                    .graphs(self._slug)
                    .types.nodes(nodetype_slug)
                    .nodes(node_id).patch(params))

    def delete_node(self, nodetype_slug, node_id):
        return (self._api
                    .graphs(self._slug)
                    .types.nodes(nodetype_slug)
                    .nodes(node_id).delete())

    def get_relationships(self, relationshiptype_slug):
        return (self._api
                    .graphs(self._slug)
                    .types.relationships(relationshiptype_slug)
                    .relationships.get())

    def post_relationships(self, relationshiptype_slug,
                           params=None):
        return (self._api
                    .graphs(self._slug)
                    .types.relationships(relationshiptype_slug)
                    .relationships.post(params))

    def get_relationship(self, relationshiptype_slug,
                         relationship_id):
        return (self._api
                    .graphs(self._slug)
                    .types.relationships(relationshiptype_slug)
                    .relationships(relationship_id).get())

    def put_relationship(self, relationshiptype_slug,
                         relationship_id, params=None):
        return (self._api
                    .graphs(self._slug)
                    .types.relationships(relationshiptype_slug)
                    .relationships(relationship_id).put(params))

    def patch_relationship(self, relationshiptype_slug,
                           relationship_id, params=None):
        return (self._api
                    .graphs(self._slug)
                    .types.relationships(relationshiptype_slug)
                    .relationships(relationship_id).patch(params))

    def delete_relationship(self, relationshiptype_slug,
                            relationship_id):
        return (self._api
                    .graphs(self._slug)
                    .types.relationships(relationshiptype_slug)
                    .relationships(relationship_id).delete())
