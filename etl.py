import configparser
import psycopg2
from sql_queries import copy_table_queries, insert_table_queries




def load_staging_tables(cur, conn):
    """
    Triggers the data extraction process from the json files to the staging tables.
                 
    Parameters:
        cur (psycopg2.cursor): database cursor object
        conn (psycopg2.connection): database connection object
        
    Returns:
        None
    """
    print("loading data from S3 to AWS Redshift tables...")
    try:
        for query in copy_table_queries:
            print('Executing query: {}'.format(query))
            cur.execute(query)
            conn.commit()
            print('{} executed'.format(query))

    except psycopg2.Error as e:
        print(e)




def insert_tables(cur, conn):
    """
    Triggers the data transformation and loading processes.
    
    Arguments:
        cur (psycopg2.cursor): database cursor object
        conn (psycopg2.connection): database connection object
        
    Returns:
        None
    """
    print("Inserting data from staging tables into fact and dimension tables...")
    try:
        for query in insert_table_queries:
            print('Executing query: {}'.format(query))
            cur.execute(query)
            conn.commit()
            print('{} executed'.format(query))

    except psycopg2.Error as e:
        print(e)




def main():
    """
    The main function connects to the database and provides the cursor, triggers the functions staging_tables and insert_tables.
    
    Arguments:
        None
        
    Returns:
        None
    """
    print("Establishing connection to AWS Redshift.")
    try:
        config = configparser.ConfigParser()
        config.read('dwh.cfg')

        conn = psycopg2.connect("host={} dbname={} user={} password={} port={}".format(*config['CLUSTER'].values()))
        cur = conn.cursor()

        print("AWS Redshift connection established.")

        load_staging_tables(cur, conn)
        insert_tables(cur, conn)

        conn.close()

    except psycopg2.Error as e:
        print(e)
    



if __name__ == "__main__":
    main()