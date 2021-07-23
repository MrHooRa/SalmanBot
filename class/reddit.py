from inspect import getcallargs
from discord.ext import tasks, commands
from logs import *
from db import *
import requests

# Get env values
from decouple import config

class Reddit(commands.Cog):
    """Reddit api"""

    def __init__(self, bot, BOT_DETAILS):
        self.bot = bot
        self.BOT_DETAILS = BOT_DETAILS
        self.logs = Logs(name="reddit.py")
        self.db = DB(config('DB_USERNAME'), config('DB_PASSWORD'),
                     config('DB_NAME'), config('DB_HOSTNAME'))
        self.db.connect()

    @commands.Cog.listener()
    async def on_ready(self):
        self.logs.log("Reddit is ready!", True)
        self.redditChannel = self.bot.get_channel(self.BOT_DETAILS['reddit_channel'])

        self.req = self.request(config('REDDIT_CLIENT_ID'), config('REDDIT_CLIENT_SECRET'),
                                config('REDDIT_USERNAME'), config('REDDIT_PASSWORD'), config('REDDIT_USERAGENT'))

        self.updateToken.start(True)
        if self.req:
            self.updateReddit.start()

    @tasks.loop(seconds=6600)
    async def updateToken(self, starting=False):
        """Update reddit token every ~2 hours"""
        if not starting:
            self.req = self.request(config('REDDIT_CLIENT_ID'), config('REDDIT_CLIENT_SECRET'),
                                    config('REDDIT_USERNAME'), config('REDDIT_PASSWORD'), config('REDDIT_USERAGENT'))

    @tasks.loop(seconds=60)
    async def updateReddit(self):
        """Get reddit posts from specific subreddit"""
        await self.update("HolUp", 'hot', 4)
        await self.update("CrazyFuckingVideos", 'hot', 4)
        await self.update("maybemaybemaybe", 'hot', 4)
        await self.update("nonononoyes", 'hot', 4)

    def request(self, client_id, secret_token, username, password, userAgent='SalmanBot 0.1'):
        try:
            # authenticate API
            auth = requests.auth.HTTPBasicAuth(client_id, secret_token)

            data = {
                'grant_type': 'password',
                'username': username,
                'password': password
            }

            # setup our header info, which gives reddit a brief description of our app
            headers = {'User-Agent': userAgent}

            # send our request for an OAuth token
            res = requests.post('https://www.reddit.com/api/v1/access_token',
                                auth=auth, data=data, headers=headers)

            # convert response to JSON and pull access_token value
            TOKEN = res.json()['access_token']

            # add authorization to our headers dictionary
            self.headers = {**headers, **{'Authorization': f"bearer {TOKEN}"}}

            # while the token is valid (~2 hours) we just add headers=headers to our requests
            requests.get('https://oauth.reddit.com/api/v1/me',
                         headers=self.headers)
            return True
        except Exception as e:
            self.logs.log(
                f"Can not request access_token. -> Exception: {e}", True, "Error")
            return False

    @commands.Cog.listener()
    async def update(self, subreddit: str, type='new', limit=10, table_name='reddit'):
        """Update reddit posts and push it into text channel"""

        res = requests.get(f"https://oauth.reddit.com/r/{subreddit}/{type}",
                           headers=self.headers, params={'limit': limit})

        nbOfPosts = 0
        for post in res.json()['data']['children']:
            # Check if this post already posted!
            if self.db.is_connected():
                con = self.db.connection
                try:
                    # post id
                    post_id = post['data']['id']
                    sql = f'SELECT `post_id` FROM {table_name} WHERE `post_id` = \'{post_id}\''

                    cursor = con.cursor()
                    cursor.execute(sql)
                    getAllPosts = list(cursor.fetchall())
                    cursor.close()

                    # If this post did not posted
                    if not getAllPosts:
                        
                        details = {
                            'id': post['data']['id'],
                            'subreddit': post['data']['subreddit'],
                            'title': post['data']['title'],
                            'author': post['data']['author'],
                            # 'url': f"https://www.reddit.com/r/{post['data']['subreddit']}/{post['data']['id']}",
                            'url': f"https://www.reddit.com/r/{post['data']['subreddit']}/comments/{post['data']['id']}",
                            'is_video': post['data']['is_video']
                        }

                        # Send this post to reddit channel in discord (Only vidoes!)
                        if details['is_video'] == 1:
                            nbOfPosts+=1
                            await self.redditChannel.send(details['url'])
                            # Insert this post into database
                            self.insert(details, "reddit")

                except Exception as e:
                    self.logs.log(
                        f'Can not update reddit posts. -> Exception: {e}', False, type='Error')
        if nbOfPosts > 0:
            self.logs.log(f"Update {nbOfPosts} post(s) (From: {subreddit}) successfully!", True)

    # Insert to database
    def insert(self, val, table_name):
        """Insert reddit posts to database"""
        if self.db.is_connected():
            con = self.db.connection
            cursor = con.cursor()

            sql = f"INSERT INTO `{table_name}` (post_id, subreddit, title, author, url, is_video) VALUES (%s, %s, %s, %s, %s, %s)"
            vals = (val['id'], val['subreddit'], val['title'],
                    val['author'], val['url'], val['is_video'])
            try:
                cursor.execute(sql, vals)
                con.commit()
                cursor.close()

                return True
            except Error as e:
                self.logs.log(
                    f"Did not insert to database. -> Exception: {e}", True, type="Error")
                return False
