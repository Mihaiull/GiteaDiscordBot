import os
from dotenv import load_dotenv
import discord

load_dotenv()  # load variables from .env

DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
CHANNEL_ID = int(os.getenv("DISCORD_CHANNEL_ID"))

intents = discord.Intents.default()
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f"Logged in as {client.user}")
    channel = client.get_channel(CHANNEL_ID)
    if channel:
        await channel.send("✅ Test message: bot is working!")
    await client.close()  # exit after sending

client.run(DISCORD_TOKEN)
