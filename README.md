import time
import sqlite3

connection = None
cursor = None

def connect(path):
    global connection, cursor

    connection = sqlite3.connect(path)
    cursor = connection.cursor()
    cursor.execute(' PRAGMA forteign_keys=ON; ')
    connection.commit()
    return
def getPath():
    '''Input: None
       Returns: 'path' which is string containing the name of database to be connected to
    '''
    path = input('Enter database name: ')
    return path
    
def connectPath(path):
    '''
        This fuction connects to a database
        Input: path is a string containing name of Database
        Return: None
    '''
    global connection, cursor
    
    try:
        connection = sqlite3.connect(path)
        cursor = connection.cursor()
        cursor.execute(' PRAGMA forteign_keys=ON; ')
        connection.commit()
    except Exception as e:
        print('An error occured while connecting to database')
        

def login():
    # this function displays 
    # input: None
    # Return: None
    pass


def main():
    # Controls the life of the application while in use
    # Input: None
    # Returns: None
    
    exit = False
    while not exit:
        # do functions
        # set termination condition (exit=True)
        path = getPath()
        connect_database()
        login, user_id = getUserLogin()
        while login:
            # do application features
            # set termination condition
main()
