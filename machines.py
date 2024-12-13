import sqlite3
import os

script_dir = os.path.dirname(os.path.abspath(__file__))

db_path = os.path.join(script_dir, 'db_path.db')

class Machine:
    def __init__(self, machine_id, name, type, status,notes,last_update):
        self.__machine_id = machine_id
        self.__name = name
        self.__type = type
        self.__status = status
        self.__notes = notes
        self.__last_update = last_update

    @property
    def name(self):
        return self.__name
    
    @name.setter
    def name(self, value):
        self.__name = value

    @property
    def type(self):
        return self.__type
    
    @type.setter
    def type(self, value):
        self.__type = value
    
    @property
    def status(self):
        return self.__status
    
    @status.setter
    def status(self, value):
        self.__status = value

    @property
    def notes(self):
        return self.__notes
    
    @notes.setter
    def notes(self, value):
        self.__notes = value
    
    @property
    def last_update(self):
        return self.__last_update
    
    @last_update.setter
    def last_update(self, value):
        self.__last_update = value
    
    @classmethod
    def delMachine(cls, machine_id):
        conn = None
        conn = sqlite3.connect( db_path)
        sql='DELETE FROM machines WHERE machine_id=?'
        cur = conn.cursor()
        cur.execute(sql, (machine_id,))
        conn.commit()
        conn.close()

    @classmethod
    def addMachine(cls,  machine_id, name, type, status,notes,last_update):
        conn = None
        conn = sqlite3.connect( db_path)
        sql='INSERT INTO machines (  machine_id, name, type, status,notes,last_update) values (?,?,?,?,?,?)'
        cur = conn.cursor()
        cur.execute(sql, (  machine_id, name, type, status,notes,last_update,))
        conn.commit()
        if conn:
            conn.close()

    @classmethod
    def updateMachine(cls, machine_id, name, type, status,notes,last_update):
        conn = sqlite3.connect(db_path)
        sql='UPDATE machines SET name=?, type=?, status=?,notes=?,last_update=? WHERE machine_id = ?'
        cur = conn.cursor()
        cur.execute(sql, ( name, type, status,notes,last_update,machine_id,))
        conn.commit()
        conn.close()

    @classmethod
    def getAllMachines(cls):
        conn = sqlite3.connect(db_path)
        cursorObj = conn.cursor()
        cursorObj.execute("SELECT machine_id, name, type, status, notes, last_update FROM machines ORDER BY CASE status WHEN 'Out of Service' THEN 1 WHEN 'Maintenance Required' THEN 2 WHEN 'Operational' THEN 3 WHEN 'Unknown' THEN 4 ELSE 5 END;")
        allRows = cursorObj.fetchall()
        ListOfDictionaries = []
        for row in allRows:
            m = {"machine_id": row[0], 'name':row[1],"type":row[2], 'status': row[3], 'notes':row[4], 'last_update':row[5]}
            ListOfDictionaries.append(m)
        if conn:
            conn.close()
        return ListOfDictionaries

    @classmethod
    def getMachine(cls, machine_id):
        machines = Machine.getAllMachines()
        for machine in machines:
            if machine['machine_id'] == machine_id:
                return machine
    
    @classmethod
    def InsertSampleData(cls):
        conn = sqlite3.connect(db_path)
        cur = conn.cursor()
        sample_data = [('M001', 'Forklift Alpha', 'Forklift', 'Operational', None, '2024-12-01 10:15:00'),
('M002', 'Pallet Jack Beta', 'Pallet Jack', 'Maintenance Required', 'Routine maintenance is due for hydraulic inspection.', '2024-11-30 14:30:00'),
('M003', 'Reach Truck Gamma', 'Reach Truck', 'Operational', None, '2024-11-25 08:45:00'),
('M004', 'Tow Tractor Delta', 'Tow Tractor', 'Out of Service', 'Electrical failure reported; parts on order.', '2024-12-03 16:20:00'),
('M005', 'Forklift Epsilon', 'Forklift', 'Operational', None, '2024-12-01 09:10:00'),
('M006', 'Order Picker Zeta', 'Order Picker', 'Operational', None, '2024-11-28 11:25:00'),
('M007', 'Pallet Jack Eta', 'Pallet Jack', 'Operational', None, '2024-12-02 13:50:00'),
('M008', 'Reach Truck Theta', 'Reach Truck', 'Maintenance Required', 'Battery replacement scheduled for next week.', '2024-12-01 15:40:00'),
('M009', 'Tow Tractor Iota', 'Tow Tractor', 'Operational', None, '2024-11-29 07:30:00'),
('M010', 'Order Picker Kappa', 'Order Picker', 'Out of Service', 'Control panel malfunction requires technician.', '2024-12-04 18:00:00'),
('M011', 'Forklift Alpha', 'Forklift', 'Operational', None, '2024-12-01 10:15:00'),
('M012', 'Pallet Jack Beta', 'Pallet Jack', 'Maintenance Required', 'Routine maintenance is due for hydraulic inspection.', '2024-11-30 14:30:00'),
('M013', 'Reach Truck Gamma', 'Reach Truck', 'Operational', None, '2024-11-25 08:45:00'),
('M014', 'Tow Tractor Delta', 'Tow Tractor', 'Out of Service', 'Electrical failure reported; parts on order.', '2024-12-03 16:20:00'),
('M015', 'Forklift Epsilon', 'Forklift', 'Operational', None, '2024-12-01 09:10:00'),
('M016', 'Order Picker Zeta', 'Order Picker', 'Operational',None, '2024-11-28 11:25:00'),
('M017', 'Pallet Jack Eta', 'Pallet Jack', 'Operational', None, '2024-12-02 13:50:00'),
('M018', 'Reach Truck Theta', 'Reach Truck', 'Maintenance Required', 'Battery replacement scheduled for next week.', '2024-12-01 15:40:00'),
('M019', 'Tow Tractor Iota', 'Tow Tractor', 'Operational', None, '2024-11-29 07:30:00'),
('M020', 'Order Picker Kappa', 'Order Picker', 'Out of Service', 'Control panel malfunction requires technician.', '2024-12-04 18:00:00')]
        cur.executemany('''INSERT INTO machines (machine_id, name, type, status,notes,last_update) VALUES (?, ?, ?, ?, ?,?)''', sample_data)
        conn.commit()
        conn.close()

    @classmethod
    def createSampleTable(cls):
        conn = sqlite3.connect(db_path)
        cur = conn.cursor()
        cur.execute('''CREATE TABLE machines (machine_id TEXT PRIMARY KEY,name TEXT,type TEXT,status TEXT,notes TEXT,last_update TEXT);''')
        conn.commit()
        conn.close()


if __name__ == '__main__':
    Machine.createSampleTable()
    Machine.InsertSampleData()
    print(Machine.getAllMachines())