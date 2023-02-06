#This bot was created using Chat GPT LOL

# There are several platforms that allow you to host your Discord bot for free, including:

# Heroku: A cloud platform that supports multiple programming languages and is easy to use. You can host your bot on Heroku by creating a new app, deploying your code, and running the bot on a dyno (Heroku's virtual machine).

# Repl.it: An online coding environment that allows you to host your code for free. You can host your Discord bot on Repl.it by creating a new project, uploading your code, and running the bot from the Repl.it terminal.

# Glitch: A web-based platform for building and hosting web applications. You can host your Discord bot on Glitch by creating a new project, uploading your code, and running the bot from the Glitch terminal.

# These platforms offer limited resources for free, so you may want to consider a paid option if you need more power for your bot.


import asyncio
import tweepy
import requests
import discord

# Discord setup
client = discord.Client()
discord_channel_id = <insert Discord channel ID>

# Twitter setup
twitter_consumer_key = <insert Twitter consumer key>
twitter_consumer_secret = <insert Twitter consumer secret>
twitter_access_token = <insert Twitter access token>
twitter_access_token_secret = <insert Twitter access token secret>
twitter_username = <insert Twitter username>

auth = tweepy.OAuthHandler(twitter_consumer_key, twitter_consumer_secret)
auth.set_access_token(twitter_access_token, twitter_access_token_secret)
api = tweepy.API(auth)
twitter_user_id = api.get_user(twitter_username).id

# Twitch setup
twitch_client_id = <insert Twitch client ID>

# YouTube setup
youtube_api_key = <insert YouTube API key>

# Function to post new tweets to Discord
def on_tweet(status):
    if status.user.screen_name == twitter_username:
        tweet_url = f'https://twitter.com/{status.user.screen_name}/status/{status.id}'
        message = f'New tweet: "{status.text}" - {tweet_url}'
        discord_channel = client.get_channel(discord_channel_id)
        asyncio.run_coroutine_threadsafe(discord_channel.send(message), client.loop)

# Set up a Twitter stream to listen for new tweets
class TweetStreamListener(tweepy.StreamListener):
    def on_status(self, status):
        on_tweet(status)

stream_listener = TweetStreamListener()
stream = tweepy.Stream(auth=api.auth, listener=stream_listener)
stream.filter(follow=[twitter_user_id])

# Function to handle new YouTube videos
async def handle_new_youtube_video(video_id):
    response = requests.get(
        f'https://www.googleapis.com/youtube/v3/videos?part=snippet&id={video_id}&key={youtube_api_key}'
    ).json()

    video_title = response['items'][0]['snippet']['title']
    video_url = f'https://www.youtube.com/watch?v={video_id}'

    channel = client.get_channel(discord_channel_id)
    await channel.send(f'New YouTube video: "{video_title}" - {video_url}')

# Function to handle new Twitch streams
async def handle_new_twitch_stream(stream_id):
    response = requests.get(
        f'https://api.twitch.tv/helix/streams?id={stream_id}',
        headers={
            'Client-ID': twitch_client_id
        }
    ).json()

    stream_title = response['data'][0]['title']
    stream_url = f'https://www.twitch.tv/{response["data"][0]["user_name"]}'

    channel = client.get_channel(discord_channel_id)
    await channel.send(f'New Twitch stream: "{stream_title}" - {stream_url}')
