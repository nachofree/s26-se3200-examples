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

if __name__ == "__main__":
    db = DB("guitars.db")
    db.readAllRecords()
    db.saveRecord({"name": "sample", "price":99.99, "rating": 4})
    db.readAllRecords()
    db.close()