from neo4j import GraphDatabase


class LoadGraphData:
    def __init__(self, username, password, uri):
        self.username = username
        self.password = password
        self.uri = uri
        self.driver = GraphDatabase.driver(
            self.uri, auth=(self.username, self.password)
        )

    def create(self, query):
        with self.driver.session() as graphDB_Session:
            return graphDB_Session.run(query)

    def set_max_nodes(self, number):
        query = f":config initialNodeDisplay: {number}"
        with self.driver.session() as graphDB_Session:
            return graphDB_Session.run(query)

    def delete_graph(self):
        delete = "MATCH (n) DETACH DELETE n"
        with self.driver.session() as graphDB_Session:
            graphDB_Session.run(delete)

    @staticmethod
    def do_cypher_tx(tx, cypher):
        result = tx.run(cypher)
        values = []
        for record in result:
            values.append(record.values())
        return values

    def work_with_data(self, query):
        with self.driver.session() as session:
            values = session.read_transaction(self.do_cypher_tx, query)
        return values
