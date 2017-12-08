import MySQLdb


class Database:
    def __init__(self):
        try:
            self.connection = MySQLdb.connect(host="dbinstance.cxhzpvafprvi.eu-west-2.rds.amazonaws.com",
                                              user="username",
                                              passwd="password",
                                              db="WhoIsWho_Unleashed4",
                                              port=1433)
        except MySQLdb.Error as e:
            print(e)

    def check_connection(self):
        self.cursor = self.connection.cursor()
        self.cursor.execute("SELECT VERSION()")
        row = self.cursor.fetchone()
        print("Connected to server:", row[0])

    def reset_and_delete(self):
        self.cursor = self.connection.cursor()
        sql_command = "DELETE FROM employee"  # reset auto incrementing id
        self.cursor.execute(sql_command)
        self.connection.commit()
        self.cursor.close()
        print("Deleting all entries")

        self.cursor = self.connection.cursor()
        sql_command = "ALTER TABLE employee AUTO_INCREMENT = 1"  # reset auto incrementing id
        self.cursor.execute(sql_command)
        self.connection.commit()
        self.cursor.close()
        print("Employee id set to 1")

    def add_user(self, habitat_id, naam, title, before, after):
        self.cursor = self.connection.cursor()
        format_str = """INSERT INTO employee (habitat_id, first_name, job_title, picture_before, picture_after)
                        VALUES ('{habitat}','{naam}', '{title}', '{before}', '{after}');"""
        sql_command = format_str.format(habitat=int(habitat_id), naam=naam, title=title, before=before, after=after)
        self.cursor.execute(sql_command)
        self.connection.commit()
        self.cursor.close()
        print("Successful Commit >> " + sql_command)

    def count_employees(self):
        try:
            self.cursor = self.connection.cursor()
            sql = "SELECT COUNT(*) FROM employee"
            result = self.cursor.execute(sql)
            number_of_people = self.cursor.fetchone()[0]
            print("Number of employees in DB: " + str(number_of_people))
            self.cursor.close()

        except MySQLdb.Error as e:
            print(e)
        except:
            print("count_employees >> Unknown error occurred")

    def close_connection(self):
        self.connection.close()
