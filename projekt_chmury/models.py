
from urllib.parse import urlparse, urlunparse

import os
import uuid

#neo4jrestclient
from neo4jrestclient.client import GraphDatabase

url = urlparse(os.environ.get("GRAPHENEDB_URL"))
url_without_auth = urlunparse((url.scheme, "{0}:{1}".format(url.hostname, url.port), url.path, None, None, None))

graph = GraphDatabase(url_without_auth, username = url.username, password = url.password)

def execute(query):
    return graph.query(query)

def list_all():
    query = "MATCH (p:Przystanek) RETURN (p)"
    return execute(query)

def get_autobus(nazwa1, nazwa2):
    query = "MATCH (start:Przystanek{nazwa: '" + nazwa1 + "'}), "
    query+= "(end:Przystanek {nazwa: '" + nazwa2 + "'}) "
    query+= "MATCH (start)-[p:POLACZONY]-(end) "
    query+= "RETURN p.numer AS numer"
    return execute(query)

class Przystanek:
    def __init__(self, nazwa):
        self.nazwa = nazwa

    def find(self):
        query = "MATCH (p:Przystanek {nazwa: '" + self.nazwa + "'}) RETURN p"
        result = execute(query)
        return ( result )

    def add(self, ulica, numer):
        if not self.find():
            query = "CREATE (p:Przystanek {nazwa:'" + self.nazwa + "', "
            query+= "ulica: '" + ulica + "', numer:'" + numer + "'})"
            execute(query)
            return True
        else:
            return False

    def add_rel(self, nazwa2, autobus, czas):
        p1 = self.find()
        p2 = Przystanek(nazwa2).find()

        if not p1 or not p2:
            return False

        query = "MATCH (p1:Przystanek), (p2:Przystanek) "
        query+= "WHERE p1.nazwa = '" + self.nazwa +"' "
        query+= "AND p2.nazwa = '" + nazwa2 +"' "
        query+= "CREATE (p1) - [r:POLACZONY{ numer: '" + autobus + "', czas: " + czas + "}]->(p2) "
        query+= "RETURN r"

        return execute(query)

    def patch(self, nazwa2):
        p1 = self.find()
        p2 = Przystanek(nazwa2).find()

        if not p1 or not p2:
            return False

        query = "MATCH (start:Przystanek{nazwa: '" + self.nazwa + "'}), "
        query+= "(end:Przystanek {nazwa: '" + nazwa2 + "'}) "
        query+= "CALL algo.shortestPath.stream(start, end, 'czas') "
        query+= "YIELD nodeId, cost "
        query+= "RETURN algo.asNode(nodeId).nazwa AS name, cost "

        res = execute(query)
        return res

    def modify(self, ulica, numer):
        query = "MATCH (n { nazwa: '" + self.nazwa + "' }) " 
        query+= "SET n.ulica = '" + ulica + "', "
        query+= "n.numer = '" + numer + "' "
        query+= "RETURN n"

        return execute(query)

    def delete(self):
        if not self.find():
            return False
        else:
            query = "MATCH (p:Przystanek {nazwa: '" + self.nazwa + "'}) DETACH DELETE p "
            execute(query) 
            return True

    def delete_rel(self, nazwa2):
        p1 = self.find()
        p2 = Przystanek(nazwa2).find()
        query_exists="MATCH (start:Przystanek{nazwa: '" + self.nazwa + "'}), "
        query_exists+= "(end:Przystanek {nazwa: '" + nazwa2 + "'}) "
        query_exists+= "RETURN EXISTS ((start)-[:POLACZONY]-(end))"

        if not p1 or not p2:
            return False
        elif not execute(query_exists):
            return False
        else:
            query = "MATCH (start:Przystanek{nazwa: '" + self.nazwa + "'})"
            query+= "-[r:POLACZONY]-"
            query+= "(end:Przystanek {nazwa: '" + nazwa2 + "'}) "
            query+= "DELETE r"

            execute(query)
            return True

    def list_all(self):
        query = " MATCH (p:Przystanek) RETURN (p) "
        return execute(query)
    