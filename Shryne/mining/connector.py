import psycopg2
from sshtunnel import SSHTunnelForwarder

class ConnectDB(object):

    def __init__(self, path_to_private_key):
        self.port=5432
        self.path_to_private_key=path_to_private_key
        self.remote_bind_address=('localhost', 5432)
        self.local_bind_address=('localhost', 5432)
        self.user_name='analytics'
        self.dbname='dreikanter_production'
        self.remote_host='dreikanter.production.devguru.co'
        self.remote_port=22
        self.conn=None

        self._make_connection()

    def _make_connection(self):

        try:
            with SSHTunnelForwarder((self.remote_host, self.remote_port),
                                    ssh_private_key = self.path_to_private_key,
                                    ssh_username = self.user_name,
                                    local_bind_address = self.local_bind_address,
                                    remote_bind_address = self.remote_bind_address):
                #params = {
                 #   'database': self.dbname,
                 #   'user': self.user_name,
                 #   'host': self.remote_host,
                 #   'port': self.port
                #}
                params = {
                    'database': 'dreikanter_production',
                    'user': 'analytics',
                    'host': 'localhost',
                    'port': 5432
                }
                conn = psycopg2.connect(**params)


                self.conn = conn
        except Exception as e:
            print("failed with Error",e)

    def get_connection(self):
        return self.conn

    def close_connection(self):
        self.conn.close()

def main():

    print("we're in main")

    dbconnection = ConnectDB("/home/sophie/.ssh/id_rsa.pub")
    print("we have a connection")

    conn = dbconnection.get_connection()
    print("we should definitely have a connection")

    # create a cursor
    c = conn.cursor()
    print("cursor")

    # execute a command
    c.execute("SELECT * FROM feed_items LIMIT 1")
    print("command executed")

    result = [row for row in c.fetchall()]
    print("results are in result object")

    print(result)

    dbconnection.close_connection()

main()
