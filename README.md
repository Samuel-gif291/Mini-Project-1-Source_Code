import time
import sqlite3

connection = None
cursor = None

def getPath():
    '''
       Input: None
       Returns: 'path' which is string containing the name of database to be connected to
    '''
    path = input('Enter database name: ')
    return path
    
def connectPath():
    '''
        This fuction connects to a database using information entered from user
        Input: None
        Return: None
    '''
    global connection, cursor
    path = getPath()
    try:
        connection = sqlite3.connect(path)
        cursor = connection.cursor()
        cursor.execute(' PRAGMA forteign_keys=ON; ')
        connection.commit()
    except Exception as e:
        print('An error occured while connecting to database')
    return
        
def privledgeUser(user_id):
    '''
        This function determines if a user has priviledges or not
        Input: user_id is the primary key used to identify a user in database
        Return: Boolean; True if user is in the privilege table and False otherwise
    '''
   global connection, cursor
   pass
   
def display_menu(privilege):
    '''
        This function displays the menu to the command-line and it restricts features based on privileges
        Input: privilege is a boolean representing status of priviledge
        Return: None
    '''
    global connection, cursor
    pass


def getUserLogin():
    '''
        This function checks for registered users or resigters new users to the database.
        Input: None
        Return: a list of size two containing a boolean represent status of user in database(True if in it and False otherwise);
                and information about primary key of user. [True, user_id]
    '''
    global connection, cursor
    pass


def main():
    # Controls the life of the application while in use
    # Input: None
    # Returns: None
    connectPath()
    exit = False
    while not exit:
        # do functions
        # set termination condition (exit=True)
        login, user_id = getUserLogin()
        priviledge = privledgeUser(user_id)
        while login:
            # do application features
            # set termination condition
            display_menu(privilege)
main()
