import MySQLdb


class Database:

    def __init__(self):

        self.con = MySQLdb.connect("xxxx", "xxxx", "xxxx", "xxxx")
        self.cursor = self.con.cursor()

    def connect_to_db(self):
        self.cursor.execute("CREATE TABLE IF NOT EXISTS estates (id INTEGER PRIMARY KEY NOT NULL AUTO_INCREMENT, "
                            "location TEXT, type_estate TEXT, price REAL, size INTEGER, price_per_kvm REAL, "
                            "bedroom INTEGER, date DATE, description TEXT)")

    def insert_to_db(self, location, type_estate, price, size, price_per_kvm, bedroom, date, description):
        self.cursor.execute("INSERT INTO estates VALUES (NULL, %s,%s,%s,%s,%s,%s,%s,%s)"
                            , (location, type_estate, price, size, price_per_kvm, bedroom, date, description))
        self.con.commit()

    def view_db(self):
        self.cursor.execute("SELECT * FROM estates")
        rows = self.cursor.fetchall()
        return rows

    def search_in_db(self, location="", type_estate="", price="", size="", price_per_kvm="", bedroom="",
                     date='0000-00-00'):
        self.cursor.execute("SELECT * FROM estates WHERE location=%s OR type_estate=s% OR price=%s OR "
                            "size=%s OR price_per_kvm=%s OR bedroom=%s OR date=%s",
                            (location, type_estate, price, size, price_per_kvm, bedroom, date))
        rows = self.cursor.fetchall()
        return rows

    def delete_from_db(self, id="", location="", type_estate="", price="", size="", price_per_kvm="", bedroom="",
                       date='0000-00-00'):
        self.cursor.execute("DELETE FROM estates WHERE id=%s OR location=%s OR type_estate=%s OR price=%s OR "
                            "size=%s OR price_per_kvm=%s OR bedroom=%s OR date=%s",
                            (id, location, type_estate, price, size, price_per_kvm, bedroom, date))
        self.con.commit()

    def check_if_exists(self, description):
        self.cursor.execute("SELECT * FROM estates where description=%s", (description,))
        rows = self.cursor.fetchone()
        return rows

    def send_commmand(self, command):
        self.cursor.execute(command)
        rows = self.cursor.fetchall()
        return rows

    def show_columns(self):
        self.cursor.execute("SHOW FIELDS FROM estates")
        rows = self.cursor.fetchall()
        columns_list = list(rows)
        columns_in_db = []
        for item in columns_list:
            columns_in_db.append(item[0])
        return columns_in_db

    def get_prices(self):
        self.cursor.execute("SELECT price FROM estates")
        rows = self.cursor.fetchall()
        return rows

    def get_prices_per_kvm(self):
        self.cursor.execute("SELECT price_per_kvm FROM estates ")
        rows = self.cursor.fetchall()
        return rows

    def close_db(self):
        self.con.close()
