import sqlite3
import os

script_dir = os.path.dirname(os.path.abspath(__file__))

db_path = os.path.join(script_dir, 'db_path.db')

class Project:
    def __init__(self, project_id, name, poc_name, poc_email, poc_phone, location, est_length, curr_length, budget, curr_exp, start_date, proj_end, status):
        self.__project_id = project_id
        self.__name = name
        self.__poc_name = poc_name
        self.__poc_email = poc_email
        self.__poc_phone = poc_phone
        self.__location = location
        self.__est_length = est_length
        self.__curr_length = curr_length
        self.__budget = budget
        self.__curr_exp = curr_exp
        self.__start_date = start_date
        self.__proj_end = proj_end
        self.__status = status

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

    @property
    def location(self):
        return self.__location

    @location.setter
    def location(self, value):
        self.__location = value

    @property
    def est_length(self):
        return self.__est_length

    @est_length.setter
    def est_length(self, value):
        self.__est_length = value

    @property
    def curr_length(self):
        return self.__curr_length

    @curr_length.setter
    def curr_length(self, value):
        self.__curr_length = value

    @property
    def budget(self):
        return self.__budget

    @budget.setter
    def budget(self, value):
        self.__budget = value

    @property
    def curr_exp(self):
        return self.__curr_exp

    @curr_exp.setter
    def curr_exp(self, value):
        self.__curr_exp = value

    @property
    def start_date(self):
        return self.__start_date

    @start_date.setter
    def start_date(self, value):
        self.__start_date = value

    @property
    def proj_end(self):
        return self.__proj_end

    @proj_end.setter
    def proj_end(self, value):
        self.__proj_end = value
    
    @classmethod
    def delProject(cls, project_id):
        conn = None
        conn = sqlite3.connect( db_path)
        sql='DELETE FROM projects WHERE project_id=?'
        cur = conn.cursor()
        cur.execute(sql, (project_id,))
        conn.commit()
        conn.close()

    @classmethod
    def addProject(cls, project_id, name, poc_name, poc_email, poc_phone, location, est_length, budget, curr_exp, start_date, proj_end, status):
        conn = None
        conn = sqlite3.connect( db_path)
        sql='INSERT INTO projects ( project_id, name, poc_name, poc_email, poc_phone, location, est_length, budget, curr_exp, start_date, proj_end, status) values (?,?,?,?,?,?,?,?,?,?,?,?)'
        cur = conn.cursor()
        cur.execute(sql, ( project_id, name, poc_name, poc_email, poc_phone, location, est_length, budget, curr_exp, start_date, proj_end,status, ))
        conn.commit()
        if conn:
            conn.close()

    @classmethod
    def updateProject(cls,project_id, name, poc_name, poc_email, poc_phone, location, est_length, budget, curr_exp, start_date, proj_end,status):
        conn = sqlite3.connect(db_path)
        sql='UPDATE projects SET name, poc_name, poc_email, poc_phone, location, est_length, budget, curr_exp, start_date, proj_end,status WHERE project_id = ?'
        cur = conn.cursor()
        cur.execute(sql, (name, poc_name, poc_email, poc_phone, location, est_length, budget, curr_exp, start_date, proj_end,status, project_id,))
        conn.commit()
        conn.close()


    @classmethod
    def getAllProjects(cls):
        conn = sqlite3.connect(db_path)
        cursorObj = conn.cursor()
        cursorObj.execute('SELECT project_id, name, poc_name, poc_email, poc_phone, location, est_length, curr_length, budget, curr_exp, start_date, proj_end,status FROM projects;')
        allRows = cursorObj.fetchall()
        ListOfDictionaries = []
        for row in allRows:
            m = {"project_id": row[0], 'name':row[1],"poc_name":row[2], 'poc_email': row[3], 'poc_phone':row[4], 'location':row[5],'est_length':row[6],'curr_length':row[7],'budget':row[8],'curr_exp':row[9],'start_date':row[10],'proj_end':row[11],'status':row[12]}
            ListOfDictionaries.append(m)
        if conn:
            conn.close()
        return ListOfDictionaries

    @classmethod
    def getProject(cls,project_id):
        projects = Project.getAllProjects()
        for project in projects:
            if project['project_id'] == project_id:
                return project
    
    @classmethod
    def InsertSampleData(cls):
        conn = sqlite3.connect(db_path)
        cur = conn.cursor()
        sample_data = [('Warehouse Automation', 'John Smith', 'john.smith@tmhna.com', '123-456-7890', 'Columbus, OH', '12 months', '6 months', 500000.00, 200000.00, '2024-01-01', '2024-12-31','On Time'),
('Forklift Telematics', 'Emily Davis', 'emily.davis@tmhna.com', '987-654-3210', 'Dallas, TX', '18 months', '9 months', 750000.00, 300000.00, '2023-07-01', '2024-12-31', 'On Time'),
('Inventory Management System', 'Michael Brown', 'michael.brown@tmhna.com', '456-789-0123', 'Indianapolis, IN', '24 months', '12 months', 1000000.00, 450000.00, '2023-01-01', '2025-01-01', 'At Risk'),
('Battery Optimization', 'Sophia Johnson', 'sophia.johnson@tmhna.com', '321-654-0987', 'Detroit, MI', '8 months', '4 months', 300000.00, 120000.00, '2024-03-01', '2024-11-01', 'Delayed'),
('Fleet Tracking', 'Liam Martinez', 'liam.martinez@tmhna.com', '654-321-8765', 'Phoenix, AZ', '15 months', '7 months', 600000.00, 250000.00, '2023-10-01', '2024-12-31', 'On Time'),
('Safety Enhancements', 'Emma Garcia', 'emma.garcia@tmhna.com', '567-890-1234', 'Seattle, WA', '10 months', '5 months', 400000.00, 180000.00, '2024-02-01', '2024-12-01', 'Delayed'),
('AI Predictive Maintenance', 'Oliver Wilson', 'oliver.wilson@tmhna.com', '890-123-4567', 'Chicago, IL', '20 months', '10 months', 900000.00, 400000.00, '2023-05-01', '2025-01-01', 'On Time'),
('Robotics Integration', 'Isabella Lee', 'isabella.lee@tmhna.com', '234-567-8901', 'Atlanta, GA', '16 months', '8 months', 800000.00, 350000.00, '2023-09-01', '2025-01-01', 'On Time'),
('Load Balancing Systems', 'James Thompson', 'james.thompson@tmhna.com', '678-901-2345', 'Denver, CO', '14 months', '6 months', 550000.00, 220000.00, '2024-01-01', '2025-03-01', 'On Time'),
('Real-Time Analytics', 'Ava White', 'ava.white@tmhna.com', '901-234-5678', 'San Diego, CA', '22 months', '11 months', 1200000.00, 500000.00, '2023-06-01', '2025-04-01', 'On Time')]
        cur.executemany('''INSERT INTO projects (name, poc_name, poc_email, poc_phone, location, est_length, curr_length, budget, curr_exp, start_date, proj_end, status) VALUES (?, ?, ?, ?, ?,?,?,?,?,?,?,?)''', sample_data)
        conn.commit()
        conn.close()

    @classmethod
    def createProjectTable(cls):
        conn = sqlite3.connect(db_path)
        cur = conn.cursor()
        cur.execute('''CREATE TABLE projects (project_id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT NOT NULL,poc_name TEXT NOT NULL,poc_email TEXT NOT NULL,poc_phone TEXT NOT NULL,location TEXT NOT NULL,est_length TEXT NOT NULL,curr_length TEXT,budget FLOAT NOT NULL,curr_exp FLOAT NOT NULL,start_date TEXT NOT NULL,proj_end TEXT NOT NULL, status TEXT NOT NULL);''')
        conn.commit()
        conn.close()


if __name__ == '__main__':
    Project.createProjectTable()
    Project.InsertSampleData()
    print(Project.getAllProjects())