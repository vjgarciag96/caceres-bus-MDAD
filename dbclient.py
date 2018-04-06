from arango import ArangoClient

class client():

    def __init__(self):
        self.client = ArangoClient(
            protocol='http',
            host='localhost',
            port=8529,
            username='root',
            password='',
            enable_logging=True
        )

        self.graph = client.db('flights').create_graph('flights_graph')
        self.students = self.graph.create_vertex_collection('airports')
        self.fligths = self.graph.create_edge_definition(
            name='flights',
            from_collections=['airports'],
            to_collections=['airports']
        )