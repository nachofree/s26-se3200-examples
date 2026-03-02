
import json
import sqlite3

class RealDB:
    def __init__(self, filename):
        self.filename = filename
        self.conn = sqlite3.connect("database.db")
        self.cursor = self.conn.cursor()
    

    def saveRecord(self, record):
        print(record)
        data = [record["name"], record['rating'], record['price']]
        self.cursor.execute("INSERT INTO guitars (name, rating, price) VALUES (?, ?, ?) ", data)
        self.conn.commit()
      
    def dict_factory(self, cursor, row):
        fields = []
        # Extract column names from cursor description
        for column in cursor.description:
            fields.append(column[0])

        # Create a dictionary where keys are column names and values are row values
        result_dict = {}
        for i in range(len(fields)):
            result_dict[fields[i]] = row[i]

        return result_dict

    def readAllRecords(self):
        self.cursor.execute("SELECT * FROM guitars")
        guitars = self.cursor.fetchall()
        all = []
        for row in guitars:
           d = self.dict_factory(self.cursor, row)
           all.append(d)
        print("Alld the rows are", all)
        return all



