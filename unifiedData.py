import sqlite3
import os

script_dir = os.path.dirname(os.path.abspath(__file__))

db_path = os.path.join(script_dir, 'db_path.db')

class DataStream:
    def __init__(self, datastream_id, name, department, process_time, status, last_update, poc_name, poc_email, poc_phone):
        self.__datastream_id = datastream_id
        self.__name = name
        self.__department = department
        self.__status = status
        self.__process_time = process_time
        self.__last_update = last_update
        self.__poc_name = poc_name
        self.__poc_email = poc_email
        self.__poc_phone = poc_phone

    @property
    def name(self):
        return self.__name
    
    @name.setter
    def name(self, value):
        self.__name = value

    @property
    def status(self):
        return self.__status
    
    @status.setter
    def status(self, value):
        self.__status = value
    
    @property
    def last_update(self):
        return self.__last_update
    
    @last_update.setter
    def last_update(self, value):
        self.__last_update = value

    @property
    def department(self):
        return self.__department
    
    @department.setter
    def department(self, value):
        self.__department = value

    @property
    def process_time(self):
        return self.__process_time
    
    @process_time.setter
    def process_time(self, value):
        self.__process_time = value

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
    def poc_phone(self, value):
        self.__poc_phone = value
    
    @classmethod
    def delDataStream(cls, datastream_id):
        conn = None
        conn = sqlite3.connect( db_path)
        sql='DELETE FROM datastreams WHERE datastream_id=?'
        cur = conn.cursor()
        cur.execute(sql, (datastream_id,))
        conn.commit()
        conn.close()

    @classmethod
    def addDataStream(cls, datastream_id, name, department, process_time, status, last_update, poc_name, poc_email, poc_phone):
        conn = None
        conn = sqlite3.connect( db_path)
        sql='INSERT INTO datastreams ( datastream_id, name, department, process_time, status, last_update, poc_name, poc_email, poc_phone) values (?,?,?,?,?,?,?,?,?)'
        cur = conn.cursor()
        cur.execute(sql, ( datastream_id, name, department, process_time, status, last_update, poc_name, poc_email, poc_phone,))
        conn.commit()
        if conn:
            conn.close()

    @classmethod
    def updateDataStream(cls, datastream_id, name, department, process_time, status, last_update, poc_name, poc_email, poc_phone):
        conn = sqlite3.connect(db_path)
        sql='UPDATE machines SET name=?, department=?, process_time=?, status=?, last_update=?, poc_name=?, poc_email=?, poc_phone=? WHERE datastream_id = ?'
        cur = conn.cursor()
        cur.execute(sql, ( name, department, process_time, status, last_update, poc_name, poc_email, poc_phone,datastream_id,))
        conn.commit()
        conn.close()

    @classmethod
    def getAllDataStreams(cls):
        conn = sqlite3.connect(db_path)
        cursorObj = conn.cursor()
        cursorObj.execute("SELECT datastream_id, name, department, process_time, status, last_update, poc_name, poc_email, poc_phone FROM datastreams ORDER BY CASE status WHEN 'Online' THEN 1 WHEN 'Delayed/Errors' THEN 2 WHEN 'Offline' THEN 3 WHEN 'Unknown' THEN 4 ELSE 5 END;")
        allRows = cursorObj.fetchall()
        ListOfDictionaries = []
        for row in allRows:
            m = {"datastream_id": row[0], 'name':row[1],"department":row[2], 'process_time': row[3], 'status':row[4], 'last_update':row[5],'poc_name':row[6],'poc_email':row[7],'poc_phone':row[8]}
            ListOfDictionaries.append(m)
        if conn:
            conn.close()
        return ListOfDictionaries

    @classmethod
    def getDataStream(cls, datastream_id):
        ds = DataStream.getAllDataStreams()
        for d in ds:
            if d['datastream_id'] == datastream_id:
                return d
    
    @classmethod
    def InsertSampleData(cls):
        conn = sqlite3.connect(db_path)
        cur = conn.cursor()
        sample_data = [('DS001', 'Order Processing', 'Sales', '00:30', 'Online', '2024-12-13 09:50:00', 'John Doe', 'john.doe@example.com', '555-1234'),
    ('DS002', 'Inventory Management', 'Operations', '01:30', 'Delayed/Errors', '2024-12-12 17:30:00', 'Jane Smith', 'jane.smith@example.com', '555-2345'),
    ('DS003', 'Customer Feedback', 'Marketing', '01:30', 'Online', '2024-12-13 11:45:00', 'Emily Johnson', 'emily.johnson@example.com', '555-3456'),
    ('DS004', 'Shipping Logistics', 'Logistics', '01:30', 'Online', '2024-12-13 12:55:00', 'Michael Brown', 'michael.brown@example.com', '555-4567'),
    ('DS005', 'Employee Onboarding', 'HR', '01:30', 'Offline', '2024-12-11 16:00:00', 'Sarah Williams', 'sarah.williams@example.com', '555-5678'),
    ('DS006', 'Product Returns', 'Customer Service', '01:30', 'Online', '2024-12-13 14:50:00', 'David Lee', 'david.lee@example.com', '555-6789'),
    ('DS007', 'Quality Assurance', 'Engineering', '01:30', 'Offline', '2024-12-12 15:30:00', 'Olivia Harris', 'olivia.harris@example.com', '555-7890'),
    ('DS008', 'Supplier Communication', 'Procurement', '01:30', 'Online', '2024-12-13 16:45:00', 'James Clark', 'james.clark@example.com', '555-8901'),
    ('DS009', 'Financial Reporting', 'Finance', '01:30', 'Offline', '2024-12-10 14:00:00', 'Sophia Rodriguez', 'sophia.rodriguez@example.com', '555-9012'),
    ('DS010', 'Project Management', 'IT', '01:30', 'Online', '2024-12-13 18:50:00', 'Liam Martinez', 'liam.martinez@example.com', '555-0123'),
    ('DS011', 'Compliance Auditing', 'Legal', '01:30', 'Delayed/Errors', '2024-12-12 13:45:00', 'Lucas Hernandez', 'lucas.hernandez@example.com', '555-1235'),
    ('DS012', 'Sales Forecasting', 'Sales', '01:30', 'Online', '2024-12-13 20:30:00', 'Charlotte Lewis', 'charlotte.lewis@example.com', '555-2346'),
    ('DS013', 'IT Support', 'IT', '01:30', 'Offline', '2024-12-12 17:00:00', 'Benjamin Walker', 'benjamin.walker@example.com', '555-3457'),
    ('DS014', 'Marketing Campaign', 'Marketing', '01:30', 'Online', '2024-12-13 22:55:00', 'Amelia Young', 'amelia.young@example.com', '555-4568'),
    ('DS015', 'Vendor Management', 'Procurement', '01:30', 'Offline', '2024-12-13 18:30:00', 'Mason King', 'mason.king@example.com', '555-5679'),
    ('DS016', 'Legal Contracts', 'Legal', '01:30', 'Online', '2024-12-13 23:50:00', 'Harper Scott', 'harper.scott@example.com', '555-6780'),
    ('DS017', 'Employee Benefits', 'HR', '01:30', 'Delayed/Errors', '2024-12-12 19:15:00', 'Ella Green', 'ella.green@example.com', '555-7891'),
    ('DS018', 'Data Analytics', 'IT', '01:30', 'Online', '2024-12-13 23:30:00', 'Aiden Adams', 'aiden.adams@example.com', '555-8902'),
    ('DS019', 'Customer Support', 'Customer Service', '01:30', 'Offline', '2024-12-12 20:45:00', 'Mia Carter', 'mia.carter@example.com', '555-9013'),
    ('DS020', 'Event Planning', 'Marketing', '01:30', 'Online', '2024-12-14 04:50:00', 'Elijah Baker', 'elijah.baker@example.com', '555-0124')]
        cur.executemany('''INSERT INTO datastreams (datastream_id, name, department, process_time, status, last_update, poc_name, poc_email, poc_phone) VALUES (?, ?, ?, ?,?,?,?,?,?)''', sample_data)
        conn.commit()
        conn.close()

    @classmethod
    def createSampleTable(cls):
        conn = sqlite3.connect(db_path)
        cur = conn.cursor()
        cur.execute('''CREATE TABLE datastreams (datastream_id TEXT PRIMARY KEY,name TEXT NOT NULL,department TEXT NOT NULL,process_time TEXT NOT NULL,status TEXT NOT NULL,last_update TEXT NOT NULL,poc_name TEXT NOT NULL,poc_email TEXT NOT NULL,poc_phone TEXT NOT NULL);''')
        conn.commit()
        conn.close()


if __name__ == '__main__':
    DataStream.createSampleTable()
    DataStream.InsertSampleData()
    print(DataStream.getAllDataStreams())