import sqlite3
import os

script_dir = os.path.dirname(os.path.abspath(__file__))

db_path = os.path.join(script_dir, 'db_path.db')

class Dealer:
    def __init__(self, dealer_id, name, poc_name, poc_email, poc_phone, address):
        self.__dealer_id = dealer_id
        self.__name = name
        self.__poc_name = poc_name
        self.__poc_email = poc_email
        self.__poc_phone = poc_phone
        self.__address = address

   
    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, value):
        self.__name = value

    @property
    def address(self):
        return self.__address

    @address.setter
    def address(self, value):
        self.__address = value

    @property
    def poc_name(self):
        return self.__poc_name

    @poc_name.setter
    def poc_name(self, value):
        self.__poc_name = value

    @property
    def poc_email(self):
        return self.__poc_email

    @poc_email.setter
    def poc_email(self, value):
        self.__poc_email = value
    
    @property
    def poc_phone(self):
        return self.__poc_phone

    @poc_phone.setter
    def profile_image(self, value):
        self.__poc_phone = value

    def __str__(self):
        return "Dealer Name: {} \n Address: {} \n Point of Contact Information:\n Name: {} \n Email: {} \n Phone Number: {} ".format(self.name, self.address, self.poc_name,self.poc_email,self.poc_phone)
    
    @classmethod
    def delDealer(cls, dealer_id):
        conn = None
        conn = sqlite3.connect( db_path)
        sql='DELETE FROM dealers WHERE dealer_id=?'
        cur = conn.cursor()
        cur.execute(sql, (dealer_id,))
        conn.commit()
        conn.close()

    @classmethod
    def addDealer(cls, dealer_id, name, poc_name, poc_email, poc_phone, address):
        conn = None
        conn = sqlite3.connect( db_path)
        sql='INSERT INTO dealers ( dealer_id, name, poc_name, poc_email, poc_phone, address) values (?,?,?,?,?,?)'
        cur = conn.cursor()
        cur.execute(sql, ( dealer_id, name, poc_name, poc_email, poc_phone,address,))
        conn.commit()
        if conn:
            conn.close()

    @classmethod
    def updateDealer(cls,dealer_id, name, poc_name, poc_email, poc_phone, address):
        conn = sqlite3.connect(db_path)
        sql='UPDATE dealers SET name=?, poc_name=?, poc_email=?, poc_phone=?, address=a? WHERE dealer_id = ?'
        cur = conn.cursor()
        cur.execute(sql, (name, poc_name, poc_email, poc_phone,address,dealer_id,))
        conn.commit()
        conn.close()


    @classmethod
    def getAllDealers(cls):
        conn = sqlite3.connect(db_path)
        cursorObj = conn.cursor()
        cursorObj.execute('SELECT dealer_id, name, poc_name, poc_email, poc_phone, address FROM dealers;')
        allRows = cursorObj.fetchall()
        ListOfDictionaries = []
        for row in allRows:
            m = {"dealer_id": row[0], 'name':row[1],"poc_name":row[2], 'poc_email': row[3], 'poc_phone':row[4], 'address':row[5]}
            ListOfDictionaries.append(m)
        if conn:
            conn.close()
        return ListOfDictionaries

    @classmethod
    def getDealer(cls, dealer_id):
        dealers = Dealer.getAllDealers()
        for dealer in dealers:
            if dealer['dealer_id'] == dealer_id:
                return dealer
    
    @classmethod
    def InsertSampleData(cls):
        conn = sqlite3.connect(db_path)
        cur = conn.cursor()
        sample_data = [('Best Auto Dealers', 'John Doe', 'johndoe@bestauto.com', '123-456-7890', '123 Main St, Springfield, IL 62701'),
('Elite Motors', 'Jane Smith', 'janesmith@elitemotors.com', '987-654-3210', '456 Elm St, Bloomington, IN 47408'),
('Premier Cars', 'Alice Johnson', 'alice.johnson@premiercars.com', '555-123-4567', '789 Oak St, Columbus, OH 43215'),
('Quality Wheels', 'Bob Brown', 'bob.brown@qualitywheels.com', '444-555-6666', '101 Pine Ave, Indianapolis, IN 46202'),
('Superior Rides', 'Emma Davis', 'emma.davis@superiorrides.com', '333-777-8888', '202 Maple Blvd, Louisville, KY 40202')]
        cur.executemany('''INSERT INTO dealers (name, poc_name, poc_email, poc_phone, address) VALUES (?, ?, ?, ?, ?)''', sample_data)
        conn.commit()
        conn.close()

    @classmethod
    def createDealerTable(cls):
        conn = sqlite3.connect(db_path)
        cur = conn.cursor()
        cur.execute('''CREATE TABLE dealers (dealer_id INTEGER PRIMARY KEY AUTOINCREMENT,name TEXT NOT NULL,poc_name TEXT NOT NULL,poc_email TEXT NOT NULL,poc_phone TEXT NOT NULL,address TEXT NOT NULL);''')
        conn.commit()
        conn.close()


if __name__ == '__main__':
    #Dealer.createDealerTable()
    #Dealer.InsertSampleData()
    print(Dealer.getAllDealers())