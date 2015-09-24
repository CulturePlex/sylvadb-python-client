# -*- coding: utf-8 -*-
import slumber


class SylvadbApiClient():
    # The idea is that this attr get a default value
    sylvadb_api = None

    # Method to connect to the SylvadbAPI
    def api_connect(self, host, auth):
        self.sylvadb_api = slumber.API(host,
                                       auth=auth)

    # Let's start with the API methods that encapsules the client

    # Graphs methods
    def get_graphs(self):
        return self.sylvadb_api.graphs.get()

    def post_graph(self, params=None):
        # The params available are:
        # - name
        # - description
        return self.sylvadb_api.graphs.post(params)

    def get_graph(self, graph_slug):
        return self.sylvadb_api.graphs(graph_slug).get()

    def put_graph(self, graph_slug, params=None):
        # The params available are:
        # - name
        # - description
        # - public
        return self.sylvadb_api.graphs(graph_slug).put(params)

    def patch_graph(self, graph_slug, params=None):
        # The params available are:
        # - name
        # - description
        # - public
        return self.sylvadb_api.graphs(graph_slug).patch(params)

    def delete_graph(self, graph_slug):
        return self.sylvadb_api.graphs(graph_slug).delete()

    # Export and import methods
    # The methods that allow export are all GET
    def export_graph(self, graph_slug):
        return self.sylvadb_api.graphs(graph_slug).export.graph.get()

    def export_schema(self, graph_slug):
        return self.sylvadb_api.graphs(graph_slug).export.schema.get()

    def export_data(self, graph_slug):
        return self.sylvadb_api.graphs(graph_slug).export.data.get()

    # The methods that allow export are all PUT
    # def import_graph(self, graph_slug, params=None):
    #     return self.sylvadb_api.graphs(graph_slug).import.graph.put(params)

    # def import_schema(self, graph_slug, params=None):
    #     return self.sylvadb_api.graphs(graph_slug).import.schema.put(params)

    # def import_data(self, graph_slug, params=None):
    #     return self.sylvadb_api.graphs(graph_slug).import.data.put(params)

    # Schema methods
    def get_nodetypes(self, graph_slug):
        return (self.sylvadb_api
                    .graphs(graph_slug)
                    .types.nodes.get())

    def post_nodetypes(self, graph_slug, params):
        # The params available are:
        # - name
        # - description
        return (self.sylvadb_api
                    .graphs(graph_slug)
                    .types.nodes.get())

    def get_relationshiptypes(self, graph_slug):
        return (self.sylvadb_api
                    .graphs(graph_slug)
                    .types.relationships.get())

    def post_relationshiptypes(self, graph_slug):
        # The params available are:
        # - name
        # - description
        return (self.sylvadb_api
                    .graphs(graph_slug)
                    .types.relationships.get())

    def get_nodetype(self, graph_slug, nodetype_slug):
        return (self.sylvadb_api
                    .graphs(graph_slug)
                    .types.nodes(nodetype_slug).get())

    def delete_nodetype(self, graph_slug, nodetype_slug):
        return (self.sylvadb_api
                    .graphs(graph_slug)
                    .types.nodes(nodetype_slug).delete())

    def get_nodetype_schema(self, graph_slug, nodetype_slug):
        return (self.sylvadb_api
                    .graphs(graph_slug)
                    .types.nodes(nodetype_slug)
                    .schema.get())

    def put_nodetype_schema(self, graph_slug, nodetype_slug, params=None):
        # The params available are:
        # - name
        # - description
        return (self.sylvadb_api
                    .graphs(graph_slug)
                    .types.nodes(nodetype_slug)
                    .schema.put(params))

    def patch_nodetype_schema(self, graph_slug, nodetype_slug, params=None):
        # The params available are:
        # - name
        # - description
        return (self.sylvadb_api
                    .graphs(graph_slug)
                    .types.nodes(nodetype_slug)
                    .schema.patch(params))

    def get_nodetype_schema_properties(self, graph_slug, nodetype_slug):
        return (self.sylvadb_api
                    .graphs(graph_slug)
                    .types.nodes(nodetype_slug)
                    .schema.properties.get())

    def post_nodetype_schema_properties(self, graph_slug,
                                        nodetype_slug, params=None):
        # The params available are:
        # - name
        # - description
        return (self.sylvadb_api
                    .graphs(graph_slug)
                    .types.nodes(nodetype_slug)
                    .schema.properties.post(params))

    def get_relationshiptype(self, graph_slug, relationshiptype_slug):
        return (self.sylvadb_api
                    .graphs(graph_slug)
                    .types.relationships(relationshiptype_slug).get())

    def delete_relationshiptype(self, graph_slug, relationshiptype_slug):
        return (self.sylvadb_api
                    .graphs(graph_slug)
                    .types.relationships(relationshiptype_slug).delete())

    def get_relationshiptype_schema(self, graph_slug, relationshiptype_slug):
        return (self.sylvadb_api
                    .graphs(graph_slug)
                    .types.relationships(relationshiptype_slug)
                    .schema.get())

    def put_relationshiptype_schema(self, graph_slug,
                                    relationshiptype_slug, params=None):
        # The params available are:
        # - name
        # - description
        return (self.sylvadb_api
                    .graphs(graph_slug)
                    .types.relationships(relationshiptype_slug)
                    .schema.put(params))

    def patch_relationshiptype_schema(self, graph_slug,
                                      relationshiptype_slug, params=None):
        # The params available are:
        # - name
        # - description
        return (self.sylvadb_api
                    .graphs(graph_slug)
                    .types.relationships(relationshiptype_slug)
                    .schema.patch(params))

    def get_relationshiptype_schema_properties(self, graph_slug,
                                               relationshiptype_slug):
        return (self.sylvadb_api
                    .graphs(graph_slug)
                    .types.relationships(relationshiptype_slug)
                    .schema.properties.get())

    def post_relationshiptype_schema_properties(self, graph_slug,
                                                relationshiptype_slug,
                                                params=None):
        # The params available are:
        # - name
        # - description
        return (self.sylvadb_api
                    .graphs(graph_slug)
                    .types.relationships(relationshiptype_slug)
                    .schema.properties.post(params))

    # Data methods
    def get_nodes(self, graph_slug, nodetype_slug):
        return (self.sylvadb_api
                    .graphs(graph_slug)
                    .types.nodes(nodetype_slug)
                    .nodes.get())

    def post_nodes(self, graph_slug, nodetype_slug, params=None):
        return (self.sylvadb_api
                    .graphs(graph_slug)
                    .types.nodes(nodetype_slug)
                    .nodes.post(params))

    def get_node(self, graph_slug, nodetype_slug, node_id):
        return (self.sylvadb_api
                    .graphs(graph_slug)
                    .types.nodes(nodetype_slug)
                    .nodes(node_id).get())

    def put_node(self, graph_slug, nodetype_slug, node_id, params=None):
        return (self.sylvadb_api
                    .graphs(graph_slug)
                    .types.nodes(nodetype_slug)
                    .nodes(node_id).put(params))

    def patch_node(self, graph_slug, nodetype_slug, node_id, params=None):
        return (self.sylvadb_api
                    .graphs(graph_slug)
                    .types.nodes(nodetype_slug)
                    .nodes(node_id).patch(params))

    def delete_node(self, graph_slug, nodetype_slug, node_id):
        return (self.sylvadb_api
                    .graphs(graph_slug)
                    .types.nodes(nodetype_slug)
                    .nodes(node_id).delete())

    def get_relationships(self, graph_slug, relationshiptype_slug):
        return (self.sylvadb_api
                    .graphs(graph_slug)
                    .types.relationships(relationshiptype_slug)
                    .relationships.get())

    def post_relationships(self, graph_slug, relationshiptype_slug,
                           params=None):
        return (self.sylvadb_api
                    .graphs(graph_slug)
                    .types.relationships(relationshiptype_slug)
                    .relationships.post(params))

    def get_relationship(self, graph_slug, relationshiptype_slug,
                         relationship_id):
        return (self.sylvadb_api
                    .graphs(graph_slug)
                    .types.relationships(relationshiptype_slug)
                    .relationships(relationship_id).get())

    def put_relationship(self, graph_slug, relationshiptype_slug,
                         relationship_id, params=None):
        return (self.sylvadb_api
                    .graphs(graph_slug)
                    .types.relationships(relationshiptype_slug)
                    .relationships(relationship_id).put(params))

    def patch_relationship(self, graph_slug, relationshiptype_slug,
                           relationship_id, params=None):
        return (self.sylvadb_api
                    .graphs(graph_slug)
                    .types.relationships(relationshiptype_slug)
                    .relationships(relationship_id).patch(params))

    def delete_relationship(self, graph_slug, relationshiptype_slug,
                            relationship_id):
        return (self.sylvadb_api
                    .graphs(graph_slug)
                    .types.relationships(relationshiptype_slug)
                    .relationships(relationship_id).delete())
