# Defualts packages
import os

# Discord packages
import discord
from discord.ext import tasks

# For reddit api
import requests
import json

# Mysql db
import mysql.connector
from mysql.connector import Error

# Get database login details
host = os.getenv('DB_HOSTNAME')
user = os.getenv('DB_USERNAME')
password = os.getenv('DB_PASSWORD')
database = os.getenv('DB_NAME')

class Posts():
    def __init__(self, redditUsername, sortBy="new", postsLimit=25, redditPostFileName="reddit_posts.txt"):
        # IMPORTANT NOTE: You should choose sortBy (top, new, popular) from the beginning or you will lost some posts
        self.rtUsername = redditUsername
        self.sBy = sortBy
        self.pLimit = postsLimit
        self.rPFN = redditPostFileName

    def update(self, connection, conn = None):
        connection = connection if connection != None else conn
        link = 'https://reddit.com/user/IHooRa/upvoted.json?sort=new&limit=25'

        # Send get request
        r = requests.get(link, headers={'User-agent': 'SalamnBot 0.1'})

        # Get all json on it
        res = json.loads(r.text)

        # old -> new
        allPosts = []
        toSavePosts = []

        # Count upvote posts
        countposts = len(res['data']['children'])

        # Get last id
        with open('reddit_posts.txt', 'r') as f:
            lines = f.read().splitlines()
            lastID = lines[-1] if len(lines) > 0 else 0

        counter = 0
        duplicatedCounter = 0
        # send last upvoted posts
        for i in range(countposts):
            # Get post id
            postID = res['data']['children'][i]['data']['id']

            isDuplicatedPost = False

            # Check if this post is duplicated or not
            for k in range(len(lines)):
                if postID == lines[-k]:
                    isDuplicatedPost = True

            # If duplicated, pass it
            if isDuplicatedPost:
                # print(f"Duplicated post {postID}")
                duplicatedCounter += 1
                pass
            else:
                # Get post details
                postTitle = res['data']['children'][i]['data']['title']
                postSubreddit = res['data']['children'][i]['data']['subreddit_name_prefixed']
                postUrl = res['data']['children'][i]['data']['url']
                postAuthor = res['data']['children'][i]['data']['author']
                postPoints = res['data']['children'][i]['data']['score']
                postComments = res['data']['children'][i]['data']['num_comments']

                # For videos
                postIsVideo = False
                postIsYoutube = False
                postIsText = False
                postIsImageGif = False

                tPT = res['data']['children'][i]['data']['thumbnail']
                postThumbnail = tPT if tPT != "null" and tPT != "nsfw" else postUrl
                postIsVideo = res['data']['children'][i]['data']['is_video']
                postIsYoutube = True if postUrl.find("youtu") > 0 else False
                postIsText = False if postIsVideo or postIsYoutube or postIsImageGif else True
                postIsImageGif = False if postIsVideo or postIsYoutube else True

                if postIsYoutube:
                    postThumbnail = res['data']['children'][i]['data']['media']['oembed']['thumbnail_url']

                # Set last id with this post id
                toSavePosts.append(postID)
                lastID = postID

                # Send to discord this post
                # print(f"ID = {postID} -> {postSubreddit} | {postTitle}\n{postUrl}\n----------------------------------------\n")
                allPosts.append([postID, postSubreddit, postTitle, postUrl, postThumbnail, postIsVideo,
                                 postIsYoutube, postIsImageGif, postAuthor, postPoints, postComments, postIsText])
                counter += 1

        # # Save all sent posts to reddit_posts.txt
        # with open("reddit_posts.txt", "a") as a_file:
        #     for ll in range(len(toSavePosts)):
        #         if len(toSavePosts) != 0:
        #             a_file.write(f"{toSavePosts[ll]}\n")

        # Insert all reddit posts to database
        try:
            if connection.is_connected():
                # db_Info = connection.get_server_info()
                # print("Connected to MySQL Server version ", db_Info)
                cursor = connection.cursor()

            # YOUR CODE HERE
            for i in range(len(allPosts)):
                mySql_insert_query = f"INSERT INTO `discordBot_redditPosts` (`id`, `postId`, `subreddit`, `title`, `url`, `thumbnail`, `IsVideo`, `IsYoutube`, `IsImageGif`, `IsText`, `author`, `points`, `comments`) VALUES (NULL, '{allPosts[i][0]}', '{allPosts[i][1]}', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1')"
                cursor.execute(mySql_insert_query)

            connection.commit()
            print(cursor.rowcount, "Record inserted successfully into discordBot_redditPosts table")
            cursor.close()

        except Error as e:
            print("Error while connecting to MySQL", e)
        # Return posts count
        return counter, duplicatedCounter, allPosts