SylvaDB API - Python Client
===========================

The SylvaDB API client allows the interaction with the SylvaDB API in an easily and flexible way.

Installation_
-------------

.. code:: shell

  $ pip install sylvadbclient


`Getting started`_
------------------

To start, we need to instance the main class called `API`. It takes two parameters, the host where our api is running and the authorization to establish the connection.
Optionally, a third parameter `graph_slug` can be passed to the API knows which graph to use by default:

.. code:: python

  >>> from sylvadbclient import API

  >>> api = API(auth=("default", "default"))

  >>> api = API(auth=("default", "default"), graph_slug="graph-1")

Right now, we can interact with the api using the available methods (see the docs). All the responses that we obtain are in JSON format:

.. code:: python

  # We get all the graphs for user "default"
  >>> api.get_graphs()

  # We get the graph called "test"
  >>> api.get_graph("test")

  # We get the graph called "test"
  >>> api.get_graph("test")

  # We get the graph node types
  >>> api.get_nodetypes("test")

However, SylvaDB client provides a higher level API, the `Graph`:

.. code:: python

  >>> from sylvadbclient import Graph

  >>> g = Graph(graph_slug="graph-1")

  >>> g.name
  'Country'

Almost every object can be retrieved from server by invoking the medthod `.pull()`, and any change can be saved by using `.push()`.
In the event of running a `.pull()` before a `.push()`, all local changes are lost.

.. code:: python

  >>> g.description = "Network"

  >>> g.push()

Both nodes and relationships can be listed according to their schema type:

.. code:: python

  >>> g.nodes.types.all()
  [{'description': None, 'name': 'Country', 'schema': 4, 'slug': 'country-2'},
   {'description': None, 'name': 'Software', 'schema': 4, 'slug': 'software-2'},
   {'description': None,
    'name': 'Traditional',
    'schema': 4,
    'slug': 'traditional-2'}]

  >>> country_type = g.nodes.types.single()

  >>> countries = g.nodes[country_type]
  >>> countries
  <SylvaDB NodeDataCollection of country-2 at 0x7f3620f3ea90>

  >>> countries[2:4]
  [{'id': 120, 'properties': {'Name': 'Austria'}},
   {'id': 130, 'properties': {'Name': 'United States'}}]

  >>> countries.all()
  ...

And adding new nodes or relationships is as easy as adding a new dictionary to a type:

.. code:: python

  >>> countries.add({'Name': 'United States'})

  >>> countries[-1]
  {'id': None, 'properties': {'Name': 'United States'}}

  >>> countries.push()

  >>> countries[-1]
  {'id': 180, 'properties': {'Name': 'United States'}}
