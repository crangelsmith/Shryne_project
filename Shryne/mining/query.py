import connector

class Query(object):
    def __init__(self, conn, query):
        self.conn = conn
        self.query = query
        self.cursor = conn.cursor()

        # self.list_of_lists
        # self.df
        # self.csv_file_path

        self._run_query()

    def _run_query(self):
        try:
            c = self.cursor.execute(self.query)
        except Exception as e:
            print ("Error in query,", e)

    def get_query_list(self):
        return self.cursor

    def get_dataframe(self):
        pass

    def dump_to_csv(self):
        pass


def main():


    print("we're in main")

    dbconnection = connector.ConnectDB("/home/sophie/.ssh/id_rsa.pub")
    print("we have a connection")

    conn = dbconnection.get_connection()
    print("we should definitely have a connection")

    query_test = Query(conn, 'select * from feed_items limit 10;')
    result = query_test.get_query_list()

    print (result.fetchall())

    # # create a cursor
    # c = conn.cursor()
    # print("cursor")
    #
    # # execute a command
    # c.execute("SELECT * FROM feed_items LIMIT 10")
    # print("command executed")
    #
    # result = [row for row in c.fetchall()]
    # print("results are in result object")
    #
    # print(result)
    #
    # dbconnection.close_connection()
    #
    # print("done")


main()

