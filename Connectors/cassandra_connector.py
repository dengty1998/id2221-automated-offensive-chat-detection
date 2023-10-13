from cassandra.cluster import Cluster


def init_cassandra_connection():
    '''
    Inits a cassandra session
    :return: cssaadnra cluster and session
    '''

    # Set the contact points for your Cassandra cluster
    contact_points = ['127.0.0.1']


    # Create a connection to your Cassandra cluster
    cluster = Cluster(contact_points=contact_points)
    session = cluster.connect()

    return cluster, session


def close_cassandra_connection(cluster, session):
    '''
    shut down cassandra clusters and session
    :param cluster: cassandra cluster
    :param session: cassandra session
    '''
    cluster.shutdown()
    session.shutdown()


def init_cassandra():

    '''
    Initialize cassandra set up
    '''

    cql_file_path = 'init_cassandra.cql'  # Replace with the path to your CQL file

    with open(cql_file_path, 'r') as cql_file:

        cql_statements = cql_file.read().split(';')
        cluster, session = init_cassandra_connection()

        for statement in cql_statements:
            if statement.strip():
                try:
                    session.execute(statement)
                except Exception as e:
                    print(f"Error inserting data: {str(e)}")

        close_cassandra_connection(cluster, session)


def check_password(username, password):
    '''

    :param username: username entered by user
    :param password: password entered by user
    :return: True if password matches, False if not
    '''

    cluster, session = init_cassandra_connection()
    query = f"SELECT password FROM users.accounts WHERE name = '{username}'"
    result = session.execute(query)


    login_success = False
    if result:
        if result[0].password == password:
            login_success = True

    close_cassandra_connection(cluster, session)

    return login_success


def check_account_status(username):

    '''

    :param username: username entered by user
    :return: True if account is flagged, False if not
    '''

    cluster, session = init_cassandra_connection()
    query = f"SELECT flagged FROM users.accounts WHERE name = '{username}'"
    result = session.execute(query)
    close_cassandra_connection(cluster, session)

    return result[0].flagged


def flag_account(username):
    '''
    flags user's account
    :param username: username entered by user
    '''
    cluster, session = init_cassandra_connection()
    query_1 = f"SELECT id FROM users.accounts WHERE name = '{username}'"
    result = session.execute(query_1)
    user_id = result[0].id
    query_2 = f"UPDATE users.accounts SET flagged = TRUE WHERE id = {user_id}"
    session.execute(query_2)
    close_cassandra_connection(cluster, session)





