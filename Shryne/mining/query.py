import pandas as pd

class Query(object):
    def __init__(self, conn, query):
        self.conn = conn
        self.query = query
        self.query_file_name = '_'.join(query.replace('*', 'ALL').replace(';', '').split()) + '.csv'
        self.cursor = conn.cursor()

        # hardcoded data folder location, dye to shared file structure
        self.csv_file_path = '../data/' + self.query_file_name

        # run the query then assign the cursor information into
        # a list and generate query dataframe
        self._run_query()
        self.query_list = self.cursor.fetchall()
        self.query_df = pd.DataFrame(self.query_list, columns=[k[0] for k in self.cursor.description])

    def _run_query(self):
        try:
            self.cursor.execute(self.query)
        except Exception as e:
            print ("Error in query,", e)

    def get_query_list(self):
        return self.query_list

    def get_query_dataframe(self):
        return self.query_df

    def write_df_to_csv(self):
        self.query_df.to_csv(self.csv_file_path)


# def main():
#
#     import connector
#
#     q = "SELECT DISTINCT userid, first_name, last_name FROM fakes_names WHERE first_name NOT IN (\'Connor\', \'Danielle\', \'Garrett\',\'Anne\',\'Ethan\',\'Bethany\',\'Cody\');"
#
#     dbconnection = connector.ConnectDB()
#     conn = dbconnection.get_connection()
#     query = Query(conn, q)
#     query_list = query.get_query_list()
#     query_df = query.get_query_dataframe()
#     query.write_df_to_csv()
#
# main()

