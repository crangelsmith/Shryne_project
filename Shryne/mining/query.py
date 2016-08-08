#from connector import ConnectDB


class Query(object):
    def __init__(self,conn,query):
        self.conn=conn
        self.query=query
        self.cursor=conn.cursor()
        self.output=[]

        self._run_query()


    def _run_query(self):
        try:
            c = self.cursor.execute(self.query)
            self.output=c
        except Exception as e:
            print ("Error in query,", e)

    def get_query_list(self):
        return self.output

# def main():
#
#     print("we're in main")
#
#     dbconnection = ConnectDB("/Users/Camila/.ssh/ssh_key.pub")
#     print("we have a connection")
#
#     conn = dbconnection.get_connection()
#     print("we should definitely have a connection")
#
#     # create a cursor
#     c = conn.cursor()
#     print("cursor")
#
#     # execute a command
#     c.execute("SELECT * FROM feed_items LIMIT 10")
#     print("command executed")
#
#     result = [row for row in c.fetchall()]
#     print("results are in result object")
#
#     print(result)
#
#     dbconnection.close_connection()
#
#     print("done")
#
#
# main()
#
