import ast

from neo4j.v1 import GraphDatabase, basic_auth

class EntityCreator:

    created = set()

    def is_expr_context(self, node):
        return node.__class__.__name__ in ('Load', 'Store', 'Del')

    def create_node(self, node):
        nid = id(node)
        if nid in self.created:
            return
        if self.is_expr_context(node):
            return
        self.tx.run("create (n:Node {nid:{nid}, class:{cls}})", {
            "nid" : nid,
            "cls" : node.__class__.__name__
        })
        self.created.add(nid)

    def create_relationship(self, from_, to):
        self.create_node(from_)
        self.create_node(to)
        fid = id(from_)
        tid = id(to)
        if (fid, tid) in self.created:
            return
        if self.is_expr_context(to):
            self.tx.run("""match (a:Node)
                where a.nid = {nid}
                set a.ctx = '{ctx}'
            """.format(nid=fid, ctx=to.__class__.__name__))
        else:
            self.tx.run("""match (a:Node), (b:Node)
                where a.nid = {} and b.nid = {}
                create (a)-[:Child]->(b)
            """.format(fid, tid))
        self.created.add((fid, tid))


def store(tree):

    password = '123456'
    driver = GraphDatabase.driver('bolt://localhost', auth=basic_auth('neo4j', password))
    session = driver.session()

    creator = EntityCreator()   

    with session.begin_transaction() as tx:

        creator.tx = tx

        for node in ast.walk(tree):
            creator.create_node(node)

        for node in ast.walk(tree):
            for child in ast.iter_child_nodes(node):
                creator.create_relationship(node, child)

        # for ctx in ('Load', 'Store', 'Del'):
        #     tx.run("""match (n:Node)<-[r]-(m:Node)
        #         where n.class = '{ctx}'
        #         delete r
        #         set m.ctx = '{ctx}'
        #     """.format(ctx=ctx))
             

        tx.success = True

    session.close()