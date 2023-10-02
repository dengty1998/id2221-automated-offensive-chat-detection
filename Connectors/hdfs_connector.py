from hdfs import InsecureClient



def init_hdfs_connection():
    '''
    Initialize hdfs connection
    :return: hdfs client
    '''
    # Initialize the HDFS client
    hdfs_host = 'localhost'
    hdfs_port = 9870 # Default HDFS port
    hdfs_user = 'minhao'

    client = InsecureClient(f'http://{hdfs_host}:{hdfs_port}', user=hdfs_user)

    return client


def upload_json(hdfs_path, json_path):
    '''
    upload json to specified hdfs path
    :param hdfs_path: hdfs path to store json file
    :param json_path: local json file path
    :return:
    '''
    client = init_hdfs_connection()
    # Upload the local JSON file to the specified HDFS path
    client.upload(hdfs_path, json_path, n_threads=1)

    print(f"JSON file '{json_path}' has been uploaded to HDFS path: {hdfs_path}")


def init_hdfs(hdfs_paths, json_paths):
    '''

    :param hdfs_paths: List of hdfs paths to store user logs
    :param json_paths: List of local json file for each user
    '''
    client = init_hdfs_connection()

    for hdfs_path, json_path in zip(hdfs_paths, json_paths):
        client.makedirs(hdfs_path)
        upload_json(f'{hdfs_path}/{json_path}', json_path)


'''
To be Decided
'''
def append_json(hdfs_path):

    pass

'''
To be decided
'''


def read_json(hdfs_path):

    pass






