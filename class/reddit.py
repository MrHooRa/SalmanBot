from inspect import getcallargs
import discord
from discord.embeds import Embed
from discord.ext import tasks, commands
from logs import *
from db import *
import requests
import urllib
import traceback
from decouple import config

#TODO: Remove all (self.logs.log(f"<*****> Full traceback -> {traceback.print_exc()}", True, "Error"))

class Reddit(commands.Cog):
    """Reddit api"""

    def __init__(self, bot, BOT_DETAILS):
        self.bot = bot
        self.BOT_DETAILS = BOT_DETAILS
        self.logs = Logs(name="reddit.py")
        self.db = DB(config('DB_USERNAME'), config('DB_PASSWORD'),
                     config('DB_NAME'), config('DB_HOSTNAME'))
        self.is_running = False

    @commands.Cog.listener()
    async def on_ready(self):
        if not self.is_running:
            self.logs.log("Reddit is ready!", True)
            self.redditChannel = self.bot.get_channel(
                self.BOT_DETAILS['reddit_channel'])
            self.is_running = True

        if not self.updateToken.is_running():
            self.updateToken.start()
        if not self.updateReddit.is_running():
            self.updateReddit.start()

    @tasks.loop(seconds=1800)
    async def updateToken(self):
        """Update reddit token every ~2 hours"""
        self.request(config('REDDIT_CLIENT_ID'), config('REDDIT_CLIENT_SECRET'),
                     config('REDDIT_USERNAME'), config('REDDIT_PASSWORD'), config('REDDIT_USERAGENT'))

    @tasks.loop(seconds=60)
    async def updateReddit(self):
        """Get reddit posts from specific subreddit"""
        try:
            await self.update("cat", 'hot', 10)
            await self.update("CrazyFuckingVideos", 'hot', 5)
            await self.update("maybemaybemaybe", 'hot', 5)
            await self.update("funnycats", 'hot', 10)
            await self.update("AnimalsBeingDerps", 'hot', 5)
        except Exception as e:
            self.logs.log(
                f"Something happened. -> Exception: {e}", True, "Error")
            self.logs.log(f"<updateReddit> Full traceback -> {traceback.print_exc()}", True, "Error")

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
            self.logs.log(f"<request> Full traceback -> {traceback.print_exc()}", True, "Error")
            self.logs.log(
                f"Can not request access_token. -> Exception: {e}", True, "Error")
            return False

    @commands.Cog.listener()
    async def update(self, subreddit: str, type='new', limit=10, table_name='reddit'):
        """Update reddit posts and push it into text channel."""
        posts = self.get_posts(subreddit, type, limit, table_name)
        if len(posts) > 0:
            for post in posts:
                await self.redditChannel.send(embed=post[1])
            self.logs.log(
                f"Update {len(posts)} post(s) (From: {subreddit}) successfully!", True)

    def get_posts(self, subreddit: str, type='new', limit: int = 10, table_name: str = 'reddit'):
        posts = []
        try:
            res = requests.get(f"https://oauth.reddit.com/r/{subreddit}/{type}",
                               headers=self.headers, params={'limit': limit})
            self.logs.log(f"<get_posts_res_testing> res={res}", True, "Testing")
        except Exception as e:
            self.logs.log(f"<get_posts_res> Full traceback -> {traceback.print_exc()}", True, "Error")
            if not self.request(config('REDDIT_CLIENT_ID'), config('REDDIT_CLIENT_SECRET'),
                                config('REDDIT_USERNAME'), config('REDDIT_PASSWORD'), config('REDDIT_USERAGENT')):
                self.logs.log(
                    f"(get_post) Can not request. -> Exception: {e}", True, "Error")
                return None
        # Check if database is connect
        try:
            if self.db.connect():
                con = self.db.connection
            else:
                return False
        except Exception as e:
            self.logs.log(f"<get_post_db> Full traceback -> {traceback.print_exc()}", True, "Error")
            self.logs.log(
                f"get_posts. connnection failed!. -> Exception: {e}", True, type="Error")

        # Get all posts from res
        try:
            res_json = res.json()['data']['children']
        except Exception as e:
            self.logs.log(f"<res_json> did not work.", True, "Error")

        for post in res_json:
            # Check if this post is already posted
            if self.check_post(con, post['data']['id'], table_name):
                details = {
                    'id': post['data']['id'],
                    'subreddit': post['data']['subreddit'],
                    'title': post['data']['title'],
                    'author': post['data']['author'],
                    'thumbnail': post['data']['thumbnail'],
                    'url': f"https://www.reddit.com/r/{post['data']['subreddit']}/comments/{post['data']['id']}",
                    'is_video': post['data']['is_video'],
                    'uniqueID': post['data']['url'].partition(".it/")[2].replace(".jpg", ""),
                    'permalink': post['data']['permalink']
                }
                embed = self.redditEmbed(details)
                if embed[0]:
                    posts.append([details, embed[1]])

                    # Insert to database
                    if not self.insert(details, 'reddit'):
                        self.logs.log(f"Can not insert.", True, type="Error")
                        return None

        if not self.db.close():
            self.logs.log("get_posts did not close database.", True, "Error")
        return posts

    def check_post(self, con, id, table_name):
        """Check post id from database"""
        try:
            cursor = con.cursor()
            cursor.execute(
                f'SELECT `post_id` FROM {table_name} WHERE `post_id` = \'{id}\'')
            get_post = list(cursor.fetchall())
        except Exception as e:
            self.logs.log(f"<check_post> Full traceback -> {traceback.print_exc()}", True, "Error")
            self.logs.log(
                f"check_posts failed. -> Exception: {e}", True, "Error")
        # If this post didn't post
        return not get_post

    def redditEmbed(self, details):
        """Create discord embed with reddit details (Videos only!)."""
        if details['is_video'] == 1:
            embed = discord.Embed(
                title=str(details['title']), url=str(details['url']), description=f"r/{details['subreddit']}")
            embed.set_author(
                name="Download", url=f"{self.cuttly_shorturl(details)}")
            if details['thumbnail'] != "nsfw":
                embed.set_image(url=details['thumbnail'])
            return True, embed
        return False, None

    def cuttly_shorturl(self, details):
        """Convert long url to short one with https://cutt.ly"""
        permalink = f"https://reddit.com{details['permalink']}"
        video_url = f"https://v.redd.it/{details['uniqueID']}/DASH_720.mp4?source=fallback"
        audio_url = f"https://v.redd.it/{details['uniqueID']}/DASH_audio.mp4?source=fallback"
        url = urllib.parse.quote(
            f"https://sd.redditsave.com/download.php?permalink={permalink}&video_url={video_url}&audio_url={audio_url}")
        r = requests.get(
            'http://cutt.ly/api/api.php?key={}&short={}'.format(self.BOT_DETAILS['cuttly_key'], url))
        return r.json()['url']['shortLink']

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
                self.logs.log(f"<insert> Full traceback -> {traceback.print_exc()}", True, "Error")
                self.logs.log(
                    f"Did not insert to database. -> Exception: {e}", True, type="Error")
                return False
