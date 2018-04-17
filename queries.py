bus_line_route_query = '''select distinct ?geo_linea where {
?uri a om:AutobusUrbano .
?uri om:lineaBus ?linea .
?linea gtfs:longName ?nombre .
filter regex("%s", ?nombre) .
?ruta gtfs:route ?linea .
?ruta schema:line ?geo_linea .
}
LIMIT 1'''