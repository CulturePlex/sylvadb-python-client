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
    """Metaclass to populate resources properties by looking up _attrs"""

    def __new__(metaname, classname, baseclasses, attrs):  # noqa
        cls = type.__new__(metaname, classname, baseclasses, attrs)
        for attr in cls._attrs.keys():
            setattr(cls, attr, property(
                # Getter
                lambda self: self._attrs.get(attr, None),
                # Setter
                lambda self, value: self._attrs.__setitem__(attr, value),
            ))
        return cls


class Base(object):

    def get(self, key, *args, **kwargs):
        """
        If key is not found, a `KeyError` is returned.
        An optional `default` value can be passed.
        """
        _key = self.__keytransform__(key)
        try:
            return self.__getitem__(_key)
        except KeyError as e:
            if args or kwargs:
                return kwargs.get("default", args[0])
            else:
                raise e

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

    def __repr__(self):
        mode = getattr(self, "_mode", None)
        slug = getattr(self, "_slug", None)
        if mode is not None:
            if slug is not None:
                msg = "{}{} of {}".format(mode.capitalize(),
                                          self.__class__.__name__, slug)
            else:
                msg = "{}{}".format(mode.capitalize(), self.__class__.__name__)
        else:
            msg = "{}".format(self.__class__.__name__)
        return "<SylvaDB {} at {}>".format(msg, hex(id(self)))


@add_metaclass(BaseMeta)
class Graph(object):
    """Graph class with properties and access to data and schema"""
    _attrs = {
        "name": None,
        "description": None,
        "public": False,
    }  # For the metaclass

    def __init__(self, graph_slug, auth):
        self._api = API(auth=auth, graph_slug=graph_slug)
        self.nodes = Data(api=self._api, mode=NODE)
        self.relationships = Data(api=self._api, mode=RELATIONSHIP)
        self.rels = self.relationships
        self.pull()

    def push(self):
        """Push changes from the Graph properties to the server"""
        self._api.patch_graph(params=self._attrs)

    def pull(self):
        """Pull changes to the Graph properties from the server"""
        _attrs = self._api.get_graph()
        for prop in self._attrs:
            self._attrs[prop] = _attrs[prop]

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


class Data(Base):
    """Data class to handle nodes and relationships"""

    def __init__(self, api, mode):
        self._api = api
        self._mode = mode
        self._types = None
        self._datacols = {}

    @property
    def types(self):
        """Lazy loading property to list data types (node and rel types)"""
        if self._types is None:
            self._types = TypeCollection(self._api, self._mode)
        return self._types

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

    def __iter__(self):
        """Return an interator over the types"""
        return iter(self.types)

    def __len__(self):
        """Return the number of types"""
        return len(self.types)


class BaseCollection(Base):
    """BaseCollection class to handle collections"""

    def __init__(self, api, mode, slug=None):
        self._api = api
        self._mode = mode
        self._slug = slug
        self._data = None
        self._to_add = []  # Tracks new data to add in push

    @property
    def data(self):
        """Lazy loading the data (list of nodes and relationships)"""
        if self._data is None:
            self.pull()
        return self._data

    def _hydrate(self, data_dict):
        """Transform data to be sent to the server. Override to customize"""
        return data_dict

    def _dehydrate(self, data_dict):
        """Transform data from server. Override to customize"""
        return data_dict

    def add(self, data_dict):
        """Add a new data dictionary to be added on a push"""
        self._to_add.append(self._hydrate(data_dict))

    def all(self):
        """Return all the elements in the collection"""
        return self.data + self._to_add

    def single(self):
        """Return the first item dictionary in the collection"""
        data = self.data + self._to_add
        if data:
            return data[0]

    def __getitem__(self, key):
        # TODO: Lazy loading and slicing from server
        _key = self.__keytransform__(key)
        if isinstance(_key, (int, slice)):
            return self.all()[_key]

    def __iter__(self):
        """Return an interator over the data"""
        return iter(self.all())

    def __len__(self):
        """Return the number of elements in the data"""
        return len(self.all())


class DataCollection(BaseCollection):
    """DataCollection class to handle collection of nodes or relationships"""

    def __init__(self, api, mode, slug=None):
        super(DataCollection, self).__init__(api, mode, slug)
        self._properties = None

    def _hydrate(self, data_dict):
        """Transform data to be sent to the server. Override to customize"""
        return {"id": None, "properties": data_dict}

    def push(self):
        """Push new data to the server for the datatype `datatype_slug`"""
        if self._to_add:
            func = getattr(self._api, "post_{}s".format(self._mode))
            ids = func(self._slug, params=self._to_add)
            if ids:
                # Update IDs as returned by the server
                for i, _id in enumerate(ids):
                    self._to_add[i].update({"id": _id})
                self._data += self._to_add
            self._to_add = []

    def pull(self):
        """Pull data from the server"""
        func = getattr(self._api, "get_{}s".format(self._mode))
        data = func(self._slug)
        self._data = data.get("{}s".format(self._mode), [])
        self._to_add = []

    @property
    def properties(self):
        """Lazy loading the properties of a data type"""
        if self._properties is None:
            self._properties = PropertyCollection(self._api, self._mode,
                                                  self._slug)
        return self._properties


class TypeCollection(BaseCollection):
    """TypeCollection class to handle collection of nodes or rels types"""

    def push(self):
        """Push new data to the server for the datatype `datatype_slug`"""
        if self._to_add:
            func = getattr(self._api, "post_{}types".format(self._mode))
            func(params=self._to_add)
            self._to_add = []

    def pull(self):
        """Pull data from the server"""
        func = getattr(self._api, "get_{}types".format(self._mode))
        self._data = func()
        self._to_add = []


class PropertyCollection(BaseCollection):

    def pull(self):
        """Pull type properties from the server"""
        func = getattr(self._api,
                       "get_{}type_schema_properties".format(self._mode))
        self._data = func(self._slug)
        if self._data:
            self._data = self._data["properties"]


class SlumberTokenAuth():
    def __init__(self, token):
        self.token = token

    def __call__(self, r):
        r.headers['Authorization'] = "Token {0}".format(self.token)
        return r


class API(object):

    def __init__(self, token, graph_slug=None):
        self._api = slumber.API(SYLVADB_API, auth=SlumberTokenAuth(token))
        self._slug = graph_slug

    def __repr__(self):
        return "<SylvaDB API at {}>".format(hex(id(self)))

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

    def filter_nodes(self, nodetype_slug, limit=None, offset=None,
                     params=None):
        return (self._api
                    .graphs(self._slug)
                    .types.nodes(nodetype_slug)
                    .filter.get(**params))
