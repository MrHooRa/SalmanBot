# SalmanBot 0.1v :smiley:
  
 (SalmanBot) for discord servers.

▶️ This bot working in python 3.9.6+ and Discord version 1.7.3

▶️ My twitter: @MrHoora

 Setup (On windows):
 -
 - Step 1: Create .env file in the same main.py directory contain:
  ```
  TOKEN=    <- Your discord app token

  REDDIT_CLIENT_ID=     <- Reddit client id
  REDDIT_CLIENT_SECRET= <- Reddit client secret
  REDDIT_USERNAME=      <- Reddit login username
  REDDIT_PASSWORD=      <- Reddit login password
  REDDIT_USERAGENT=SalmanBot

  DB_NAME=      <- Database name
  DB_USERNAME=  <- Database username
  DB_PASSWORD=  <- Database password
  DB_HOSTNAME=  <- Database hostname

  CUTTLY_KEY=   <- cuttly api key (You can create free account from https://cutt.ly/)
  ```
 - Step 2: Run ``` py main.py ```

:heavy_check_mark: What this bot can do?
-
* Temp channels.
* TTS (Text To Speech).
* Special commands (Clear, Wheel).
* Reddit posts (You can choose what subreddit you want!)

⭐ Upcoming features:
-
- Statistics reports & data visualization by using online database.
- Math equations.

📎 Updates:
-
- New commands structure and create commands.py contains all commands used by discord users.
- Add corg system to main.py.
- New temp channel task.
- tts command work perfect. Bot will leave after end of speech immediately.
- Temp channel admin can manage channel (Edit channel name, limit and delete it!). Alos can disconnect anyone in it own channel!
- Add prefix command for server admins to change bot prefix.
- New reddit posts class.
- Database class to make easy connections.
- Add tts prevent spam.

🧰 Fixes:
-
- Temp channel method now work with no errors (In the past, user will face error when delete channel by its own side!).
- SalmanBot will reply to member when used tts while it's not in voice channel.
- Fix on_ready issues (sometimes bot call on_ready randomly).
- Fix reddit.py issues (Sometimes request get error).
- Fix reddit class block SalmanBot (Stop bot around 20 seconds) by using aiohttp package.

🔴 Knowing issues:
-
- The bot don't work smothe, maybe because mysql queries or something in reddit.py.