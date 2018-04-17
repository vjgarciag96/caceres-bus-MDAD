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

    def get_shortest_bus_path(self, origin, target):
        shortest_bus_path_query = "FOR stop, trip IN OUTBOUND SHORTEST_PATH '{}' TO '{}' trips RETURN {{'stop': stop, 'bus_line':trip.route_short_name}}".format('stops/{}'.format(origin), 'stops/{}'.format(target))
        query_result = self.client.db('_system').aql.execute(shortest_bus_path_query)
        bus_path_points = list()
        for point in query_result:
            bus_path_points.append(point)
        return bus_path_points

    def get_best_flight(self, origin, target, day, month):
        query = '''FOR v, e, p IN 2 OUTBOUND '%s' flights FILTER v._id == '%s'
FILTER p.edges[*].Month ALL == %s
FILTER p.edges[*].DayofMonth ALL == %s
FILTER DATE_ADD(p.edges[0].ArrTimeUTC, 20, 'minutes') < p.edges[1].DepTimeUTC LET flightTime = DATE_DIFF(p.edges[0].DepTimeUTC, p.edges[1].ArrTimeUTC, 'i') SORT flightTime ASC
LIMIT 1
RETURN { flight: p, time: flightTime }'''
        query = query % (origin, target, day, month)
        print(query)
        result = self.client.db('_system').aql.execute(query)
        collection = list()
        for student in result:
            collection.append(student)
        return collection

    def get_all_stops(self):
        query = '''FOR stop IN stops SORT stop.name RETURN {name:stop.name, id:stop._key} '''
        query_result = self.client.db('_system').aql.execute(query)
        stops = list()
        for stop in query_result:
            stops.append(stop)
        return stops

    def get_stop_by_id(self, id):
        query = 'FOR stop IN stops FILTER stop._id == "{}" RETURN stop'
        query_result = self.client.db('_system').aql.execute(query.format(str(id)))
        return query_result
