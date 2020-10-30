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
    userID = ProcessString(userID).lower()
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
        alist = ['back','question','x', 'logout', '0', '3']
    else:
        if priviledge:
            alist = ['vote', '5', 'give', '6', 'tag', '7', 'edit', '8', 'logout', '0', 'x']
        else:
            alist = ['back', 'vote', '5', 'logout', '0', 'x']
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
        print('Type "back" to return to main menu>')
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
        print('Type "back" to return to main menu>')
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
        while (pid,) in allPIDs:
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

    #currentDate = time.strftime("%Y-%m-%d %H:%M:%S")
    currentDate = time.strftime("%Y-%m-%d")
    postID = generatePostID()
    ptitle = getPostInfo('title')
    pbody = getPostInfo('body')

    query1 = ''' INSERT into posts VALUES (?, ?, ?, ?, ?); '''
    query2 = ''' INSERT into questions VALUES (?, ?); '''
    cursor.execute(query1, (postID, currentDate, ptitle, pbody, userID))
    cursor.execute(query2, (postID, 'null'))
    connection.commit()
    print('-'*60)
    print('Post sucessufully made!')
    print('-'*60)
    print('Post Details:')
    print('Title:', ptitle)
    print('Body:', pbody)
    print('-'*60)
    
    return postID

def getSearchKey(status='placeholder'):
    '''
        This function allows user to input their key word for a search.
        Input: status is a default parameter to tell if user needed to search multiple times.
        Returns: a Processed string of user's input.
    '''
    if status == 'not found':
        print('No search results...')
        print('Try again! or type command "end" to end search> ')
    
    while True:
        key = input('Enter valid search key: ')
        key = ProcessString(key)
        if len(key)>0:
            return key.lower()

def searchQuery(word):
    # This function contains text for search query to database.
    # Input: word is the basis for search results to be queried
    # Returns: a string containing query
    query1 = '''SELECT summary_table.pid as pid, summary_table.title as title, summary_table.body as body, summary_table.tot_votes as votes,
                ifnull(count(answers.pid), 0) as numAnsw, summary_table.pdate as pdate, summary_table.poster as poster
                FROM 
                (SELECT search_results.pid as pid, search_results.title as title, search_results.body as body, ifnull(count(votes.vno), 0) as tot_votes,
                search_results.pdate as pdate, search_results.poster as poster
                FROM 
                (SELECT *
                FROM posts
                WHERE lower(posts.title) LIKE "%{}%"
                UNION
                SELECT *
                FROM posts
                WHERE lower(posts.body) LIKE "%{}%"
                UNION
                SELECT p.pid as pid, p.pdate as pdate, p.title as title, p.body as body, p.poster as poster
                FROM posts p, tags t
                WHERE p.pid=t.pid AND lower(t.tag) LIKE "%{}%") search_results LEFT OUTER JOIN votes ON
                search_results.pid=votes.pid
                group by search_results.pid ) summary_table LEFT OUTER JOIN answers ON
                summary_table.pid=answers.qid
                GROUP BY summary_table.pid, summary_table.tot_votes;
        '''.format(word, word, word)
    return query1

def helpQuickSort(result, sortKey, start, end):
    '''
        This function is just an implementatation of quick sort.
        Input: result is the list to be sorted in place. sortkey is dictionay of form {pid:Number_of_Keyword matches}
        Return: None
    '''
    if start<end:
      part_ind = RandomizedPartition(result, sortKey, start, end)
      helpQuickSort(result, sortKey, start, part_ind-1)
      helpQuickSort(result, sortKey, part_ind+1, end)

def RandomizedPartition(alist, sortKey, start, end):
    '''
     Randomizes pivot. Partions a list using the last item in list size as pivot --alist[end]
     Input: alist is a list containg posts. sortKey is a dictionary used as basis for sorting.
            start is the first index of portion of list to be sorted. end is the last index of portion of list to be sorted.
     Returns: the index of item used to partition list. Randomizes pivot
    '''
   
    rand_ind = randint(start, end)
    alist[rand_ind], alist[end] = alist[end], alist[rand_ind]
    pivot = sortKey[alist[end][0]]
   
    i = start-1 # start to i represents all items > the pivot
    j = start   # i+1 to j represents item <= pivot
    for j in range(start, end):
       count = sortKey[alist[j][0]]
       if count>pivot:
          i += 1
          alist[j], alist[i] = alist[i], alist[j]
    alist[i+1], alist[end] = alist[end], alist[i+1]
    return i+1

def countKeyOccInTags(postID, key):
    '''
        This function counts the number occurences of a keyword in a tag.
        Input: postID is a string representation of the post primary-key. Key is the string of specific keyword to be counted in tag.
        Return: total count of occurences in a tag.
    '''
    global connection, cursor
    query = ''' SELECT tag FROM posts JOIN tags ON tags.pid=posts.pid WHERE posts.pid=? '''
    cursor.execute(query, (postID,))
    tags = cursor.fetchall()
    connection.commit()
    
    count = 0
    if len(tags)>0:
        for t in tags:
            tag = t[0] 
            count += len(tag.split(key))-1
    return count

def countOccurences(result, keywords):
    '''
        This function creates and returns a dictionary containg the number matches for keyword in each post.
        Input: result is a list of posts from search database query in search option. keywords is a list of words provided by user.
        ReturnS: a dictionary object of the format{pid:Count_of_keyword_Matches}
    '''
    global connection, cursor
    someDict = {}
    for post in result:
        count = 0
        for key in keywords:
            ptitle = post[1]
            pbody = post[2]
            if key != '':
                count += len(ptitle.split(key))-1  # add count of the occurence of keyword in title of post
                count += len(pbody.split(key))-1   # add count of the occurence of keyword in body of post
                count += countKeyOccInTags(post[0], key)  # add count of the occurence of keyword in tags of post
        someDict[post[0]] = count
    return someDict
    
def orderSearchResults(result, keywords):
    '''
        This function sorts result based on kweyword matches in title, body and tags
        Input: result is the list to be sorted
        Return: None
    '''
    global connection, cursor

    sortkey = countOccurences(result, keywords) # is a dictionary
    start, end = [0,len(result)-1]
    helpQuickSort(result, sortkey, start, end)

    
def Searchdatabase(key):
    '''
        This function retrieves post that contain words in key parameter in either its title, body, or tag fields.
        Input: key is a string representation of words provie by user in search option. num is an integer representing
               the number of searches made.
        Return: ...
    '''
    global connection, cursor

    keywords = key.split(' ')
    # Remove duplicate searches
    temp = set(keywords)
    keywords = list(temp)
    result = []
    for word in keywords:
        query = searchQuery(word)
        cursor.execute(query)
        result += cursor.fetchall() # may include duplicates
    # Remove duplicates results
    unique = set(result)
    result = list(unique)
    connection.commit()
    if result == []:
        return None
    if len(keywords) > 1:
        orderSearchResults(result, keywords) # in place sorting of result based on key matches
    return result 

def truncateString(size, string):
    '''
        This function truncates a string according to size specification.
        Input: string to be manipulated. size indicates the limit for string. 
        Returns: a string of with length <= size 
    '''
    if len(string) <= size:
        return string
    else:
        cut = size-3
        return string[0:cut]+'...'
    
def displaySearchResult(result, lowerbound, upperbound):
    '''
        This function prints to sreen the result from a user's search
        Input: result is a list containing the posts to be displayed. num is an integer repersenting size of list to be displayed.
               key is the input from user used to search.
        Return: None
    '''
    global connection, cursor
    print('+'+'-'*4+'+'+'-'*4+'+'+'-'*10+'+'+'-'*15+'+'+'-'*36+'+'+'-'*5+'+'+'-'*4+'+')
    print('|{:^4}|{:^4}|{:^10}|{:^15}|{:^36}|{:^5}|{:^4}|'.format('Post','User','Date', 'Title', 'Body of Post', 'NVote', 'NAns'))
    print('+'+'-'*4+'+'+'-'*4+'+'+'-'*10+'+'+'-'*15+'+'+'-'*36+'+'+'-'*5+'+'+'-'*4+'+')
    
    for p in range(lowerbound, upperbound):
        pid = result[p][0]
        ptitle = truncateString(15,result[p][1])
        pbody = truncateString(36,result[p][2])
        numVotes = str(result[p][3])
        numAns = str(result[p][4])
        pdate = truncateString(10,result[p][5])
        user = result[p][6]
        if typeOfPost(pid) == 'answer':
            numAns = 'NA'
        print('|{:^4}|{:^4}|{:^10}|{:^15}|{:^36}|{:^5}|{:^4}|'.format(pid,user,pdate, ptitle, pbody, numVotes, numAns))
    print('+'+'-'*4+'+'+'-'*4+'+'+'-'*10+'+'+'-'*15+'+'+'-'*36+'+'+'-'*5+'+'+'-'*4+'+'); print('')

def displaySearchPageMenu(postOption):
    '''
        This page displays the menu for the search page.
        Input: postoption indicates if there are post to select from or not.
        Return: None
    '''
    global connection, cursor
    border = '-'*24+'Search post page'+'-'*24
    print(border)
    if postOption != None:
        print('Enter "more" to see more post>')
        print('Type "Post_ID" to select post>')
    print('Type "back" to go back>')
    print('Type "logout" or command 0 to go back to login page>')
    print('Type "x" to exit entire program>')
    print('-'*len(border))
        
def getSearchChoice(postOptions):
    '''
        This fuction returns a valid choice from user on the search page.
        Input: postoption indicates what is a valid input by a user
        Return: string containing choice by user
    '''
    
    global connection, cursor
    if postOptions == None:
        alist = [ 'back', 'logout', '0', 'x']
    else:
        alist = ['back', 'more', 'logout', '0', 'x']
        for postInfo in postOptions:
            alist.append(postInfo[0])
    while True:
        answer = input('Enter valid choice: ')
        if answer.lower() in alist:
            return answer.lower()

def typeOfPost(post):
    '''
        This function determines a if a post is an answer or question.
        Input: choice is a string containing pid of post
        Return: string of 'question' or 'answer'
    '''
    global connection, cursor
    query = ''' SELECT pid FROM questions WHERE pid=?; '''
    cursor.execute(query, (post,))
    temp = cursor.fetchall()
    connection.commit()
    if len(temp)==0:
        return 'answer'
    else:
        return 'question'
    
def displayMoreSearchResult(numSearch, result):
    '''
        Thisfunction prints at most five more searches to the screen
        Input: numSearches is the nth time a we have to iterate the result list. starting at 1
        Return: None.
    '''
    global connection, cursor
    
    maxDisplay = 5
    upperbound = numSearch*maxDisplay
    lowerbound = upperbound - maxDisplay
    if upperbound<=len(result):
        displaySearchResult(result, lowerbound, upperbound)
    else:
        if lowerbound<len(result):
            upperbound = len(result)
            displaySearchResult(result, lowerbound, upperbound)
        else:
            print('There are no more searches available!')
        

    
def helpHandleSearch(key, result, numSearch, priviledge):
    '''
        This function handles the search features of the application
        Input: numSearch is and integer to indicate limit of search and key contains the words provided by the user.
        Return: None or the user's choice if it is to exit or logout.
    '''
    global connection, cursor
    login = True; Exit = False
    if numSearch == 1:
        #result = Searchdatabase(key)
        if result == None:
            endSearch = False
            while result == None and not endSearch:
                key = getSearchKey('not found')
                if key == 'end':
                    endSearch = True
                if not endSearch:
                    result = Searchdatabase(key)

        if key != 'end' and result != None:
            print('Search Results: "{}"'.format(key))
            displayMoreSearchResult(numSearch, result)
            displaySearchPageMenu(result)
        else:
            displaySearchPageMenu(None)
    choice = getSearchChoice(result) # result is used to indicate what kind of choice is valid
    if choice == 'more':
        displayMoreSearchResult(numSearch+1, result)
        displaySearchPageMenu(result)
        choice = helpHandleSearch(key, result, numSearch+1, priviledge)
    if choice not in ['logout', '0', 'x', 'back']:
        Type = typeOfPost(choice) # could be a question or answer returns string
        if Type == 'question':
            pass # can answer the question, give badge, vote, edit post or tag post based on user priviledge 
        elif Type == 'answer':
            pass # can indicated as accpted, give badge, vote, edit post or tag post based on user priviledge
    else:
        return choice

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
        Return: [login, Exit] status
    '''
    global connection, cursor
    
    login = True; Exit = False
    postID = helpPostQuestion(userID)
    DisplayCreatePostOption('afterpost', priviledge)
    choice = getPostChoice('afterpost', priviledge)
    
    if choice == '0' or choice == 'logout':
        login = False
    elif choice == '3' or choice == 'question':  # consider deleting
        pass #login, Exit = postQuestion(userID, priviledge)
    elif choice == '5' or choice == 'vote':
        pass # add up vote to database
    elif choice == '6' or choice == 'badge':
        pass # give badge to userID
    elif choice == '7' or choice == 'tag':
        pass # get and add tag to post
    elif choice == '8' or choice == 'edit':
        pass # collect edit and update post with postID
    elif choice == 'back':
        login = True; Exit = False
    else:
        login = False; Exit = True
    return [login, Exit]

def searchPost(userID, priviledge):
    '''
        This function handles the search option from the main function.
        Input: userID is a string holding primary key for user, priviledge is a boolean indicating priviledge status
        Return: [login, Exit] status
    '''
    global connection, cursor
    numSearch = 1
    login = True; Exit = False
    
    print('-'*20+'Search Page'+'-'*20)
    print('Enter one or more key words seperated by a blank space to search for a post> ')
    key = getSearchKey()
    result = Searchdatabase(key)
    choice = helpHandleSearch(key, result, numSearch, priviledge)
    
    if choice == 'back':
        login = True; Exit = False
    elif choice == 'logout' or choice == '0':
        login = False
    elif choice == 'x':
        login = False; Exit = True
    return [login, Exit]

def editPost(userID, privledge):
    '''
        This function enables a priviledged user to edit any post.
        Input: userID is the primary key of the user. priviledge is a boolean indicating the administrative status of user.
        Return: [login, exit] status
    '''
    global connection, cursor
    login = True; Exit = False
    print('-'*26+'Edit Page'+'-'*26)
    choice = input('What part of post would you like to edit? (title/body)>')
    while choice.lower() not in ['title', 'body']:
        choice = input('What part of post would you like to edit? (title/body)>')
    
    edit = input('Type in edit: ')
    alist = ['logout', 'back', '0', 'exit'] 
    
    displayEditpageMenu()
    choice = getEditPageOption()

    if choice == 'logout' or choice == '0':
        login = False
    elif choice == 'exit':
        login = False; Exit = True
    elif choice == 'back':
        login = True; Exit = False
    return login,Exit


    
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
                login, Exit = searchPost(userID, priviledge)
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

