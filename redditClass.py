# Packages

# Defualt pacakges
import os

# Mysql db
import mysql.connector
from mysql.connector import Error

# For requests
import requests
import json

# Class reddit posts


class Reddit():

    # Counstructer
    def __init__(self, rUser, sortBy='new', pLimit=25):
        self.rUser = str(rUser)
        self.sortBy = str(sortBy)
        self.pLimit = pLimit

        # Class details
        print(
            f"******************\nReddit user: u/{rUser}\nSort by: {sortBy}\nPosts limit: {pLimit}\n******************\n")

    # Set database details and connections | Boolean
    def db(self, host, user, password, database, tableName):
        # Make a connection to data base
        try:
            # Connecte to MySql database
            self.connection = mysql.connector.connect(host=host,
                                                      database=database,
                                                      user=user,
                                                      password=password)
            self.tableName = tableName
            return True

        # Catch the error
        except Error as e:
            print("Error while connecting to MySQL ->", e)
            return False

    # Close db connection | Boolean
    def db_close(self):
        try:
            if self.connection.is_connected():
                self.connection.close()
                # print("MySQL connection is closed")
                return True
        except Error as e:
            print("Error while close db connection ->", e)
            return False

    # Insert to data base | Return boolean
    def insert(self, val):
        # Check if val isn't null
        if len(val) <= 0:
            # print("There is no valuse to insert to database. Try again")
            return False
        else:
            # If connected
            if self.connection.is_connected():
                cursor = self.connection.cursor()
                # Insert to database query

                # query = f"INSERT INTO `{self.tableName}` (`postId`, `subreddit`, `title`, `url`, `thumbnail`, `IsVideo`, `IsYoutube`, `IsImageGif`, `IsText`, `author`, `points`, `comments`) VALUES (NULL, '{postId}', '{postSubreddit}', '{postTitle}', '{postUrl}', '{postThumbnail}', '{postIsVideo}', '{postIsYoutube}', '{postIsImageGif}', '{postIsText}', '{postAuthor}', '{postPoints}', '{postComments}')"
                sql = f"INSERT INTO `{self.tableName}` (`postId`, `subreddit`, `title`, `url`, `thumbnail`, `IsVideo`, `IsYoutube`, `IsImageGif`, `IsText`, `author`, `points`, `comments`) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"

                try:
                    # Insert it to data base
                    cursor.executemany(sql, val)
                    self.connection.commit()
                    print(
                        cursor.rowcount, f"Record inserted successfully into {self.tableName}")
                    cursor.close()
                    return True

                # Catch the error
                except Error as e:
                    print("Error while insert to database ->", e)
                    return False

    # Get data from database | Array
    def select(self, attr='*'):
        try:
            cursor = self.connection.cursor()
            cursor.execute(f"SELECT {attr} FROM {self.tableName}")
            myresult = cursor.fetchall()

            return myresult

        except Error as e:
            print("Error while get data ->", e)
            return []

    # Update database and check the duplicated posts | Array
    def update(self):
        postsList = []
        try:
            # Get reddit json
            link = f'https://reddit.com/user/{self.rUser}/upvoted.json?sort={self.sortBy}&limit={self.pLimit}'

            # Send get request
            r = requests.get(link, headers={'User-agent': 'SalamnBot 0.1'})

            # Get all json on it
            res = json.loads(r.text)

            # Check if the post is duplicated or not
            for j in range(len(res['data']['children'])):
                try:
                    # Get reddit post id from json
                    rPoId = str(res['data']['children'][j]['data']['id'])
                    sql = f"SELECT `postId` FROM {self.tableName} WHERE `postId` = '{rPoId}'"

                    # Search in tabel where postId == reddit post id
                    cursor = self.connection.cursor()
                    cursor.execute(sql)
                    getPostId = cursor.fetchall()

                    # Convert from tuple to list
                    list(getPostId)

                    # If the post is not replicated
                    if len(getPostId) == 0:
                        # Post details
                        postID = res['data']['children'][j]['data']['id']
                        postTitle = res['data']['children'][j]['data']['title']
                        postSubreddit = res['data']['children'][j]['data']['subreddit_name_prefixed']
                        postUrl = res['data']['children'][j]['data']['url']
                        postAuthor = res['data']['children'][j]['data']['author']
                        postPoints = res['data']['children'][j]['data']['score']
                        postComments = res['data']['children'][j]['data']['num_comments']

                        # Post type
                        postIsYoutube = False
                        postIsText = False
                        postIsImageGif = res['data']['children'][j]['data']['domain']
                        postIsVideo = res['data']['children'][j]['data']['domain']
                        postIsVideo = True if postIsVideo.__eq__(
                            "v.redd.it") else False
                        postIsYoutube = True if postUrl.find(
                            "youtu") > 0 else False

                        postIsImageGif = True if postIsImageGif.__eq__(
                            "i.redd.it") else False
                        postIsText = False if postIsVideo or postIsYoutube or postIsImageGif else True

                        # For discord embed (Thumbnail)
                        tPT = res['data']['children'][j]['data']['thumbnail']
                        postThumbnail = tPT if tPT != "null" and tPT != "nsfw" else postUrl

                        # If this post is youtube url
                        if postIsYoutube:
                            postThumbnail = res['data']['children'][j]['data']['media']['oembed']['thumbnail_url']

                        # Insert all posts to postsList to return it
                        postsList.append([postID, postSubreddit, postTitle, postUrl, postThumbnail, postIsVideo,
                                          postIsYoutube, postIsImageGif, postIsText, postAuthor, postPoints, postComments])

                        # print(f"** (ID:{postID}) IsVideo: {postIsVideo} | IsYoutube: {postIsYoutube} | IsImageGif: {postIsImageGif} | IsText: {postIsText} **\n")

                except Error as e:
                    print("Error in <redditClass.py> ->", e)

            # Insert posts to database
            self.insert(postsList)

        except Error as e:
            print("There is no posts (redditClass.py) -> ", e)
        return postsList

    # Get all reddit posts in db
    def get(self, t = 0):
        sql = f"SELECT * FROM {self.tableName}"

        cursor = self.connection.cursor()
        cursor.execute(sql)
        getPosts = cursor.fetchall()

        if t == 0:
            for post in getPosts:
                print(f"\n********************\n{post}\n********************\n")
        elif t == 1:
            for post in getPosts:
                print(f"{post[2]} {post[6]} {post[7]} {post[8]} {post[9]} {post[10]} {post[11]} {post[12]}")