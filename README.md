import time
import sqlite3
import getpass
from random import randint

connection = None
cursor = None

# helper functions: defined below


def getPath():
    '''
       Input: None
       Returns: 'path' which is string containing the name of database to be connected to
    '''
    path = input('Enter database name: ')
    return "./{}".format(path)

def ProcessString(string):
    '''
        This basic function ensures that the input from user does not contain ';' in input string.
        Input: 'string' is of type String.
        Output: returns a processed string.
    '''
    temp = string
    if ';' in temp: 
        temp = string.split(sep=';', maxsplit=1)
        temp = temp[0]
    return temp

def connectPath():
    '''
        This fuction connects to a database using information entered from user
        Input: None
        Return: None
    '''
    global connection, cursor
    print('Welcome to Cmput 291 Mini-Project 1')
    while True:
        path = getPath()
        try:
            connection = sqlite3.connect(path)
            cursor = connection.cursor()
            cursor.execute(' PRAGMA forteign_keys=ON; ')
            connection.commit()
            return
        except Exception as e:
            print('An error occured while connecting to database. Try again')
        
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

def askForRegistration():
    '''
        This function determines if a user is registered or not
        Input: none
        Return: none
    '''
    global connection, cursor
    
    answer = input('Are you a registered user? (Enter yes or no): ')
    while not answer.lower() in ['y', 'yes', 'n', 'no']:
        answer = input('Are you a registered user? (Enter yes or no): ')
    if answer.lower() in ['y', 'yes']:
        return True
    else:
        return False
    
def searchForUser(userID, password):
    '''
        This function determines the validity of a registered user.
        Input: userID is a string holding primary key for a user. password is string holding password for asscociated user_id.
        Return: boolean true if user_id is valid and false otherwise.
    '''
    global connection, cursor
    
    query = query = ''' SELECT uid, pwd FROM users WHERE uid=? AND pwd=? '''
    cursor.execute(query, (userID, password))
    alist = cursor.fetchall()
    connection.commit()
    if len(alist) > 0:
        ID,pwd = [alist[0][0], alist[0][1]]
        if ID == userID and pwd == password:
            return True
    return False
        

def provideValidUser():
    '''
        This is validates a user's registration id and returns it.
    '''
    global connection, cursor
    query = ''' SELECT uid FROM users '''
    cursor.execute(query)
    allUsers = cursor.fetchall()
    connection.commit()

    uid = input('Enter unique user id(characters must be less than 5): ')
    while len(uid)<=0 or len(uid)>=5 or ((uid,) in allUsers):
        uid = input('Enter unique user id(characters must be less than 5): ')
    return uid 
        
def provideValidPassword():
    '''
        This is validates a user's registration password and returns it.
    '''
    complete = False
    while not complete:
        #uid = input('Create a unique password (size must be at least one): ')
        uid = getpass.getpass('Create a unique password (size must be at least one): ')
        while len(uid)<= 0:
            uid = getpass.getpass('Create a unique password (size must be at least one): ')
        
        uid2 = getpass.getpass('Confirm password: ')

        if uid == uid2:
            complete = True
        else:
            print('Passwords do not match!')
    
    return uid

def addUser(name, location, userID, password):
    '''
        This function registers user in the database
        Input: name, location userID and password all pertain to a valid user entity in database.
        Return: None
    '''
    global connection, cursor
    currentDate = time.strftime("%Y-%m-%d %H:%M:%S")
    query = ''' INSERT into users VALUES (?, ?, ?, ?, ?); '''
    cursor.execute(query, (userID, name, password, location, currentDate))
    connection.commit()
    
    
def getLoginInfo():
    '''
        This function prompts for user_id and password. It hides the password while being entered in the command line.
        Input: none
        Return: user_id and password
    '''
    global connection, cursor
    
    userID = input('Enter user id: ')
    password = getpass.getpass('Enter password: ')
    return [userID, password]

def getExitOption():
    '''
        This function returns the user choice to exit the application.
        Input: None
        Return: true if user wants to exit application and false otherwise.
    '''
    global connection, cursor
    answer = input('Would you like to exit the program? (yes or no)')
    while answer.lower() not in ['y','yes','n','no']:
        answer = input('Would you like to exit the program? (yes or no)')
    if answer.lower() in ['y','yes']:
        return True
    else:
        return False

def displayMainMenu():
    '''
        This function displays the two main features that a logged in user may be able to use.
        Input: None
        Return: None
    '''
    global connection, cursor
    border = '-'*24+'Main Menu'+'-'*24
    border1 = '-'*len(border)
    print(border)
    print('Type "search" or command 1 to search for a post>')
    print('Type "post" or command 2 to create a post>')
    print('Type "logout" or command 0 to go back to login page>')
    print('Type "x" to exit entire program>')
    print(border1)

def getMainChoice():
    '''
        This gets a users input for their choice of feature to explore.
    '''
    global connection, cursor
    
    alist = ['search','post','x', 'logout', '0', '1', '2']
    choice = input('Enter a valid choice: ')
    while True:    
        if choice.lower() in alist:
            return choice.lower()
        else:
            choice = input('Enter a valid choice: ')

def getPostChoice(displayPage, priviledge):
    '''
        This function gets the user's choice from the createPost function based on the page they are on.
        Input: displaypage indicates what position options shouuld be avaliable to user based on priivildges
        Return: .lower() string of valid user choice.
    '''
    global connection, cursor
    
    if displayPage == 'beforepost':
        alist = ['question','x', 'logout', '0', '3']
    else:
        if priviledge:
            alist = ['vote', '5', 'give', '6', 'tag', '7', 'edit', '8', 'logout', '0', 'x']
        else:
            alist = ['vote', '5', 'logout', '0', 'x']
    choice = input('Enter your choice: ')
    while True:    
        if choice.lower() in alist:
            return choice.lower()
        else:
            choice = input('Enter a valid choice: ')

def DisplayCreatePostOption(displayPage, priviledge):
    '''
        This function displays the menu for createPost() function
        Input: priviledge is a boolean indicating the status of the user
        Return: None
    '''
    if displayPage == 'beforepost':
        border = '-'*24+'Create post page'+'-'*24
        print(border)
        print('Enter 3 to create Question post or the command "question">')
        print('Type "logout" or command 0 to go back to login page>')
        print('Type "x" to exit entire program>')
        print('-'*len(border))
    else:
        border = '-'*26+'Post page'+'-'*26
        print(border)
        print('Enter 5 or the command "vote" to vote for post >')
        if priviledge:
            print('Enter 6 or command "give" to give badge to user>')
            print('Enter 7 or command "tag" to add tag to post>')
            print('Enter 8 or command "edit" to edit post>')
        print('Type "logout" or command 0 to go back to login page>')
        print('Type "x" to exit entire program>') 
        print('-'*len(border))

def generatePostID():
    '''
        This is genrates a unique pid for primary key of a post in the database.
        Input: None
        Return: a string containing a unique post id
    '''
    global connection, cursor

    query = ''' SELECT pid FROM posts ORDER BY pid; '''
    cursor.execute(query)
    allPIDs = cursor.fetchall()
    connection.commit()
    
    num = randint(0,999)
    pid = 'p{:03d}'.format(num)
    
    if len(allPIDs)>0:
        largestpid = allPIDs[len(allPIDs)-1]; largestpid = largestpid[0]
        while pid <= largestpid:
            num = randint(0,999)
            pid = 'p{:03d}'.format(num)
    return pid    

def getPostInfo(partOfPost):
    '''
        This portion of the function gets the body and title of a post to be made.
        Input: 'partOfPost' represents either title or body of post to be prompted for.
        Returns: a string containing the input title or body of post to be made.
    '''
    global connection, cursor
    
    if partOfPost == 'title':
        text = input('Enter title of post: ')
    else:
        text = input('Enter body of post: ')
    text = ProcessString(text)
    return text

def helpPostQuestion(userID):
    '''
        This function handles adding a post to the database.
        Input: userID is primark key of the user making the post.
        Returns: the postID in case neeeded.
    '''
    global connection, cursor

    currentDate = time.strftime("%Y-%m-%d %H:%M:%S")
    postID = generatePostID()
    ptitle = getPostInfo('title')
    pbody = getPostInfo('body')

    query = ''' INSERT into posts VALUES (?, ?, ?, ?, ?); '''
    cursor.execute(query, (postID, currentDate, ptitle, pbody, userID))
    connection.commit()
    print('Post sucessufully made!')
    print('-'*60)
    print('Post Details:')
    print('Title:', ptitle)
    print('Body:', pbody)
    print('-'*60)
    
    return postID

def exitProgram():
    '''
        Prints goodbye message to the screen and closes connection.
    '''
    global connection, cursor
    print('Thanks for using this application. Have a good day!')
    connection.close()
    
# Main Functions: defined below

def getUserLogin():
    '''
        This function checks for registered users or resigters new users to the database.
        Input: None
        Return: a list of size two containing a boolean represent status of user in database(True if in it and False otherwise);
                and information about primary key of user. [True, user_id]
    '''
    global connection, cursor
    
    registered = askForRegistration()
    if registered:
        userID,password = getLoginInfo()
        if searchForUser(userID, password):
            return [True, userID]
        else:
            print('User not registered!')
            userID, password = registerUser()
    else:
        userID, password = registerUser()
    return [True, userID]
    

def privledgeUser(userID):
    '''
        This function determines if the user has administrative priviledges
        Input: userID is the identification of user to be logged in
        Return: returns true if user has priviledge and false otherwise. 
    '''
    global connection, cursor
    temp = None
    query = ''' SELECT * FROM privileged WHERE uid=?  '''
    cursor.execute(query, (userID,))
    temp = cursor.fetchone()
    connection.commit()
    if temp != None and temp[0] == userID:
        return True
    else:
        return False
    
def registerUser():
    '''
        This function registers a user in the database:
        Input: none
        Return: string of user_id and password in a list.
    '''
    global connection, cursor
    
    print('Setting up account... ')
    name = input('Enter your Name: '); name = ProcessString(name)
    location = input('Enter your location: '); location = ProcessString(location)
    userID = provideValidUser()
    password = provideValidPassword(); password = ProcessString(password)

    addUser(name, location, userID, password)
    return [userID, password]

def createPost(userID, priviledge):
    '''
        This function allows a user to to create a question post.
        It can also update the login and exit variables in the main function.
        Input: userID is the unique identification for logged-in user.
        Return: login and exit status
    '''
    global connection, cursor
    login = True; Exit = False
    DisplayCreatePostOption('beforepost', priviledge)
    choice = getPostChoice('beforepost', priviledge)
    
    if choice == '0' or choice == 'logout':
        login = False
    elif choice == '3' or choice == 'question':
        login, Exit = postQuestion(userID, priviledge)
    else:
        login = False; Exit = True
    return [login, Exit]
    
    
def postQuestion(userID, priviledge):
    '''
        This function is collects and organizes a user's post for insertion into database. Also prompts for any other actions
        a user might want to take.
        Input: userID is primary of user making a post
        Return: ...
    '''
    global connection, cursor
    
    login = True; Exit = False
    postID = helpPostQuestion(userID)
    DisplayCreatePostOption('afterpost', priviledge)
    choice = getPostChoice('afterpost', priviledge)
    
    if choice == '0' or choice == 'logout':
        login = False
    elif choice == '3' or choice == 'question':
        pass #postQuestion(userID, priviledge)
    elif choice == '5' or choice == 'vote':
        pass # add up vote to database
    elif choice == '6' or choice == 'badge':
        pass # give badge to userID
    elif choice == '7' or choice == 'tag':
        pass # get and add tag to post
    elif choice == '8' or choice == 'edit':
        pass # collect edit and update post with postID
    else:
        login = False; Exit = True
    return [login, Exit]
    
    
def main():
    # Controls the life of the application while in use
    # Input: None
    # Returns: None
    global connection, cursor
    connectPath()
    Exit = False
    while not Exit:
        # do functions
        # set termination condition (exit=True)
        login, userID = getUserLogin()
        priviledge = privledgeUser(userID)
        
        while login:
            # do application features
            # set termination condition for 
            displayMainMenu()
            choice = getMainChoice()
            if choice == '1' or choice == 'search':
                searchPost(userID)
            elif choice == '2' or choice == 'post':
                login, Exit = createPost(userID, priviledge)
            elif choice == '0' or choice == 'logout':
                login = False
            else:
                login = False; Exit = True
        
        if Exit == False:
            Exit = getExitOption()
    exitProgram()

main()

