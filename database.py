import sqlite3
import helpers



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
        conn = sqlite3.connect('grades.db')
        cursor = conn.cursor()
        cursor.execute(command)
        rows = cursor.fetchall()
        return rows
    except sqlite3.Error as error:
        return helpers.apology(error)
    
    finally:
        if conn:
            conn.close()