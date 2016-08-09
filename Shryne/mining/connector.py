import psycopg2
from sshtunnel import SSHTunnelForwarder


class ConnectDB(object):
    def __init__(self, path_to_private_key):
        self.port = 5432
        self.path_to_private_key = path_to_private_key
        self.remote_bind_address = ('localhost', 5432)
        self.local_bind_address = ('localhost', 5432)
        self.user_name = 'analytics'
        self.dbname = 'dreikanter_production'
        self.remote_host = 'dreikanter.production.devguru.co'
        self.remote_port = 22
        self.conn = None
        self.server = None
        self._make_connection()

    def _make_connection(self):
        '''
        Creates a connection to a predifined Postgresql database
        '''
        self.server = SSHTunnelForwarder((self.remote_host, self.remote_port),
                                    ssh_private_key=self.path_to_private_key,
                                    ssh_username=self.user_name,
                                    local_bind_address=self.local_bind_address,
                                    remote_bind_address=self.remote_bind_address)

        self.server.start()
        params = {
            'database': 'dreikanter_production',
            'user': 'analytics',
            'host': 'localhost',
            'port': 5432
        }
        conn = psycopg2.connect(**params)

        self.conn = conn

    def get_connection(self):
        return self.conn

    def close_connection(self):
        self.conn.close()
        self.server.stop()


def main():
     '''
     Quick main script to test out whether or not
     we can connect to the database
     :return: None
     '''

     dbconnection = ConnectDB("/home/sophie/.ssh/id_rsa.pub")
     conn = dbconnection.get_connection()
     c = conn.cursor()
     c.execute("SELECT * FROM feed_items LIMIT 1")
     result = [row for row in c.fetchall()]
     print(result)
     dbconnection.close_connection()

main()
