import sqlite3
from passlib.hash import bcrypt

def dict_factory(cursor, row):
    fields = []
    # Extract column names from cursor description
    for column in cursor.description:
        fields.append(column[0])

    # Create a dictionary where keys are column names and values are row values
    result_dict = {}
    for i in range(len(fields)):
        result_dict[fields[i]] = row[i]

    return result_dict


class DB:
    def __init__(self, dbfilename):
        self.dbfilename = dbfilename
        self.connection = sqlite3.connect(dbfilename)
        self.cursor = self.connection.cursor()
        self._ensure_guitars_table()

    def _ensure_guitars_table(self):
        self.cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS guitars (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                price REAL NOT NULL,
                rating INTEGER NOT NULL
            );
            """
        )
        self.connection.commit()

    def readAllRecords(self):
        self.cursor.execute("SELECT * FROM guitars")
        rows = self.cursor.fetchall()
        all = []
        for row in rows:
            d = dict_factory(self.cursor, row)
            all.append(d)
        print("the rows are", all)
        return all
    
    def editRecord(self,id, d):
        data = [d["name"], d["price"],d["rating"], id]
        self.cursor.execute("UPDATE guitars SET name=?, price=?, rating=? WHERE id = ?;", data)
        self.connection.commit()
    
    def deleteRecord(self, id):
        self.cursor.execute("DELETE FROM guitars WHERE id = ?;", [id])
        self.connection.commit()
        
    
    def saveRecord(self, record):
        data = [record["name"], record["price"], record["rating"]]
        self.cursor.execute("INSERT INTO guitars (name,  price, rating) VALUES (?, ?, ?);", data)
        self.connection.commit()



    def close(self):
        self.connection.close()


class User:
    def __init__(self, dbfilename):
        self.dbfilename = dbfilename
        self.connection = sqlite3.connect(dbfilename)
        self.cursor = self.connection.cursor()
        self._ensure_users_table()

    def _ensure_users_table(self):
        self.cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                email TEXT NOT NULL UNIQUE,
                password_hash TEXT NOT NULL
            );
            """
        )
        self.connection.commit()

    def userExists(self, email):
        self.cursor.execute("SELECT 1 FROM users WHERE email = ? LIMIT 1;", [email])
        return self.cursor.fetchone() is not None

    def saveUser(self, email, password):
        password_hash = bcrypt.hash(password)
        self.cursor.execute(
            "INSERT INTO users (email, password_hash) VALUES (?, ?);",
            [email, password_hash]
        )
        self.connection.commit()

    def close(self):
        self.connection.close()


if __name__ == "__main__":
    db = DB("guitars.db")
    db.readAllRecords()
    db.saveRecord({"name": "sample", "price":99.99, "rating": 4})
    db.readAllRecords()
    db.close()