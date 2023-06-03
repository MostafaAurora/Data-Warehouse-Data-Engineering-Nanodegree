import configparser
import psycopg2
from sql_queries import create_table_queries, drop_table_queries


def drop_tables(cur, conn):
    """
    Drops the tables defined in the 'drop_table_queries' array.
    
    Arguments:
        cur (psycopg2.cursor): database cursor object
        conn (psycopg2.connection): database connection object
        
    Returns:
        None
    """
    print("Dropping tables")
    try:
        for query in drop_table_queries:
            cur.execute(query)
            conn.commit()
            print(query)

    except psycopg2.Error as e:
        print(e)




def create_tables(cur, conn):
    """
    Creates the tables defined in the 'create_table_queries' array
    
    Arguments:
        cur (psycopg2.cursor): database cursor object
        conn (psycopg2.connection): database connection object
        
    Returns:
        None
    """
    print("Creating tables")
    try:
        for query in create_table_queries:
            cur.execute(query)
            conn.commit()
            print(query)

    except psycopg2.Error as e:
        print(e)




def main():
    """
    The main function connects to the database and provides the cursor, triggers table drop and creation.
    
    Arguments:
        None
        
    Returns:
        None
    """
    try:
        print("Reading connection parameters")
        config = configparser.ConfigParser()
        config.read('dwh.cfg')

        print("Establishing connection to AWS Redshift.")
        conn = psycopg2.connect("host={} dbname={} user={} password={} port={}".format(*config['CLUSTER'].values()))
        cur = conn.cursor()
        print("AWS Redshift connection established.")

        drop_tables(cur, conn)
        create_tables(cur, conn)

        conn.close()

    except psycopg2.Error as e:
        print(e)




if __name__ == "__main__":
    main()