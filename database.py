import sqlite3



def insert(command):
    try:
        database = sqlite3.connect("grades.db")
        cursor = database.cursor()
        cursor.execute(command)
        
    except sqlite3.Error as error:
        print("There has been a error: ", error)
        
    finally:
        if database:
            database.close()
            
def readData(command):
    try: 
        database = sqlite3.connect("grades.db")
        cursor = database.cursor()
        
        cursor.execute(command)
        result = cursor.fetchall()
        
        cursor.close()
        return result
        
    except sqlite3.Error as error:
        print("There is a error - ", error)
    
    finally:
        if database:
            database.close()