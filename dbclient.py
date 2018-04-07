from arango import ArangoClient


class arangodb_client:

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
        query = '''FOR v, e, p IN 2 OUTBOUND '/%s' flights FILTER v._id == '%s'
FILTER p.edges[*].Month ALL == %s
FILTER p.edges[*].DayofMonth ALL == %s
FILTER DATE_ADD(p.edges[0].ArrTimeUTC, 20, 'minutes') < p.edges[1].DepTimeUTC LET flightTime = DATE_DIFF(p.edges[0].DepTimeUTC, p.edges[1].ArrTimeUTC, 'i') SORT flightTime ASC
LIMIT 1
RETURN { flight: p, time: flightTime }'''
        query = query % (origin, target, day, month)
        result = self.client.db('_system').aql.execute(query)
        collection = list()
        for student in result:
            collection.append(student)
        return collection

    def get_all_airports(self):
        query = '''FOR airport IN airports RETURN { name:airport.airport, id:airport._id}'''
        result = self.client.db('_system').aql.execute(query)
        collection = list()
        for student in result:
            collection.append(student)
        return collection

    def get_coordinates_from_airport(self, id):
        query = '''FOR airport IN airports
FILTER airport._id == '%s'
RETURN {
    lat:airport.lat,
    long:airport.long
}'''
        query = query % (id)
        result = self.client.db('_system').aql.execute(query)
        collection = list()
        for student in result:
            collection.append(student)
        return collection
