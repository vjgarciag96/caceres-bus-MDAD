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

    def get_best_flight(self, origin, target, day, month):
        result = self.client.db('_system').aql.execute(
'''FOR v, e, p IN 2 OUTBOUND 'airports/'''+origin+'''' flights FILTER v._id == 'airports/'''+target+''''
FILTER p.edges[*].Month ALL == '''+month+'''
FILTER p.edges[*].DayofMonth ALL == '''+day+'''
LET flightTime = DATE_DIFF(p.edges[0].DepTimeUTC, p.edges[1].ArrTimeUTC, 'i') SORT flightTime ASC
LIMIT 5
RETURN { flight: p, time: flightTime }'''
)
        collection = list()
        collection.append([student for student in result])
        return collection

    def get_all_airports(self):
        result = self.client.db('_system').aql.execute(
'''FOR airport IN airports
RETURN {
    name:airport.airport,
    id:airport._key
}'''
        )
        collection = list()
        collection.append([student for student in result])
        return collection