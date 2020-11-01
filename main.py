import getpass
import readline
import sqlite3
import time
from random import randint

connection = None
cursor = None
print('Welcome to Cmput 291 Mini-Project 1')
while True:
    input_path = input('Enter database name: ')
    path = "./{}".format(input_path)
    try:
        connection = sqlite3.connect(path)
        cursor = connection.cursor()
        cursor.execute(' PRAGMA forteign_keys=ON; ')
        connection.commit()
        break
    except Exception:
        print('An error occured while connecting to database. Try again')


# helper functions: defined below

def ProcessString(string):
    """
        This basic function ensures that the input from user does not contain ';' in input string.
        Input: 'string' is of type String.
        Output: returns a processed string.
    """
    temp = string
    if ';' in temp:
        temp = string.split(sep=';', maxsplit=1)
        temp = temp[0]
    return temp

def askForRegistration():
    """
        This function determines if a user is registered or not
        Input: none
        Return: none
    """
    answer = input('Are you a registered user? (Enter yes or no): ')
    while not answer.lower() in ['y', 'yes', 'n', 'no']:
        answer = input('Are you a registered user? (Enter yes or no): ')
    if answer.lower() in ['y', 'yes']:
        return True
    else:
        return False

def searchForUser(userID, password):
    """
        This function determines the validity of a registered user.
        Input: userID is a string holding primary key for a user. password is string holding password for associated user_id.
        Return: boolean true if user_id is valid and false otherwise.
    """
    query = ''' SELECT uid, pwd FROM users WHERE uid=? AND pwd=? '''
    cursor.execute(query, (userID, password))
    alist = cursor.fetchall()
    connection.commit()
    if len(alist) > 0:
        ID, pwd = [alist[0][0], alist[0][1]]
        if ID == userID and pwd == password:
            return True
    return False

def provideValidUser():
    """
        This is validates a user's registration id and returns it.
    """
    query = ''' SELECT uid FROM users '''
    cursor.execute(query)
    allUsers = cursor.fetchall()
    connection.commit()

    uid = input('Enter unique user id(characters must be less than 5): ')
    while len(uid) <= 0 or len(uid) >= 5 or ((uid,) in allUsers):
        uid = input('Enter unique user id(characters must be less than 5): ')
    return uid

def provideValidPassword():
    """
        This is validates a user's registration password and returns it.
    """
    complete = False
    uid = ''
    while not complete:
        while len(uid) <= 0:
            uid = getpass.getpass('Create a unique password (size must be at least one): ')
        uid2 = getpass.getpass('Confirm password: ')

        if uid == uid2:
            complete = True
        else:
            print('Passwords do not match!')

    return uid

def addUser(name, location, userID, password):
    """
        This function registers user in the database
        Input: name, location userID and password all pertain to a valid user entity in database.
        Return: None
    """
    currentDate = time.strftime("%Y-%m-%d %H:%M:%S")
    query = ''' INSERT into users VALUES (?, ?, ?, ?, ?); '''
    cursor.execute(query, (userID, name, password, location, currentDate))
    connection.commit()

def getLoginInfo():
    """
        This function prompts for user_id and password. It hides the password while being entered in the command line.
        Input: none
        Return: user_id and password
    """
    userID = input('Enter user id: ')
    password = getpass.getpass('Enter password: ')
    userID = ProcessString(userID).lower()
    return [userID, password]

def getExitOption():
    """
        This function returns the user choice to exit the application.
        Input: None
        Return: true if user wants to exit application and false otherwise.
    """
    answer = ''
    while answer.lower() not in ['y', 'yes', 'n', 'no']:
        answer = input('Would you like to exit the program? (yes or no)')
    if answer.lower() in ['y', 'yes']:
        return True
    else:
        return False

def displayMainMenu():
    """
        This function displays the two main features that a logged in user may be able to use.
        Input: None
        Return: None
    """
    border = '-' * 24 + 'Main Menu' + '-' * 24
    border1 = '-' * len(border)
    print(border)
    print('Type "search" or command 1 to search for a post>')
    print('Type "post" or command 2 to create a post>')
    print('Type "logout" or command 0 to go back to login page>')
    print('Type "x" to exit entire program>')
    print(border1)

def getMainChoice():
    """
        This gets a users input for their choice of feature to explore.
    """
    alist = ['search', 'post', 'x', 'logout', '0', '1', '2']
    choice = input('Enter a valid choice: ')
    while True:
        if choice.lower() in alist:
            return choice.lower()
        else:
            choice = input('Enter a valid choice: ')

def getPostChoice(displayPage, priviledge):
    """
        This function gets the user's choice from the createPost function based on the page they are on.
        Input: displaypage indicates what position options shouuld be avaliable to user based on priivildges
        Return: .lower() string of valid user choice.
    """
    if displayPage == 'beforepost':
        alist = ['back', 'question', 'x', 'logout', '0', '3']
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
    """
        This function displays the menu for createPost() function
        Input: priviledge is a boolean indicating the status of the user
        Return: None
    """
    if displayPage == 'beforepost':
        border = '-' * 24 + 'Create post page' + '-' * 24
        print(border)
        print('Type 3 to create Question post or the command "question">')
        print('Type "logout" or command 0 to go back to login page>')
        print('Type "back" to return to main menu>')
        print('Type "x" to exit entire program>')
        print('-' * len(border))
    else:
        border = '-' * 26 + 'Post page' + '-' * 26
        print(border)
        print('Enter 5 or the command "vote" to vote for post >')
        if priviledge:
            print('Enter 6 or command "give" to give badge to user>')
            print('Enter 7 or command "tag" to add tag to post>')
            print('Enter 8 or command "edit" to edit post>')
        print('Type "logout" or command 0 to go back to login page>')
        print('Type "back" to return to main menu>')
        print('Type "x" to exit entire program>')
        print('-' * len(border))

def generatePostID():
    """
        This is genrates a unique pid for primary key of a post in the database.
        Input: None
        Return: a string containing a unique post id
    """
    query = ''' SELECT pid FROM posts ORDER BY pid; '''
    cursor.execute(query)
    allPIDs = cursor.fetchall()
    connection.commit()

    num = randint(0, 999)
    pid = 'p{:03d}'.format(num)
    if len(allPIDs) > 0:
        while (pid,) in allPIDs:
            num = randint(0, 999)
            pid = 'p{:03d}'.format(num)
    return pid

def getPostInfo(partOfPost):
    """
        This portion of the function gets the body and title of a post to be made.
        Input: 'partOfPost' represents either title or body of post to be prompted for.
        Returns: a string containing the input title or body of post to be made.
    """
    if partOfPost == 'title':
        text = input('Enter title of post: ')
    else:
        text = input('Enter body of post: ')
    text = ProcessString(text)
    return text

def helpPostQuestion(userID):
    """
        This function handles adding a post to the database.
        Input: userID is primark key of the user making the post.
        Returns: the postID in case neeeded.
    """
    # currentDate = time.strftime("%Y-%m-%d %H:%M:%S")
    currentDate = time.strftime("%Y-%m-%d")
    postID = generatePostID()
    ptitle = getPostInfo('title')
    pbody = getPostInfo('body')

    query1 = ''' INSERT into posts VALUES (?, ?, ?, ?, ?); '''
    query2 = ''' INSERT into questions VALUES (?, ?); '''
    cursor.execute(query1, (postID, currentDate, ptitle, pbody, userID))
    cursor.execute(query2, (postID, 'null'))
    connection.commit()
    print('-' * 60)
    print('Post sucessufully made!')
    print('-' * 60)
    print('Post Details:')
    print('Title:', ptitle)
    print('Body:', pbody)
    print('-' * 60)

    return postID

def getSearchKey(status='placeholder'):
    """
        This function allows user to input their key word for a search.
        Input: status is a default parameter to tell if user needed to search multiple times.
        Returns: a Processed string of user's input.
    """
    if status == 'not found':
        print('No search results...')
        print('Try again! or type command "end" to end search> ')

    while True:
        key = input('Enter valid search key: ')
        key = ProcessString(key)
        if len(key) > 0:
            return key.lower()

def searchQuery(word):
    # This function contains text for search query to database.
    # Input: word is the basis for search results to be queried
    # Returns: a string containing query
    query1 = '''
    SELECT summary_table.pid as pid, summary_table.title as title, summary_table.body as body, 
    summary_table.tot_votes as votes, ifnull(count(answers.pid), 0) as numAnsw, summary_table.pdate as pdate, 
    summary_table.poster as poster 
    FROM 
    (SELECT search_results.pid as pid, search_results.title as title, search_results.body as body, 
    ifnull(count(votes.vno), 0) as tot_votes, search_results.pdate as pdate, search_results.poster as poster 
    FROM 
    (SELECT * FROM posts WHERE lower(posts.title) LIKE "%{}%"
    UNION
     SELECT * FROM posts WHERE lower(posts.body) LIKE "%{}%"
    UNION
     SELECT p.pid as pid, p.pdate as pdate, p.title as title, p.body as body, p.poster as poster
        FROM posts p, tags t
        WHERE p.pid=t.pid AND lower(t.tag) LIKE "%{}%") search_results 
        LEFT OUTER JOIN votes ON search_results.pid=votes.pid group by search_results.pid ) summary_table 
        LEFT OUTER JOIN answers ON summary_table.pid=answers.qid GROUP BY summary_table.pid, summary_table.tot_votes;
        '''.format(word, word, word)
    return query1

def keyInTags(postID, key):
    """
        This function counts the number occurences of a keyword in a tag.
        Input: postID is a string representation of the post primary-key. Key is the string of specific keyword to be counted in tag.
        Return: boolean True if key is in tag and False otherwise.
    """
    query = ''' SELECT tag FROM posts JOIN tags ON tags.pid=posts.pid WHERE posts.pid=? '''
    cursor.execute(query, (postID,))
    tags = cursor.fetchall()
    connection.commit()

    if len(tags) > 0:
        for t in tags:
            if key in t[0]:
                return True
    return False

def ranking(post, keywords):
    count = 0
    for key in keywords:
        ptitle = post[1]
        pbody = post[2]
        if key != '':
            if key in ptitle or key in pbody or keyInTags(post[0], key):
                count += 1
    return count

def Searchdatabase(key):
    """
        This function retrieves post that contain words in key parameter in either its title, body, or tag fields.
        Input: key is a string representation of words provided by user in search option.
        Return: result is a list of posts enity that contain keyword(s)
    """
    keywords = key.split(' ')
    # Remove duplicate searches
    temp = set(keywords)
    keywords = list(temp)
    result = []
    for word in keywords:
        query = searchQuery(word)
        cursor.execute(query)
        result += cursor.fetchall()  # may include duplicates
    # Remove duplicates results
    unique = set(result)
    result = list(unique)
    connection.commit()
    if not result:
        return None
    if len(keywords) > 1:
        sorted(result, key=lambda p: ranking(p, keywords)) # sorting of result based on key matches(relevance)
    return result

def truncateString(size, string):
    """
        This function truncates a string according to size specification.
        Input: string to be manipulated. size indicates the limit for string.
        Returns: a string of with length <= size
    """
    if len(string) <= size:
        return string
    else:
        cut = size - 3
        return string[0:cut] + '...'

def displaySearchResult(result, lowerbound, upperbound):
    """
        This function prints to sreen the result from a user's search
        Input: result is a list containing the posts to be displayed. num is an integer repersenting size of list to be displayed.
               key is the input from user used to search.
        Return: None
    """
    pattern = '+' + '-' * 4 + '+' + '-' * 4 + '+' + '-' * 10 + '+' + '-' * 15 + '+' + '-' * 36 \
              + '+' + '-' * 5 + '+' + '-' * 4 + '+ '
    print(pattern)
    print('|{:^4}|{:^4}|{:^10}|{:^15}|{:^36}|{:^5}|{:^4}|'.format('Post', 'User', 'Date', 'Title',
                                                                  'Body of Post', 'NVote', 'NAns'))
    print(pattern)

    for p in range(lowerbound, upperbound):
        pid = result[p][0]
        ptitle = truncateString(15, result[p][1])
        pbody = truncateString(36, result[p][2])
        numVotes = str(result[p][3])
        numAns = str(result[p][4])
        pdate = truncateString(10, result[p][5])
        user = result[p][6]
        if typeOfPost(pid) == 'answer':
            numAns = 'NA'
        print('|{:^4}|{:^4}|{:^10}|{:^15}|{:^36}|{:^5}|{:^4}|'.format(pid, user, pdate, ptitle, pbody, numVotes, numAns))
    print(pattern)
    print('')

def displaySearchPageMenu(postOption):
    """
        This page displays the menu for the search page.
        Input: postoption indicates if there are post to select from or not.
        Return: None
    """
    global connection, cursor
    border = '-' * 24 + 'Search post page' + '-' * 24
    print(border)
    if postOption != None:
        print('Enter "more" to see more post>')
        print('Type "Post_ID" to select post>')
    print('Type "back" to go back>')
    print('Type "logout" or command 0 to go back to login page>')
    print('Type "x" to exit entire program>')
    print('-' * len(border))

def getSearchChoice(postOptions):
    """
        This function returns a valid choice from user on the search page.
        Input: postoption indicates what is a valid input by a user
        Return: string containing choice by user
    """
    if postOptions == None:
        alist = ['back', 'logout', '0', 'x']
    else:
        alist = ['back', 'more', 'logout', '0', 'x']
        for postInfo in postOptions:
            alist.append(postInfo[0])
    while True:
        answer = input('Enter valid choice: ')
        if answer.lower() in alist:
            return answer.lower()

def typeOfPost(post):
    """
        This function determines a if a post is an answer or question.
        Input: choice is a string containing pid of post
        Return: string of 'question' or 'answer'
    """
    global connection, cursor
    query = ''' SELECT pid FROM questions WHERE pid=?; '''
    cursor.execute(query, (post,))
    temp = cursor.fetchall()
    connection.commit()
    if len(temp) == 0:
        return 'answer'
    else:
        return 'question'

def displayMoreSearchResult(numSearch, result):
    """
        Thisfunction prints at most five more searches to the screen
        Input: numSearches is the nth time a we have to iterate the result list. starting at 1
        Return: None.
    """
    global connection, cursor

    maxDisplay = 5
    upperbound = numSearch * maxDisplay
    lowerbound = upperbound - maxDisplay
    if upperbound <= len(result):
        displaySearchResult(result, lowerbound, upperbound)
    else:
        if lowerbound < len(result):
            upperbound = len(result)
            displaySearchResult(result, lowerbound, upperbound)
        else:
            print('There are no more searches available!')

def printPost(pid):
    """
        This function prints a post to the screen
        Input: pid is a string of post primary key
        Return: None
    """
    query = ''' SELECT * FROM posts WHERE lower(pid)=?'''
    cursor.execute(query, (pid,))
    post = cursor.fetchone()
    connection.commit()

    Type = typeOfPost(pid)
    print('-' * 25 + 'Post Details' + '-' * 24)
    print('<'+Type.upper()+'Post>')
    print('Post ID: {}'.format(pid))
    print('Post date: {}'.format(post[1]))
    print('Post title: {}'.format(post[2]))
    print('Post body: {}'.format(post[3]))
    print('Poster: {}'.format(post[4]))
    print('-' * 60)

def helpHandleSearch(key, result, numSearch, priviledge, userID):
    """
        This function handles the search features of the application
        Input: numSearch is and integer to indicate limit of search and key contains the words provided by the user.
        Return: None or the user's choice if it is to exit or logout.
    """
    login = True
    Exit = False
    if numSearch == 1:
        if result is None:
            endSearch = False
            while result is None and not endSearch:
                key = getSearchKey('not found')
                if key == 'end':
                    endSearch = True
                if not endSearch:
                    result = Searchdatabase(key)

        if key != 'end' and result is not None:
            print('Search Results: "{}"'.format(key))
            displayMoreSearchResult(numSearch, result)
            displaySearchPageMenu(result)
        else:
            displaySearchPageMenu(None)
    choice = getSearchChoice(result)  # result is used to indicate what kind of choice is valid
    if choice == 'more':
        displayMoreSearchResult(numSearch + 1, result)
        displaySearchPageMenu(result)
        choice = helpHandleSearch(key, result, numSearch + 1, priviledge, userID)
    if choice not in ['logout', '0', 'x', 'back']:
        printPost(choice)
        choice = handlePostChoice(priviledge, userID, choice)
        return choice
    else:
        return choice

def displayPostChoiceMenu(Type, priviledge):
    """
        This function prints the menu after a post has been selected
        Input: Type is a string indicating type of post
        Return: None
    """
    print('-' * 60)
    if Type == 'question':
        print('Enter 4 or "answer" to create answer post for question>')
    print('Enter 5 or "vote" to add upvote to post>')
    if priviledge:
        print('Enter 6 or "give badge" to give poster a badge>')
        print('Enter 7 or "tag" to add a tag to the post>')
        print('Enter 8 or "edit" to edit post>')
    if Type == 'answer' and priviledge:
        print('Enter 9 or "mark" to indicate as the correct answer>')
    print('Type "back" to go back>')
    print('Type 0 or "logout" to go logout>')
    print('Type "x" to exit the entire program>')
    print('-' * 60)

def getSelectedPostChoice(Type, priviledge):
    """
        This function gets the user input after selecting a post
        Input: Type is a string indicating type of post
        Return: string containing choice from the user
    """
    alist = ['vote', '0', 'logout', 'x', 'back', '5']
    blist = []
    if Type == 'answer' and priviledge:
        blist = ['answer', '4', 'mark', '9', 'give badge', '6', 'edit', '8', 'tag', '7']
    elif Type == 'question' and priviledge:
        blist = ['answer', '4', 'give badge', '6', 'tag', '7', 'edit', '8']
    elif Type == 'question':
        blist = ['answer', '4']
    alist = blist + alist
    while True:
        choice = input('Select an option: ')
        if choice.lower() in alist:
            return choice.lower()

def handlePostChoice(priviledge, userID, postID):
    """
        This function handles the menu options available to a user after a user has selected a post.
        Input: priviledge is a boolean indicating what features the user has access to. The userID belond to whomever is logged in and postID is the post selected.
        Return: [login, Exit] status
    """
    Type = typeOfPost(postID)  # could be a question or answer returns string
    displayPostChoiceMenu(Type, priviledge)
    choice = getSelectedPostChoice(Type, priviledge)
    if choice == 'answer' or choice == '4':
        answerQuestion(userID, postID)
    elif choice == 'vote' or choice == '5':
        votePost(userID, postID)
    elif choice == 'give badge' or choice == '6':
        giveBadge(postID)
    elif choice == 'tag' or choice == '7':
        tag(postID)
    elif choice == 'edit' or choice == '8':
        privilegedEditPost(postID)
    elif choice == 'mark' or choice == '9':
        markAsAccepted(userID,postID)
    else:
        return choice
    choice = 'back'
    return choice

def tag(postID):
     '''
        This function adds tags to a selected post
        Input: postID is the primary key of the post.
        Return: None
     '''
     print("All tags on the post:")
     query = ''' SELECT tag FROM posts JOIN tags ON tags.pid=posts.pid WHERE posts.pid=? '''
     cursor.execute(query,(postID,))
     allTags = cursor.fetchall()
     connection.commit()
     if len(allTags) == 0:
         print("NO TAGS ON THIS POST")
     else:
         for i in allTags:
          print(i[0])
     print()
     print("Enter a tag which is not listed")
     text = input("Enter a Unique Tag: ")
     while (text,) in allTags:
         text = input("Enter a Unique Tag: ")
     query2 = ''' INSERT into tags VALUES (?, ?); '''
     cursor.execute(query2, (postID, text))
     connection.commit()

     print()
     print("Tag has been added to the post")
     print()
     query3 = '''SELECT * from tags where pid = ?'''
     cursor.execute(query3, (postID,))
     var1 = cursor.fetchall()
     connection.commit()
     print(var1)

def markAsAccepted(userID,postID):
     '''
        This function updates the accepted answer for a post.
        Input: primary key of user and answer post
        Return: None
     '''

     query1 = ''' SELECT a.qid from answers a, questions q  where lower(a.qid) = q.pid and a.pid=?'''
     cursor.execute(query1, (postID,))
     qid = cursor.fetchone()
     connection.commit()
     query4 =  '''Select * from questions where pid = ?;'''
     cursor.execute(query4, (qid[0],))
     var = cursor.fetchone()
     connection.commit()    
     if var[1] != 'null':
         print('-'*60); print("Do you want to change the accepted answer for the post below? ")
         printPost(qid[0])
         text = input("Yes or NO: ")
         if text.lower() == 'yes':
            query3 = ''' UPDATE questions set theaid = ? where pid  = ?; '''
            cursor.execute(query3, ('null', qid[0]))
            connection.commit()
            markAsAccepted(userID,postID)
     else:
         query3 = ''' UPDATE questions set theaid = ? where pid  = ?; '''
         cursor.execute(query3, (postID, qid[0]))
         connection.commit()
         print()
         print("The answer has been marked as accepted!")
         print()

def rlinput(prompt, prefill=''):
    '''
        This function gets input for an update
        Input: prompt is a string
        Return: the edited changes from a user
    '''
    readline.set_startup_hook(lambda: readline.insert_text(prefill))
    try:
        return input(prompt)
    finally:
        readline.set_startup_hook()

def privilegedEditPost(postID):
    """
    This allows the user to edit the existing title and body of the selected post
    Input: postID is the selected post
    Return: None
    """
    query = ''' SELECT title, body FROM posts WHERE pid = ?; '''
    cursor.execute(query, (postID,))
    title, body = cursor.fetchone()
    connection.commit()

    title = rlinput("Edit title: ", title)
    body = rlinput("Edit body: ", body)

    query = ''' UPDATE posts SET title = ?,body = ? WHERE pid = ? '''
    cursor.execute(query, (title, body, postID))
    connection.commit()

    print()
    print("The post has been updated")
    print()

def promptForBadgeName():
    """
    This prompts the user for a badge name that is available in the database
    Input: None
    Return: the chosen badge name
    """
    query = ''' SELECT bname FROM badges; '''
    cursor.execute(query)
    allBnames = cursor.fetchall()
    connection.commit()
    print()
    print('Available badge names:')
    for bname in allBnames:
        print('\t' + bname[0])
    print()
    chosenBname = input('Enter a valid badge name: ')
    while (chosenBname.lower(),) not in allBnames:
        chosenBname = input('The badge name you have chosen is not a valid badge name. Please re-enter: ')
    print()
    return chosenBname.lower()

def posterHasReceivedABadgeToday(poster, currentDate):
    """
    This checks if the creator of the selected post has received a badge today already
    Input: poster is the uid of the selected post's creator, currentDate is today's date
    Return: True if the user has voted already, False otherwise
    """
    global connection, cursor

    query = ''' SELECT * FROM ubadges WHERE uid = ? AND bdate = ?; '''
    cursor.execute(query, (poster, currentDate))
    rows = cursor.fetchall()
    connection.commit()
    if len(rows) == 0:
        return False
    return True

def giveBadge(postID):
    """
    This inserts an entry in the ubadges table for the poster associated with postID
    Input postID is the primary key of the selected post
    Return: None
    """
    currentDate = time.strftime("%Y-%m-%d")
    query = ''' SELECT poster FROM posts WHERE pid = ?; '''
    cursor.execute(query, (postID,))
    poster = cursor.fetchone()[0]
    connection.commit()

    if posterHasReceivedABadgeToday(poster, currentDate):
        print("The creator of this post has already received a badge today!")
        print()
        return None

    bname = promptForBadgeName()
    query = ''' INSERT INTO ubadges VALUES (?, ?, ?); '''
    cursor.execute(query, (poster, currentDate, bname))
    connection.commit()

    print('The badge "' + bname + '" has been given to user ' + poster + '!')
    print()

def generateVoteNumber(postID):
    """
        This generates a unique vno for the selected post in the database.
        Input: None
        Return: an unique integer vno for the selected post
    """
    global connection, cursor

    query = ''' SELECT vno FROM votes WHERE pid = ? ORDER BY vno; '''
    cursor.execute(query, (postID,))
    allVNOs = cursor.fetchall()
    connection.commit()

    vno = randint(0, 999)
    if len(allVNOs) > 0:
        while (vno,) in allVNOs:
            vno = randint(0, 999)
    return vno

def userVotedAlready(userID, postID):
    """
    This checks if the user has voted on the selected post already
    Input: userID is the primary key of the user, postID is the primary key of the selected post
    Return: True if the user has voted already, False otherwise
    """
    global connection, cursor

    query = ''' SELECT * FROM votes WHERE uid = ? AND pid = ?; '''
    cursor.execute(query, (userID, postID))
    rows = cursor.fetchall()
    connection.commit()
    if len(rows) == 0:
        return False
    return True

def votePost(userID, postID):
    """
    This inserts a user's vote in the votes table for the selected post
    Input: userID is the primary key of the user, postID is the primary key of the selected post
    Return: None
    """
    if userVotedAlready(userID, postID):
        print("You have voted on this post already!")
        print()
        return None

    currentDate = time.strftime("%Y-%m-%d")
    vno = generateVoteNumber(postID)
    query = ''' INSERT into votes VALUES (?, ?, ?, ?); '''
    cursor.execute(query, (postID, vno, currentDate, userID))
    connection.commit()
    print('-' * 60)
    print('Your vote has been cast!')
    print()
    print('-' * 60)

def helpPostAnswer(userID, questionID):
    """
    This function handles adding a post to the database.
    Input: userID is primark key of the user making the post.
    Returns: the postID in case neeeded.
    """
    currentDate = time.strftime("%Y-%m-%d")
    answerPostID = generatePostID()
    ptitle = getPostInfo('title')
    pbody = getPostInfo('body')

    query1 = ''' INSERT into posts values (?, ?, ?, ?, ?);'''
    query2 = ''' INSERT into answers VALUES(?, ?); '''
    
    cursor.execute(query1, (answerPostID, currentDate, ptitle, pbody, userID))
    cursor.execute(query2, (answerPostID, questionID))
    # query3 = ''' INSERT into questions VALUES (?, ?); '''
    # cursor.execute(query3, (questionID, answerPostID))
    print('-' * 60)
    print('Posted Answer sucessufully!')
    print('-' * 60)
    print('Post Details:')
    print('Title:', ptitle)
    print('Body:', pbody)
    print('-' * 60)

    return answerPostID

# Main Functions: defined below

def answerQuestion(userID, postID):
    """
    This function takes answer from question
    """
    login = True
    Exit = False
    questionID = postID
    answerID = helpPostAnswer(userID, questionID)
    choice = 'back'
    if choice == 'back':
        login = True
        Exit = False
    return [login, Exit]

def getUserLogin():
    """
        This function checks for registered users or resigters new users to the database.
        Input: None
        Return: a list of size two containing a boolean represent status of user in database(True if in it and False otherwise);
                and information about primary key of user. [True, user_id]
    """
    global connection, cursor

    registered = askForRegistration()
    if registered:
        userID, password = getLoginInfo()
        if searchForUser(userID, password):
            return [True, userID]
        else:
            print('User not registered!')
            userID, password = registerUser()
    else:
        userID, password = registerUser()
    return [True, userID]

def privledgeUser(userID):
    """
        This function determines if the user has administrative priviledges
        Input: userID is the identification of user to be logged in
        Return: returns true if user has priviledge and false otherwise.
    """
    query = ''' SELECT * FROM privileged WHERE uid=?  '''
    cursor.execute(query, (userID,))
    temp = cursor.fetchone()
    connection.commit()
    if temp is not None and temp[0] == userID:
        return True
    else:
        return False

def registerUser():
    """
        This function registers a user in the database:
        Input: none
        Return: string of user_id and password in a list.
    """
    print('Setting up account... ')
    name = input('Enter your Name: ')
    name = ProcessString(name)
    location = input('Enter your location: ')
    location = ProcessString(location)
    userID = provideValidUser()
    password = provideValidPassword()
    password = ProcessString(password)

    addUser(name, location, userID, password)
    return [userID, password]

def createPost(userID, priviledge):
    """
        This function allows a user to to create a question post.
        It can also update the login and exit variables in the main function.
        Input: userID is the unique identification for logged-in user.
        Return: login and exit status
    """
    login = True
    Exit = False
    DisplayCreatePostOption('beforepost', priviledge)
    choice = getPostChoice('beforepost', priviledge)

    if choice == '0' or choice == 'logout':
        login = False
    elif choice == '3' or choice == 'question':
        login, Exit = postQuestion(userID, priviledge)
    elif choice == 'back':
        login = True
        Exit = False
    else:
        login = False
        Exit = True
    return [login, Exit]

def postQuestion(userID, priviledge):
    """
        This function is collects and organizes a user's post for insertion into database. Also prompts for any other actions
        a user might want to take.
        Input: userID is primary of user making a post
        Return: [login, Exit] status
    """
    login = True
    Exit = False
    postID = helpPostQuestion(userID)
    # DisplayCreatePostOption('afterpost', priviledge)
    # choice = getPostChoice('afterpost', priviledge)
    choice = 'back'

    if choice == '0' or choice == 'logout':
        login = False
    elif choice == 'back':
        login = True
        Exit = False
    else:
        login = False
        Exit = True
    return [login, Exit]

def searchPost(userID, priviledge):
    """
        This function handles the search option from the main function.
        Input: userID is a string holding primary key for user, priviledge is a boolean indicating priviledge status
        Return: [login, Exit] status
    """
    numSearch = 1
    login = True
    Exit = False

    print('-' * 20 + 'Search Page' + '-' * 20)
    print('Enter one or more key words seperated by a blank space to search for a post> ')
    key = getSearchKey()
    result = Searchdatabase(key)
    choice = helpHandleSearch(key, result, numSearch, priviledge, userID)

    if choice == 'back':
        login = True
        Exit = False
    elif choice == 'logout' or choice == '0':
        login = False
    elif choice == 'x':
        login = False
        Exit = True
    return [login, Exit]

def main():
    # Controls the life of the application while in use
    Exit = False
    while not Exit:
        try:
            login, userID = getUserLogin()
            priviledge = privledgeUser(userID)
            while login:
                displayMainMenu()
                choice = getMainChoice()
                if choice == '1' or choice == 'search':
                    login, Exit = searchPost(userID, priviledge)
                elif choice == '2' or choice == 'post':
                    login, Exit = createPost(userID, priviledge)
                elif choice == '0' or choice == 'logout':
                    login = False
                else:
                    login = False
                    Exit = True
        except Exception as e:
            print(e)
            # print('An error occured! Try again.')
        if not Exit:
            Exit = getExitOption()
    print('Thanks for using this application. Have a good day!')
    connection.close()

main()
