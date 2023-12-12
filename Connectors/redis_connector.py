import json

import redis


def redis_connection():
    r = redis.Redis(host='localhost', port=6379, decode_responses=True)
    return r


def push_json(key, json_data):
    r = redis_connection()
    r.lpush(key, json_data)
    r.expire("chatlogs", 3600)


def return_parsed_data():
    r = redis_connection()
    json_data_list = r.lrange("chatlogs", 0, -1)
    parsed_data_list = [json.loads(data) for data in json_data_list]
    return parsed_data_list

# Print the parsed data
# for data in parsed_data_list:
#     print(data)
