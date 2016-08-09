import connector
import pandas as pd

class Query(object):
    def __init__(self, conn, query):
        self.conn = conn
        self.query = query
        self.query_file_name = '_'.join(query.split()) + '.csv'
        self.cursor = conn.cursor()

        # self.list_of_lists
        # self.df

        # hardcoded data folder location, dye to shared file structure
        self.csv_file_path = '../data/' + self.query_file_name

        self._run_query()

    def _run_query(self):
        try:
            c = self.cursor.execute(self.query)
        except Exception as e:
            print ("Error in query,", e)

    def get_query_cursor(self):
        return self.cursor

    def get_query_list(self):
        return self.cursor.fetchall()

    def get_query_dataframe(self):
        return pd.DataFrame(self.get_query_list(), columns=self.cursor.description)

    def write_df_to_csv(self):
        self.get_query_dataframe().to_csv(self.csv_file_path)


def main():

    dbconnection = connector.ConnectDB()
    conn = dbconnection.get_connection()
    query = Query(conn, 'select * from feed_items limit 10;')
    query_cursor = query.get_query_cursor()
    query_list =    query.get_query_list()
    query_df = query.get_query_dataframe()
    query.write_df_to_csv()

    print (query_list)

main()

