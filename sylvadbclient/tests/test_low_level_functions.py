# -*- coding: utf-8 -*-
import os
import unittest
try:
    import ujson as json
except ImportError:
    import json  # NOQA

from sylvadbclient import API

SYLVADB_TOKEN = os.environ.get("SYLVADB_TOKEN", "default")
SYLVADB_GRAPH = os.environ.get("SYLVADB_GRAPH", None)


def create_and_use_graph(test, name, description):
    params = {}
    params['name'] = name
    params['description'] = description
    result = test.api.post_graph(params=params)
    test.assertTrue(result['name'] == name)
    slug = result['slug']
    test.api.use(slug)
    return result


def create_nodetype(test, name, description):
    nodetype_params = {}
    nodetype_params['name'] = name
    nodetype_params['description'] = description
    result = test.api.post_nodetypes(nodetype_params)
    test.assertTrue(result['name'] == name)
    test.assertTrue(result['description'] == description)
    return result


def create_relationshiptype(test, name, source_slug, target_slug):
    relationshiptype_params = {}
    relationshiptype_params['name'] = name
    relationshiptype_params['source'] = source_slug
    relationshiptype_params['target'] = target_slug
    result = test.api.post_relationshiptypes(relationshiptype_params)
    test.assertTrue(result['name'] == name)
    return result


def create_nodetype_properties(test, nodetype_slug, name, description,
                               datatype):
    property_params = {}
    property_params['key'] = name
    property_params['description'] = description
    property_params['datatype'] = datatype
    properties = test.api.post_nodetype_schema_properties(nodetype_slug,
                                                          property_params)
    test.assertTrue(properties['properties'][0]['label'] == name)
    test.assertTrue(
        properties['properties'][0]['description'] == description)
    test.assertTrue(properties['properties'][0]['type'] == datatype)


def create_relationshiptype_properties(test, type_slug, name, description,
                                       datatype):
    property_params = {}
    property_params['key'] = name
    property_params['description'] = description
    property_params['datatype'] = datatype
    properties = test.api.post_relationshiptype_schema_properties(
        type_slug, property_params)
    test.assertTrue(properties['properties'][0]['label'] == name)
    test.assertTrue(
        properties['properties'][0]['description'] == description)
    test.assertTrue(properties['properties'][0]['type'] == datatype)


class GraphTestSuite(unittest.TestCase):

    def setUp(self):
        self.api = API(token=SYLVADB_TOKEN)

    def test_get_graphs(self):
        result = self.api.get_graphs()
        self.assertTrue(len(result) == 0)
        name = "test_name"
        description = "description_name"
        create_and_use_graph(self, name, description)
        result = self.api.get_graphs()
        self.assertTrue(len(result) != 0)
        slug = result[0]['slug']
        self.api.use(slug)
        self.api.delete_graph()

    def test_post_graph(self):
        name = "test_name"
        description = "description_name"
        create_and_use_graph(self, name, description)
        self.api.delete_graph()

    def test_get_graph(self):
        name = "test_name"
        description = "description_name"
        create_and_use_graph(self, name, description)
        result = self.api.get_graph()
        result_name = result['name']
        self.assertTrue(name == result_name)
        self.api.delete_graph()

    def test_put_graph(self):
        name = "test_name"
        description = "description_name"
        create_and_use_graph(self, name, description)
        new_name = "new_name"
        params = {}
        params['name'] = new_name
        result = self.api.put_graph(params=params)
        self.assertTrue(result['name'] == new_name)
        self.assertTrue(result['description'] is None)
        self.api.delete_graph()

    def test_patch_graph(self, params=None):
        name = "test_name"
        description = "description_name"
        create_and_use_graph(self, name, description)
        new_name = "new_name"
        params = {}
        params['name'] = new_name
        result = self.api.patch_graph(params=params)
        self.assertTrue(result['name'] == new_name)
        self.assertTrue(result['description'] == description)
        self.api.delete_graph()

    def test_delete_graph(self):
        name = "test_name"
        description = "description_name"
        create_and_use_graph(self, name, description)
        self.api.delete_graph()
        result = self.api.get_graphs()
        self.assertTrue(len(result) == 0)

    def test_get_nodetypes(self):
        name = "test_name"
        description = "description_name"
        create_and_use_graph(self, name, description)
        result = self.api.get_nodetypes()
        self.assertTrue(result == [])
        self.api.delete_graph()

    def test_post_nodetypes(self):
        name = "test_name"
        description = "description_name"
        create_and_use_graph(self, name, description)
        nodetype_name = "nodetype_name"
        nodetype_description = "nodetype_description"
        create_nodetype(self, nodetype_name, nodetype_description)
        self.api.delete_graph()

    def test_get_relationshiptypes(self):
        name = "test_name"
        description = "description_name"
        create_and_use_graph(self, name, description)
        result = self.api.get_relationshiptypes()
        self.assertTrue(result == [])
        self.api.delete_graph()

    def test_post_relationshiptypes(self):
        name = "test_name"
        description = "description_name"
        create_and_use_graph(self, name, description)
        # The source nodetype
        nodetype_name = "nodetype_name_source"
        nodetype_description = "nodetype_description"
        result = create_nodetype(self, nodetype_name, nodetype_description)
        source_slug = result['slug']
        # The target nodetype
        nodetype_name = "nodetype_name_target"
        nodetype_description = "nodetype_description"
        result = create_nodetype(self, nodetype_name, nodetype_description)
        target_slug = result['slug']
        relationshiptype_name = "relationshiptype_name"
        create_relationshiptype(self, relationshiptype_name,
                                source_slug, target_slug)
        self.api.delete_graph()

    def test_get_nodetype(self):
        name = "test_name"
        description = "description_name"
        create_and_use_graph(self, name, description)
        nodetype_name = "nodetype_name"
        nodetype_description = "nodetype_description"
        result = create_nodetype(self, nodetype_name, nodetype_description)
        nodetype_slug = result['slug']
        result = self.api.get_nodetype(nodetype_slug)
        self.assertTrue(result['slug'] == nodetype_slug)
        self.assertTrue(result['name'] == nodetype_name)
        self.assertTrue(result['description'] == nodetype_description)
        self.api.delete_graph()

    def test_delete_nodetype(self):
        name = "test_name"
        description = "description_name"
        create_and_use_graph(self, name, description)
        nodetype_name = "nodetype_name"
        nodetype_description = "nodetype_description"
        result = create_nodetype(self, nodetype_name, nodetype_description)
        nodetype_slug = result['slug']
        result = self.api.get_nodetype(nodetype_slug)
        self.assertTrue(result['slug'] == nodetype_slug)
        self.assertTrue(result['name'] == nodetype_name)
        self.assertTrue(result['description'] == nodetype_description)
        self.api.delete_nodetype(nodetype_slug)
        result = self.api.get_nodetypes()
        self.assertTrue(result == [])
        self.api.delete_graph()

    def test_get_nodetype_schema(self):
        name = "test_name"
        description = "description_name"
        create_and_use_graph(self, name, description)
        nodetype_name = "nodetype_name"
        nodetype_description = "nodetype_description"
        result = create_nodetype(self, nodetype_name, nodetype_description)
        nodetype_slug = result['slug']
        result = self.api.get_nodetype(nodetype_slug)
        self.assertTrue(result['slug'] == nodetype_slug)
        self.assertTrue(result['name'] == nodetype_name)
        self.assertTrue(result['description'] == nodetype_description)
        schema = self.api.get_nodetype_schema(nodetype_slug)
        self.assertTrue(schema['name'] == nodetype_name)
        self.assertTrue(schema['description'] == nodetype_description)
        self.api.delete_graph()

    def test_put_nodetype_schema(self):
        name = "test_name"
        description = "description_name"
        create_and_use_graph(self, name, description)
        nodetype_name = "nodetype_name"
        nodetype_description = "nodetype_description"
        result = create_nodetype(self, nodetype_name, nodetype_description)
        nodetype_slug = result['slug']
        result = self.api.get_nodetype(nodetype_slug)
        self.assertTrue(result['slug'] == nodetype_slug)
        self.assertTrue(result['name'] == nodetype_name)
        self.assertTrue(result['description'] == nodetype_description)
        schema = self.api.get_nodetype_schema(nodetype_slug)
        self.assertTrue(schema['name'] == nodetype_name)
        self.assertTrue(schema['description'] == nodetype_description)
        new_name = "new_nodetype_name"
        schema_params = {}
        schema_params['name'] = new_name
        new_schema = self.api.put_nodetype_schema(nodetype_slug, schema_params)
        self.assertTrue(new_schema['name'] == new_name)
        self.api.delete_graph()

    def test_patch_nodetype_schema(self):
        name = "test_name"
        description = "description_name"
        create_and_use_graph(self, name, description)
        nodetype_name = "nodetype_name"
        nodetype_description = "nodetype_description"
        result = create_nodetype(self, nodetype_name, nodetype_description)
        nodetype_slug = result['slug']
        result = self.api.get_nodetype(nodetype_slug)
        self.assertTrue(result['slug'] == nodetype_slug)
        self.assertTrue(result['name'] == nodetype_name)
        self.assertTrue(result['description'] == nodetype_description)
        schema = self.api.get_nodetype_schema(nodetype_slug)
        self.assertTrue(schema['name'] == nodetype_name)
        self.assertTrue(schema['description'] == nodetype_description)
        new_name = "new_nodetype_name"
        schema_params = {}
        schema_params['name'] = new_name
        new_schema = self.api.patch_nodetype_schema(nodetype_slug,
                                                    schema_params)
        self.assertTrue(new_schema['name'] == new_name)
        self.api.delete_graph()

    def test_get_nodetype_schema_properties(self):
        name = "test_name"
        description = "description_name"
        create_and_use_graph(self, name, description)
        nodetype_name = "nodetype_name"
        nodetype_description = "nodetype_description"
        result = create_nodetype(self, nodetype_name, nodetype_description)
        nodetype_slug = result['slug']
        result = self.api.get_nodetype(nodetype_slug)
        self.assertTrue(result['slug'] == nodetype_slug)
        self.assertTrue(result['name'] == nodetype_name)
        self.assertTrue(result['description'] == nodetype_description)
        properties = self.api.get_nodetype_schema_properties(nodetype_slug)
        self.assertTrue(properties['properties'] == [])
        self.api.delete_graph()

    def test_post_nodetype_schema_properties(self):
        name = "test_name"
        description = "description_name"
        create_and_use_graph(self, name, description)
        nodetype_name = "nodetype_name"
        nodetype_description = "nodetype_description"
        result = create_nodetype(self, nodetype_name, nodetype_description)
        nodetype_slug = result['slug']
        result = self.api.get_nodetype(nodetype_slug)
        self.assertTrue(result['slug'] == nodetype_slug)
        self.assertTrue(result['name'] == nodetype_name)
        self.assertTrue(result['description'] == nodetype_description)
        properties = self.api.get_nodetype_schema_properties(nodetype_slug)
        self.assertTrue(properties['properties'] == [])
        prop_name = "property_name"
        prop_description = "property_description"
        prop_datatype = "default"
        create_nodetype_properties(self, nodetype_slug, prop_name,
                                   prop_description, prop_datatype)
        self.api.delete_graph()

    def test_get_relationshiptype(self):
        name = "test_name"
        description = "description_name"
        create_and_use_graph(self, name, description)
        # The source nodetype
        nodetype_name = "nodetype_name_source"
        nodetype_description = "nodetype_description"
        result = create_nodetype(self, nodetype_name, nodetype_description)
        source_slug = result['slug']
        # The target nodetype
        nodetype_name = "nodetype_name_target"
        nodetype_description = "nodetype_description"
        result = create_nodetype(self, nodetype_name, nodetype_description)
        target_slug = result['slug']
        relationshiptype_name = "relationshiptype_name"
        result = create_relationshiptype(self, relationshiptype_name,
                                         source_slug, target_slug)
        relationshiptype_slug = result['slug']
        self.assertTrue(result['name'] == relationshiptype_name)
        result = self.api.get_relationshiptype(relationshiptype_slug)
        self.assertTrue(result['name'] == relationshiptype_name)
        self.api.delete_graph()

    def test_delete_relationshiptype(self):
        name = "test_name"
        description = "description_name"
        create_and_use_graph(self, name, description)
        # The source nodetype
        nodetype_name = "nodetype_name_source"
        nodetype_description = "nodetype_description"
        result = create_nodetype(self, nodetype_name, nodetype_description)
        source_slug = result['slug']
        # The target nodetype
        nodetype_name = "nodetype_name_target"
        nodetype_description = "nodetype_description"
        result = create_nodetype(self, nodetype_name, nodetype_description)
        target_slug = result['slug']
        relationshiptype_name = "relationshiptype_name"
        result = create_relationshiptype(self, relationshiptype_name,
                                         source_slug, target_slug)
        relationshiptype_slug = result['slug']
        self.assertTrue(result['name'] == relationshiptype_name)
        result = self.api.get_relationshiptype(relationshiptype_slug)
        self.assertTrue(result['name'] == relationshiptype_name)
        self.api.delete_relationshiptype(relationshiptype_slug)
        result = self.api.get_relationshiptypes()
        self.assertTrue(result == [])
        self.api.delete_graph()

    def test_get_relationshiptype_schema(self):
        name = "test_name"
        description = "description_name"
        create_and_use_graph(self, name, description)
        # The source nodetype
        nodetype_name = "nodetype_name_source"
        nodetype_description = "nodetype_description"
        result = create_nodetype(self, nodetype_name, nodetype_description)
        source_slug = result['slug']
        # The target nodetype
        nodetype_name = "nodetype_name_target"
        nodetype_description = "nodetype_description"
        result = create_nodetype(self, nodetype_name, nodetype_description)
        target_slug = result['slug']
        relationshiptype_name = "relationshiptype_name"
        result = create_relationshiptype(self, relationshiptype_name,
                                         source_slug, target_slug)
        relationshiptype_slug = result['slug']
        self.assertTrue(result['name'] == relationshiptype_name)
        schema = self.api.get_relationshiptype(relationshiptype_slug)
        self.assertTrue(schema['name'] == relationshiptype_name)
        self.api.delete_graph()

    def test_get_relationshiptype_schema_properties(self):
        name = "test_name"
        description = "description_name"
        create_and_use_graph(self, name, description)
        # The source nodetype
        nodetype_name = "nodetype_name_source"
        nodetype_description = "nodetype_description"
        result = create_nodetype(self, nodetype_name, nodetype_description)
        source_slug = result['slug']
        # The target nodetype
        nodetype_name = "nodetype_name_target"
        nodetype_description = "nodetype_description"
        result = create_nodetype(self, nodetype_name, nodetype_description)
        target_slug = result['slug']
        relationshiptype_name = "relationshiptype_name"
        result = create_relationshiptype(self, relationshiptype_name,
                                         source_slug, target_slug)
        relationshiptype_slug = result['slug']
        self.assertTrue(result['name'] == relationshiptype_name)
        schema = self.api.get_relationshiptype(relationshiptype_slug)
        self.assertTrue(schema['name'] == relationshiptype_name)
        properties = self.api.get_relationshiptype_schema_properties(
            relationshiptype_slug)
        self.assertTrue(properties['properties'] == [])
        self.api.delete_graph()

    def test_post_relationshiptype_schema_properties(self):
        name = "test_name"
        description = "description_name"
        create_and_use_graph(self, name, description)
        # The source nodetype
        nodetype_name = "nodetype_name_source"
        nodetype_description = "nodetype_description"
        result = create_nodetype(self, nodetype_name, nodetype_description)
        source_slug = result['slug']
        # The target nodetype
        nodetype_name = "nodetype_name_target"
        nodetype_description = "nodetype_description"
        result = create_nodetype(self, nodetype_name, nodetype_description)
        target_slug = result['slug']
        relationshiptype_name = "relationshiptype_name"
        result = create_relationshiptype(self, relationshiptype_name,
                                         source_slug, target_slug)
        relationshiptype_slug = result['slug']
        self.assertTrue(result['name'] == relationshiptype_name)
        schema = self.api.get_relationshiptype(relationshiptype_slug)
        self.assertTrue(schema['name'] == relationshiptype_name)
        properties = self.api.get_relationshiptype_schema_properties(
            relationshiptype_slug)
        self.assertTrue(properties['properties'] == [])
        prop_name = "property_name"
        prop_description = "property_description"
        prop_datatype = "default"
        create_relationshiptype_properties(self, relationshiptype_slug,
                                           prop_name, prop_description,
                                           prop_datatype)
        self.api.delete_graph()

    def test_get_nodes(self):
        name = "test_name"
        description = "description_name"
        create_and_use_graph(self, name, description)
        nodetype_name = "nodetype_name"
        nodetype_description = "nodetype_description"
        result = create_nodetype(self, nodetype_name, nodetype_description)
        nodetype_slug = result['slug']
        result = self.api.get_nodetype(nodetype_slug)
        self.assertTrue(result['slug'] == nodetype_slug)
        self.assertTrue(result['name'] == nodetype_name)
        self.assertTrue(result['description'] == nodetype_description)
        result = self.api.get_nodes(nodetype_slug)
        self.assertTrue(result['nodes'] == [])
        self.api.delete_graph()

    def test_post_nodes(self):
        name = "test_name"
        description = "description_name"
        create_and_use_graph(self, name, description)
        nodetype_name = "nodetype_name"
        nodetype_description = "nodetype_description"
        result = create_nodetype(self, nodetype_name, nodetype_description)
        nodetype_slug = result['slug']
        result = self.api.get_nodetype(nodetype_slug)
        self.assertTrue(result['slug'] == nodetype_slug)
        self.assertTrue(result['name'] == nodetype_name)
        self.assertTrue(result['description'] == nodetype_description)
        properties = self.api.get_nodetype_schema_properties(nodetype_slug)
        self.assertTrue(properties['properties'] == [])
        prop_name = "property_name"
        prop_description = "property_description"
        prop_datatype = "default"
        create_nodetype_properties(self, nodetype_slug, prop_name,
                                   prop_description, prop_datatype)
        node_name1 = "nodeName1"
        node_data1 = {prop_name: node_name1}
        node_name2 = "nodeName2"
        node_data2 = {prop_name: node_name2}
        nodes_list = []
        nodes_list.append(node_data1)
        nodes_list.append(node_data2)
        result = self.api.post_nodes(nodetype_slug, nodes_list)
        self.assertTrue(len(result) == 2)
        self.api.delete_graph()

    def test_get_node(self):
        name = "test_name"
        description = "description_name"
        create_and_use_graph(self, name, description)
        nodetype_name = "nodetype_name"
        nodetype_description = "nodetype_description"
        result = create_nodetype(self, nodetype_name, nodetype_description)
        nodetype_slug = result['slug']
        result = self.api.get_nodetype(nodetype_slug)
        self.assertTrue(result['slug'] == nodetype_slug)
        self.assertTrue(result['name'] == nodetype_name)
        self.assertTrue(result['description'] == nodetype_description)
        properties = self.api.get_nodetype_schema_properties(nodetype_slug)
        self.assertTrue(properties['properties'] == [])
        prop_name = "property_name"
        prop_description = "property_description"
        prop_datatype = "default"
        create_nodetype_properties(self, nodetype_slug, prop_name,
                                   prop_description, prop_datatype)
        node_name1 = "nodeName1"
        node_data1 = {prop_name: node_name1}
        nodes_list = []
        nodes_list.append(node_data1)
        result = self.api.post_nodes(nodetype_slug, nodes_list)
        self.assertTrue(len(result) == 1)
        node_id = result[0]
        node = self.api.get_node(nodetype_slug, node_id)
        self.assertTrue(node['properties']['property_name'] == node_name1)
        self.api.delete_graph()

    def test_put_node(self):
        name = "test_name"
        description = "description_name"
        create_and_use_graph(self, name, description)
        nodetype_name = "nodetype_name"
        nodetype_description = "nodetype_description"
        result = create_nodetype(self, nodetype_name, nodetype_description)
        nodetype_slug = result['slug']
        result = self.api.get_nodetype(nodetype_slug)
        self.assertTrue(result['slug'] == nodetype_slug)
        self.assertTrue(result['name'] == nodetype_name)
        self.assertTrue(result['description'] == nodetype_description)
        properties = self.api.get_nodetype_schema_properties(nodetype_slug)
        self.assertTrue(properties['properties'] == [])
        prop_name = "property_name"
        prop_description = "property_description"
        prop_datatype = "default"
        create_nodetype_properties(self, nodetype_slug, prop_name,
                                   prop_description, prop_datatype)
        node_name1 = "nodeName1"
        node_data1 = {prop_name: node_name1}
        nodes_list = []
        nodes_list.append(node_data1)
        result = self.api.post_nodes(nodetype_slug, nodes_list)
        self.assertTrue(len(result) == 1)
        node_id = result[0]
        node = self.api.get_node(nodetype_slug, node_id)
        self.assertTrue(node['properties']['property_name'] == node_name1)
        new_node_name = "newNodeName"
        new_node_data = {prop_name: new_node_name}
        new_data = {'properties': new_node_data}
        node = self.api.put_node(nodetype_slug, node_id, new_data)
        self.assertTrue(node['properties']['property_name'] == new_node_name)
        self.api.delete_graph()

    def test_patch_node(self):
        name = "test_name"
        description = "description_name"
        create_and_use_graph(self, name, description)
        nodetype_name = "nodetype_name"
        nodetype_description = "nodetype_description"
        result = create_nodetype(self, nodetype_name, nodetype_description)
        nodetype_slug = result['slug']
        result = self.api.get_nodetype(nodetype_slug)
        self.assertTrue(result['slug'] == nodetype_slug)
        self.assertTrue(result['name'] == nodetype_name)
        self.assertTrue(result['description'] == nodetype_description)
        properties = self.api.get_nodetype_schema_properties(nodetype_slug)
        self.assertTrue(properties['properties'] == [])
        prop_name = "property_name"
        prop_description = "property_description"
        prop_datatype = "default"
        create_nodetype_properties(self, nodetype_slug, prop_name,
                                   prop_description, prop_datatype)
        node_name1 = "nodeName1"
        node_data1 = {prop_name: node_name1}
        nodes_list = []
        nodes_list.append(node_data1)
        result = self.api.post_nodes(nodetype_slug, nodes_list)
        self.assertTrue(len(result) == 1)
        node_id = result[0]
        node = self.api.get_node(nodetype_slug, node_id)
        self.assertTrue(node['properties']['property_name'] == node_name1)
        new_node_name = "newNodeName"
        new_node_data = {prop_name: new_node_name}
        new_data = {'properties': new_node_data}
        node = self.api.patch_node(nodetype_slug, node_id, new_data)
        self.assertTrue(node['properties']['property_name'] == new_node_name)
        self.api.delete_graph()

    def test_delete_node(self):
        name = "test_name"
        description = "description_name"
        create_and_use_graph(self, name, description)
        nodetype_name = "nodetype_name"
        nodetype_description = "nodetype_description"
        result = create_nodetype(self, nodetype_name, nodetype_description)
        nodetype_slug = result['slug']
        result = self.api.get_nodetype(nodetype_slug)
        self.assertTrue(result['slug'] == nodetype_slug)
        self.assertTrue(result['name'] == nodetype_name)
        self.assertTrue(result['description'] == nodetype_description)
        properties = self.api.get_nodetype_schema_properties(nodetype_slug)
        self.assertTrue(properties['properties'] == [])
        prop_name = "property_name"
        prop_description = "property_description"
        prop_datatype = "default"
        create_nodetype_properties(self, nodetype_slug, prop_name,
                                   prop_description, prop_datatype)
        node_name1 = "nodeName1"
        node_data1 = {prop_name: node_name1}
        nodes_list = []
        nodes_list.append(node_data1)
        result = self.api.post_nodes(nodetype_slug, nodes_list)
        self.assertTrue(len(result) == 1)
        node_id = result[0]
        node = self.api.get_node(nodetype_slug, node_id)
        self.assertTrue(node['properties']['property_name'] == node_name1)
        self.api.delete_node(nodetype_slug, node_id)
        result = self.api.get_nodes(nodetype_slug)
        self.assertTrue(len(result['nodes']) == 0)
        self.api.delete_graph()

    def test_filter_nodes(self):
        name = "test_name"
        description = "description_name"
        create_and_use_graph(self, name, description)
        nodetype_name = "nodetype_name"
        nodetype_description = "nodetype_description"
        result = create_nodetype(self, nodetype_name, nodetype_description)
        nodetype_slug = result['slug']
        result = self.api.get_nodetype(nodetype_slug)
        self.assertTrue(result['slug'] == nodetype_slug)
        self.assertTrue(result['name'] == nodetype_name)
        self.assertTrue(result['description'] == nodetype_description)
        properties = self.api.get_nodetype_schema_properties(nodetype_slug)
        self.assertTrue(properties['properties'] == [])
        prop_name = "property_name"
        prop_description = "property_description"
        prop_datatype = "default"
        create_nodetype_properties(self, nodetype_slug, prop_name,
                                   prop_description, prop_datatype)
        node_name1 = "nodeName1"
        node_data1 = {prop_name: node_name1}
        node_name2 = "nodeName2"
        node_data2 = {prop_name: node_name2}
        nodes_list = []
        nodes_list.append(node_data1)
        nodes_list.append(node_data2)
        result = self.api.post_nodes(nodetype_slug, nodes_list)
        self.assertTrue(len(result) == 2)
        filtering_params = {prop_name: node_name1}
        result = self.api.filter_nodes(nodetype_slug, params=filtering_params)
        self.assertTrue(len(result['nodes']) == 1)
        self.api.delete_graph()

    def test_get_relationships(self):
        name = "test_name"
        description = "description_name"
        create_and_use_graph(self, name, description)
        # The source nodetype
        nodetype_name = "nodetype_name_source"
        nodetype_description = "nodetype_description"
        result = create_nodetype(self, nodetype_name, nodetype_description)
        source_slug = result['slug']
        # The target nodetype
        nodetype_name = "nodetype_name_target"
        nodetype_description = "nodetype_description"
        result = create_nodetype(self, nodetype_name, nodetype_description)
        target_slug = result['slug']
        relationshiptype_name = "relationshiptype_name"
        result = create_relationshiptype(self, relationshiptype_name,
                                         source_slug, target_slug)
        relationshiptype_slug = result['slug']
        self.assertTrue(result['name'] == relationshiptype_name)
        result = self.api.get_relationships(relationshiptype_slug)
        self.assertTrue(result['relationships'] == [])
        self.api.delete_graph()

    def test_post_relationships(self):
        name = "test_name"
        description = "description_name"
        create_and_use_graph(self, name, description)
        # The source nodetype
        nodetype_name = "nodetype_name_source"
        nodetype_description = "nodetype_description"
        result = create_nodetype(self, nodetype_name, nodetype_description)
        source_slug = result['slug']
        prop_name = "property_name"
        prop_description = "property_description"
        prop_datatype = "default"
        create_nodetype_properties(self, source_slug, prop_name,
                                   prop_description, prop_datatype)
        # The target nodetype
        nodetype_name = "nodetype_name_target"
        nodetype_description = "nodetype_description"
        result = create_nodetype(self, nodetype_name, nodetype_description)
        target_slug = result['slug']
        prop_name = "property_name"
        prop_description = "property_description"
        prop_datatype = "default"
        create_nodetype_properties(self, target_slug, prop_name,
                                   prop_description, prop_datatype)
        relationshiptype_name = "relationshiptype_name"
        result = create_relationshiptype(self, relationshiptype_name,
                                         source_slug, target_slug)
        relationshiptype_slug = result['slug']
        self.assertTrue(result['name'] == relationshiptype_name)
        prop_name = "property_name"
        prop_description = "property_description"
        prop_datatype = "default"
        create_relationshiptype_properties(
            self, relationshiptype_slug, prop_name, prop_description,
            prop_datatype)
        # We create nodes for source and target
        node_name_source = "node_name_source"
        node_data_source = {prop_name: node_name_source}
        nodes_list = []
        nodes_list.append(node_data_source)
        result = self.api.post_nodes(source_slug, nodes_list)
        self.assertTrue(len(result) == 1)
        node_source_id = result[0]
        node_name_target = "node_name_target"
        node_data_target = {prop_name: node_name_target}
        nodes_list = []
        nodes_list.append(node_data_target)
        result = self.api.post_nodes(target_slug, nodes_list)
        self.assertTrue(len(result) == 1)
        node_target_id = result[0]
        # We create the relationship
        relationship_name = "relationshipName"
        relationship_data = {prop_name: relationship_name,
                             'source_id': node_source_id,
                             'target_id': node_target_id}
        relationships_list = []
        relationships_list.append(relationship_data)
        result = self.api.post_relationships(
            relationshiptype_slug, relationships_list)
        self.assertTrue(len(result) == 1)
        self.api.delete_graph()

    def test_get_relationship(self):
        name = "test_name"
        description = "description_name"
        create_and_use_graph(self, name, description)
        # The source nodetype
        nodetype_name = "nodetype_name_source"
        nodetype_description = "nodetype_description"
        result = create_nodetype(self, nodetype_name, nodetype_description)
        source_slug = result['slug']
        prop_name = "property_name"
        prop_description = "property_description"
        prop_datatype = "default"
        create_nodetype_properties(self, source_slug, prop_name,
                                   prop_description, prop_datatype)
        # The target nodetype
        nodetype_name = "nodetype_name_target"
        nodetype_description = "nodetype_description"
        result = create_nodetype(self, nodetype_name, nodetype_description)
        target_slug = result['slug']
        prop_name = "property_name"
        prop_description = "property_description"
        prop_datatype = "default"
        create_nodetype_properties(self, target_slug, prop_name,
                                   prop_description, prop_datatype)
        relationshiptype_name = "relationshiptype_name"
        result = create_relationshiptype(self, relationshiptype_name,
                                         source_slug, target_slug)
        relationshiptype_slug = result['slug']
        self.assertTrue(result['name'] == relationshiptype_name)
        prop_name = "property_name"
        prop_description = "property_description"
        prop_datatype = "default"
        create_relationshiptype_properties(self, relationshiptype_slug,
                                           prop_name, prop_description,
                                           prop_datatype)
        # We create nodes for source and target
        node_name_source = "node_name_source"
        node_data_source = {prop_name: node_name_source}
        nodes_list = []
        nodes_list.append(node_data_source)
        result = self.api.post_nodes(source_slug, nodes_list)
        self.assertTrue(len(result) == 1)
        node_source_id = result[0]
        node_name_target = "node_name_target"
        node_data_target = {prop_name: node_name_target}
        nodes_list = []
        nodes_list.append(node_data_target)
        result = self.api.post_nodes(target_slug, nodes_list)
        self.assertTrue(len(result) == 1)
        node_target_id = result[0]
        # We create the relationship
        relationship_name = "relationshipName"
        relationship_data = {prop_name: relationship_name,
                             'source_id': node_source_id,
                             'target_id': node_target_id}
        relationships_list = []
        relationships_list.append(relationship_data)
        result = self.api.post_relationships(
            relationshiptype_slug, relationships_list)
        self.assertTrue(len(result) == 1)
        relationship_id = result[0]
        relationship = self.api.get_relationship(
            relationshiptype_slug, relationship_id)
        self.assertTrue(relationship['label_display'] == relationshiptype_name)
        self.api.delete_graph()

    def test_put_relationship(self):
        name = "test_name"
        description = "description_name"
        create_and_use_graph(self, name, description)
        # The source nodetype
        nodetype_name = "nodetype_name_source"
        nodetype_description = "nodetype_description"
        result = create_nodetype(self, nodetype_name, nodetype_description)
        source_slug = result['slug']
        prop_name = "property_name"
        prop_description = "property_description"
        prop_datatype = "default"
        create_nodetype_properties(self, source_slug, prop_name,
                                   prop_description, prop_datatype)
        # The target nodetype
        nodetype_name = "nodetype_name_target"
        nodetype_description = "nodetype_description"
        result = create_nodetype(self, nodetype_name, nodetype_description)
        target_slug = result['slug']
        prop_name = "property_name"
        prop_description = "property_description"
        prop_datatype = "default"
        create_nodetype_properties(self, target_slug, prop_name,
                                   prop_description, prop_datatype)
        relationshiptype_name = "relationshiptype_name"
        result = create_relationshiptype(self, relationshiptype_name,
                                         source_slug, target_slug)
        relationshiptype_slug = result['slug']
        self.assertTrue(result['name'] == relationshiptype_name)
        prop_name = "property_name"
        prop_description = "property_description"
        prop_datatype = "default"
        create_relationshiptype_properties(self, relationshiptype_slug,
                                           prop_name, prop_description,
                                           prop_datatype)
        # We create nodes for source and target
        node_name_source = "node_name_source"
        node_data_source = {prop_name: node_name_source}
        nodes_list = []
        nodes_list.append(node_data_source)
        result = self.api.post_nodes(source_slug, nodes_list)
        self.assertTrue(len(result) == 1)
        node_source_id = result[0]
        node_name_target = "node_name_target"
        node_data_target = {prop_name: node_name_target}
        nodes_list = []
        nodes_list.append(node_data_target)
        result = self.api.post_nodes(target_slug, nodes_list)
        self.assertTrue(len(result) == 1)
        node_target_id = result[0]
        # We create the relationship
        relationship_name = "relationshipName"
        relationship_data = {prop_name: relationship_name,
                             'source_id': node_source_id,
                             'target_id': node_target_id}
        relationships_list = []
        relationships_list.append(relationship_data)
        result = self.api.post_relationships(
            relationshiptype_slug, relationships_list)
        self.assertTrue(len(result) == 1)
        relationship_id = result[0]
        relationship = self.api.get_relationship(
            relationshiptype_slug, relationship_id)
        new_relationship_name = "newRelationshipName"
        new_relationship_data = {prop_name: new_relationship_name}
        new_data = {'properties': new_relationship_data}
        relationship = self.api.put_relationship(
            relationshiptype_slug, relationship_id, new_data)
        self.api.delete_graph()

    def test_patch_relationship(self):
        name = "test_name"
        description = "description_name"
        create_and_use_graph(self, name, description)
        # The source nodetype
        nodetype_name = "nodetype_name_source"
        nodetype_description = "nodetype_description"
        result = create_nodetype(self, nodetype_name, nodetype_description)
        source_slug = result['slug']
        prop_name = "property_name"
        prop_description = "property_description"
        prop_datatype = "default"
        create_nodetype_properties(self, source_slug, prop_name,
                                   prop_description, prop_datatype)
        # The target nodetype
        nodetype_name = "nodetype_name_target"
        nodetype_description = "nodetype_description"
        result = create_nodetype(self, nodetype_name, nodetype_description)
        target_slug = result['slug']
        prop_name = "property_name"
        prop_description = "property_description"
        prop_datatype = "default"
        create_nodetype_properties(self, target_slug, prop_name,
                                   prop_description, prop_datatype)
        relationshiptype_name = "relationshiptype_name"
        result = create_relationshiptype(self, relationshiptype_name,
                                         source_slug, target_slug)
        relationshiptype_slug = result['slug']
        self.assertTrue(result['name'] == relationshiptype_name)
        prop_name = "property_name"
        prop_description = "property_description"
        prop_datatype = "default"
        create_relationshiptype_properties(self, relationshiptype_slug,
                                           prop_name, prop_description,
                                           prop_datatype)
        # We create nodes for source and target
        node_name_source = "node_name_source"
        node_data_source = {prop_name: node_name_source}
        nodes_list = []
        nodes_list.append(node_data_source)
        result = self.api.post_nodes(source_slug, nodes_list)
        self.assertTrue(len(result) == 1)
        node_source_id = result[0]
        node_name_target = "node_name_target"
        node_data_target = {prop_name: node_name_target}
        nodes_list = []
        nodes_list.append(node_data_target)
        result = self.api.post_nodes(target_slug, nodes_list)
        self.assertTrue(len(result) == 1)
        node_target_id = result[0]
        # We create the relationship
        relationship_name = "relationshipName"
        relationship_data = {prop_name: relationship_name,
                             'source_id': node_source_id,
                             'target_id': node_target_id}
        relationships_list = []
        relationships_list.append(relationship_data)
        result = self.api.post_relationships(
            relationshiptype_slug, relationships_list)
        self.assertTrue(len(result) == 1)
        relationship_id = result[0]
        relationship = self.api.get_relationship(
            relationshiptype_slug, relationship_id)
        new_relationship_name = "newRelationshipName"
        new_relationship_data = {prop_name: new_relationship_name}
        new_data = {'properties': new_relationship_data}
        relationship = self.api.patch_relationship(
            relationshiptype_slug, relationship_id, new_data)
        self.api.delete_graph()

    def test_delete_relationship(self):
        name = "test_name"
        description = "description_name"
        create_and_use_graph(self, name, description)
        # The source nodetype
        nodetype_name = "nodetype_name_source"
        nodetype_description = "nodetype_description"
        result = create_nodetype(self, nodetype_name, nodetype_description)
        source_slug = result['slug']
        prop_name = "property_name"
        prop_description = "property_description"
        prop_datatype = "default"
        create_nodetype_properties(self, source_slug, prop_name,
                                   prop_description, prop_datatype)
        # The target nodetype
        nodetype_name = "nodetype_name_target"
        nodetype_description = "nodetype_description"
        result = create_nodetype(self, nodetype_name, nodetype_description)
        target_slug = result['slug']
        prop_name = "property_name"
        prop_description = "property_description"
        prop_datatype = "default"
        create_nodetype_properties(self, target_slug, prop_name,
                                   prop_description, prop_datatype)
        relationshiptype_name = "relationshiptype_name"
        result = create_relationshiptype(self, relationshiptype_name,
                                         source_slug, target_slug)
        relationshiptype_slug = result['slug']
        self.assertTrue(result['name'] == relationshiptype_name)
        prop_name = "property_name"
        prop_description = "property_description"
        prop_datatype = "default"
        create_relationshiptype_properties(self, relationshiptype_slug,
                                           prop_name, prop_description,
                                           prop_datatype)
        # We create nodes for source and target
        node_name_source = "node_name_source"
        node_data_source = {prop_name: node_name_source}
        nodes_list = []
        nodes_list.append(node_data_source)
        result = self.api.post_nodes(source_slug, nodes_list)
        self.assertTrue(len(result) == 1)
        node_source_id = result[0]
        node_name_target = "node_name_target"
        node_data_target = {prop_name: node_name_target}
        nodes_list = []
        nodes_list.append(node_data_target)
        result = self.api.post_nodes(target_slug, nodes_list)
        self.assertTrue(len(result) == 1)
        node_target_id = result[0]
        # We create the relationship
        relationship_name = "relationshipName"
        relationship_data = {prop_name: relationship_name,
                             'source_id': node_source_id,
                             'target_id': node_target_id}
        relationships_list = []
        relationships_list.append(relationship_data)
        result = self.api.post_relationships(
            relationshiptype_slug, relationships_list)
        self.assertTrue(len(result) == 1)
        relationship_id = result[0]
        self.api.get_relationship(relationshiptype_slug, relationship_id)
        self.api.delete_relationship(relationshiptype_slug, relationship_id)
        result = self.api.get_relationships(relationshiptype_slug)
        self.assertTrue(len(result['relationships']) == 0)
        self.api.delete_graph()
