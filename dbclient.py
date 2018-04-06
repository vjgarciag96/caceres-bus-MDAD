from arango import ArangoClient


class Client:

    def __init__(self):
        lines = open('credentials.txt').read()
        credentials = lines.split(',')
        username = credentials[0]
        password = credentials[1]
        self.client = ArangoClient(
            protocol='http',
            host='localhost',
            port=8529,
            username=username,
            password=password,
            enable_logging=True
        )

    def get_flights(self):
        result = self.client.db('_system').aql.execute('FOR s IN flights RETURN s')
        print(result)