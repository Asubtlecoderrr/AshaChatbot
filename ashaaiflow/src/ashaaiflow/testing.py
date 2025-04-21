# import os
# import sys
# sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../')))

# from shared.user_context import user_id_var
# user_id_var.set(3)
# user_id = user_id_var.get()
# import sqlite3
# from main import CareerState

# print(CareerState)
# def get_user_data(user_id):
#     db_path = "backend/database/users.db"
#     connection = sqlite3.connect(db_path)
#     cursor = connection.cursor()

#     try:
#         query = "SELECT * FROM User WHERE id = ?"
#         cursor.execute(query, (user_id,))
#         user_data = cursor.fetchone()
#         print(user_data)
#         return user_data

#     except sqlite3.Error as e:
#         print(f"Database error: {e}")
#         return None
#     finally:
#         connection.close()
        
# def set_user_data(user_id, name, email):
#     db_path = "backend/database/users.db"
#     connection = sqlite3.connect(db_path)
#     cursor = connection.cursor()

#     try:
#         # Insert or replace user data (update if exists, insert if not)
#         query = """
#         INSERT INTO User (id, name, email)
#         VALUES (?, ?, ?)
#         ON CONFLICT(id) DO UPDATE SET
#             name = excluded.name,
#             email = excluded.email;
#         """
#         cursor.execute(query, (user_id, name, email))
#         connection.commit()
#         print("User data saved successfully.")
#         return True

#     except sqlite3.Error as e:
#         print(f"Database error: {e}")
#         return False

#     finally:
#         connection.close()


# # get_user_data(user_id)