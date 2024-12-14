#!/usr/bin/env python3
'''Objective: to use a generator to compute a memory-efficient aggregate function i.e average age for a large dataset'''

import mysql.connector

config = {
        'host': 'localhost',
        'user': 'root',
        'password': 'root',
        'database': 'ALX_prodev'
    }
        
def stream_user_ages():
    '''stream user ages from the database'''
    connection = mysql.connector.connect(**config)
    cursor = connection.cursor()
    cursor.execute("SELECT age FROM user_data;")
    while True:
        row = cursor.fetchone()
        if not row:
            break
        yield row[0]
    cursor.close()
    connection.close()

def compute_ages():
    '''compute the average age of users in the database'''
    ages = stream_user_ages()
    total = 0
    count = 0
    for age in ages:
        total += age
        count += 1
    return total / count if count > 0 else 0

if __name__ == '__main__':
    print('Average age of users:', compute_ages())
    

# import mysql.connector

# seed = __import__('seed')

# def stream_user_ages():
#     """
#         Generator that connects to the database and yields user ages one by one.
#         This uses one loop to iterate over all rows returned by the cursor.
#     """
#     conn = seed.connect_to_prodev()
#     cursor = conn.cursor()
#     cursor.execute("SELECT age FROM user_data;")  # No AVERAGE used, just selecting ages

#     # Loop 1: Yield each age
#     for (age,) in cursor:
#         yield age

#     cursor.close()
#     conn.close()

# def compute_age(): 
#     """
#     Uses the stream_user_ages generator to compute the average age.
#     This will sum and count the ages without storing them all in memory.
#     """
#     total_age = 0
#     count = 0
#     # Loop 2: Iterate over each age from the generator
#     for age in stream_user_ages():
#         total_age += age
#         count += 1
    
#     return total_age / count if count > 0 else 0

# # Example usage
# if __name__ == "__main__":
#     print(f"Average age of users: {compute_age()}")