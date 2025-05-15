#!/usr/bin/python3
seed = __import__('seed')


def stream_user_ages():
    """Stream the user ages one by one."""
    connection = seed.connect_to_prodev()
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT age from user_data")
    for row in cursor:
        yield row
    
def lazy_aggregate():
    """Gets the average age of users in db"""    
    total_age = 0
    count = 0
    for user in stream_user_ages():
        total_age += user.get("age")
        count += 1
    print(f"Average age of users: {total_age / count}")


lazy_aggregate()