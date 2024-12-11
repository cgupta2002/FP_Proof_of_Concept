import sqlite3
import os

script_dir = os.path.dirname(os.path.abspath(__file__))

db_path = os.path.join(script_dir, 'db_path.db')

class User:
    def __init__(self, user_id, username, name, email, password, profile_image, branch):
        self.__userID = user_id
        self.__username = username
        self.__name = name
        self.__email = email
        self.__password = password
        self.__profile_image = profile_image
        self.__branch = branch
   
    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, value):
        self.__name = value

    @property
    def email(self):
        return self.__email

    @email.setter
    def email(self, value):
        self.__email = value

    @property
    def password(self):
        return self.__password

    @password.setter
    def password(self, value):
        self.__password = value
    
    @property
    def profile_image(self):
        return self.__profile_image

    @profile_image.setter
    def profile_image(self, value):
        self.__profile_image = value

    @property
    def branch(self):
        return self.__branch

    @branch.setter
    def branch(self, value):
        self.__branch = value

    @property
    def username(self):
        return self.__username
    
    @username.setter
    def username(self,value):
        self.__username = value

    def __str__(self):
        return "Username: {} \n Name: {} \n Email: {} \n Branch: {} ".format(self.username, self.name,self.email,self.branch)
    
    @classmethod
    def delUser(cls, user_id):
        conn = None
        conn = sqlite3.connect( db_path)
        sql='DELETE FROM users WHERE user_id=?'
        cur = conn.cursor()
        cur.execute(sql, (user_id,))
        conn.commit()
        conn.close()

    @classmethod
    def addUser(cls, user_id, username, name, email, password, profile_image, branch):
        conn = None
        conn = sqlite3.connect( db_path)
        sql='INSERT INTO users ( user_id,username, name, email, password, profile_image, branch) values (?,?,?,?,?,?,?)'
        cur = conn.cursor()
        cur.execute(sql, ( user_id, username,name, email, password, profile_image, branch,))
        conn.commit()
        if conn:
            conn.close()

    @classmethod
    def addUserNoPic(cls, user_id, username, name, email, password, branch):
        conn = None
        conn = sqlite3.connect( db_path)
        sql='INSERT INTO users ( user_id,username, name, email, password, branch) values (?,?,?,?,?,?)'
        cur = conn.cursor()
        cur.execute(sql, ( user_id, username,name, email, password, branch,))
        conn.commit()
        if conn:
            conn.close()

    @classmethod
    def updateUser(cls,  user_id, email, password, branch):
        conn = sqlite3.connect(db_path)
        sql='UPDATE users SET email=?, password=?, branch = ? WHERE user_id = ?'
        cur = conn.cursor()
        cur.execute(sql, (email, password,  branch, user_id,))
        conn.commit()
        conn.close()

    @classmethod
    def updateImage(cls, user_id, profile_image):
        conn = sqlite3.connect(db_path)
        sql='UPDATE users SET profile_image=? WHERE user_id = ?'
        cur = conn.cursor()
        cur.execute(sql, (profile_image, user_id,))
        conn.commit()
        conn.close()

    @classmethod
    def getAllUsers(cls):
        conn = sqlite3.connect(db_path)
        cursorObj = conn.cursor()
        cursorObj.execute('SELECT user_id, username, name, email, password, profile_image, branch FROM users;')
        allRows = cursorObj.fetchall()
        ListOfDictionaries = []
        for row in allRows:
            m = {"user_id": row[0], 'username':row[1],"name":row[2], 'email': row[3], 'password':row[4], 'profile_image':row[5], 'branch':row[6]}
            ListOfDictionaries.append(m)
        if conn:
            conn.close()
        return ListOfDictionaries
    
    @classmethod
    def getUser(username):
        users = User.getAllUsers()
        for user in users:
            if user['username'] == username:
                return user
    
    @classmethod
    def getUserByID(cls, user_id):
        users = User.getAllUsers()
        for user in users:
            if user['user_id'] == user_id:
                return user

    @classmethod
    def getUserByName(cls, name):
        users = User.getAllUsers()
        for user in users:
            if user['name'] == name:
                return user
            
    @classmethod
    def getName(cls, user_id):
        users = User.getAllUsers()
        for user in users:
            if user['user_id'] == user_id:
                return user['name']
    
    @classmethod
    def InsertStartingData(cls):
        conn = sqlite3.connect(db_path)
        cur = conn.cursor()
        user_data = [
            (1, 'jdoe123','John Doe', 'johndoe@example.com', 'hashed_password_1', None, 'New York, NY'),
            (2, 'jsmith2030','Jane Smith', 'janesmith@example.com', 'hashed_password_2', None, 'Los Angeles, CA')]
        cur.executemany('''INSERT INTO Users (user_id, username, name, email, password, profile_image, branch) VALUES (?, ?, ?, ?, ?, ?, ?)''', user_data)
        conn.commit()
        conn.close()

    @classmethod
    def createUserTable(cls):
        conn = sqlite3.connect(db_path)
        cur = conn.cursor()
        cur.execute('''CREATE TABLE IF NOT EXISTS Users (user_id INTEGER PRIMARY KEY AUTOINCREMENT,username TEXT NOT NULL, name TEXT NOT NULL,email TEXT NOT NULL UNIQUE,password TEXT NOT NULL,profile_image TEXT,branch TEXT);''')
        conn.commit()
        conn.close()


if __name__ == '__main__':
    User.createUserTable()
    User.InsertStartingData()
    print(User.getAllUsers())


# hellooo
#hello hello