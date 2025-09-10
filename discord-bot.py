# bot.py
import os
import discord
from fastapi import FastAPI, Request
import uvicorn
import threading
import asyncio
import json
import queue
from dotenv import load_dotenv

load_dotenv()
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
CHANNEL_ID = int(os.getenv("DISCORD_CHANNEL_ID"))

intents = discord.Intents.default()
client = discord.Client(intents=intents)

app = FastAPI()
message_queue = queue.Queue()


async def process_message_queue():
    """Process messages from the queue and send to Discord"""
    while True:
        try:
            if not message_queue.empty():
                title, url, author = message_queue.get_nowait()
                print(f"📤 Sending PR notification: {author}")

                # Wait for client to be ready
                await client.wait_until_ready()

                # Fetch the channel safely
                channel = client.get_channel(CHANNEL_ID)
                if channel is None:
                    channel = await client.fetch_channel(CHANNEL_ID)

                if channel:
                    # Create a rich embedded message
                    embed = discord.Embed(
                        title="🔄 New Pull Request",
                        description=f"**{title}**",
                        color=0x00ff00,  # Green color
                        url=url
                    )

                    # Add author information
                    embed.add_field(
                        name="👤 Author",
                        value=f"**{author}**",
                        inline=True
                    )

                    # Extract repository info from title
                    repo_info = title.split(']')[0].replace('[', '') if ']' in title else "Unknown Repository"
                    embed.add_field(
                        name="📁 Repository",
                        value=f"`{repo_info}`",
                        inline=True
                    )

                    # Extract PR number from title if available
                    pr_number = None
                    if '#' in title:
                        try:
                            pr_number = title.split('#')[1].split(' ')[0]
                            embed.add_field(
                                name="🔢 PR Number",
                                value=f"#{pr_number}",
                                inline=True
                            )
                        except:
                            pass

                    # Add footer with timestamp
                    embed.timestamp = discord.utils.utcnow()

                    await channel.send(embed=embed)
                    print("✅ PR notification sent to Discord")
                else:
                    print(f"❌ Could not find Discord channel {CHANNEL_ID}")

        except queue.Empty:
            pass
        except Exception as e:
            print(f"❌ Error sending Discord notification: {e}")

        # Check queue every second
        await asyncio.sleep(1)

@app.post("/gitea")
async def gitea_webhook(request: Request):
    payload = await request.json()

    title = None
    url = None
    author = None

    # Check for embeds in the payload (Gitea Discord webhook format)
    if "embeds" in payload and isinstance(payload["embeds"], list) and len(payload["embeds"]) > 0:
        embed = payload["embeds"][0]
        title = embed.get("title", "No title")
        url = embed.get("url", "")
        author = embed.get("author", {}).get("name", "Unknown")

    # Check for native Gitea pull request format
    elif "pull_request" in payload:
        pr = payload["pull_request"]
        title = pr.get("title", "No title")
        url = pr.get("html_url", "")
        author = pr.get("user", {}).get("login", "Unknown")

    # Send Discord message if we found pull request data
    if title and url and author:
        print(f"📥 Received webhook: PR by {author}")
        message_queue.put((title, url, author))
    else:
        print("⚠️ No pull request data found in webhook")

    return {"status": "ok"}

@client.event
async def on_ready():
    print(f"✅ Bot logged in as {client.user}")
    # Start the message queue processor
    asyncio.create_task(process_message_queue())

def run_discord_bot():
    client.run(DISCORD_TOKEN)

if __name__ == "__main__":
    threading.Thread(target=run_discord_bot, daemon=True).start()
    uvicorn.run(app, host="0.0.0.0", port=8234)
