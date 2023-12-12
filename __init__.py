from Connectors.cassandra_connector import init_cassandra, check_password, check_account_status, flag_account
from Connectors.hdfs_connector import init_hdfs, append_json

# init_cassandra()


hdfs_path = ["/chatlogs"]
json_path = ["chatlogs.json"]

init_hdfs(hdfs_path, json_path)

# data = {'username': 'New Name', 'message': 'New Value', 'timestamp': 'New Time'}
# append_json('/chatlogs/chatlogs.json', data)







