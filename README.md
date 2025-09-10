# Discord Bot for Gitea Pull Request Notifications

A Discord bot that receives webhooks from Gitea and sends formatted notifications to a Discord channel when pull requests are created or updated.

## Features

- 🔄 Receives Gitea webhooks for pull request events
- 📤 Sends rich embedded messages to Discord with PR details
- 🎨 Formatted notifications including author, repository, and PR number
- 🚀 FastAPI webhook endpoint for reliable message processing
- 🐳 Docker support for easy deployment

## Requirements

- Python 3.8+
- Discord bot token and channel access
- Publicly accessible endpoint for webhooks

## Setup

### 1. Discord Bot Setup

Create a Discord application and bot:

1. Go to the [Discord Developer Portal](https://discord.com/developers/applications)
2. Create a new application
3. Go to the "Bot" section and create a bot
4. Copy the bot token
5. Invite the bot to your server with "Send Messages" and "Embed Links" permissions

For detailed instructions, see the [official Discord bot creation guide](https://discord.com/developers/docs/getting-started).

### 2. Environment Configuration

The bot requires two environment variables:

- `DISCORD_TOKEN`: Your Discord bot token
- `DISCORD_CHANNEL_ID`: The Discord channel ID where notifications will be sent

You can set these in two ways:

#### Option A: Using a `.env` file (recommended)
Create a `.env` file in the project directory:

```env
DISCORD_TOKEN=your_discord_bot_token_here
DISCORD_CHANNEL_ID=1234567890123456789
```

#### Option B: Using shell environment variables
```bash
export DISCORD_TOKEN="your_discord_bot_token_here"
export DISCORD_CHANNEL_ID="1234567890123456789"
```

### 3. Installation & Running

#### Method 1: Docker (Recommended)

1. Build the Docker image:
```bash
docker build -t discord-bot .
```

2. Run the container:
```bash
# Using .env file
docker run -d --name discord-bot -p 8234:8234 --env-file .env discord-bot

# Using environment variables
docker run -d --name discord-bot -p 8234:8234 \
  -e DISCORD_TOKEN="your_token" \
  -e DISCORD_CHANNEL_ID="your_channel_id" \
  discord-bot
```

#### Method 2: Direct Python Execution

1. Install dependencies:
```bash
pip install fastapi uvicorn[standard] discord.py python-dotenv
```

2. Run the bot:
```bash
python discord-bot.py
```

### 4. Hosting & Webhook Configuration

The bot runs a FastAPI server on port 8234 (configurable in the code). You'll need to:

1. **Make it publicly accessible**: Use a reverse proxy, tunnel service, or cloud hosting
   - Example: Tunnel through Cloudflare to `discord-bot.yourdomain.com`
   - The webhook endpoint will be available at: `https://discord-bot.yourdomain.com/gitea`

2. **Configure Gitea webhook**:
   - Go to your Gitea repository settings
   - Add a new webhook with URL: `https://discord-bot.yourdomain.com/gitea`
   - Set content type to `application/json`
   - Select "Pull request" events
   - The bot supports both Gitea's native webhook format and Discord webhook format

### 5. Testing

Use the included test script to verify your Discord bot setup:

```bash
python test.py
```

This will send a test message to your configured Discord channel.

## Configuration

### Port Configuration
To change the default port (8234), modify the last line in `discord-bot.py`:

```python
uvicorn.run(app, host="0.0.0.0", port=YOUR_PORT_HERE)
```

And update your Docker run command accordingly:
```bash
docker run -d --name discord-bot -p YOUR_PORT_HERE:YOUR_PORT_HERE discord-bot
```

## Supported Webhook Formats

The bot handles two webhook formats:

1. **Gitea native format**: Direct pull request webhooks from Gitea
2. **Discord webhook format**: If you're using Gitea's Discord webhook integration

## 🤝 Contributions Welcome!

We love contributions! Whether it's fixing bugs, adding new features, improving documentation, or sharing ideas, your help makes this project better for everyone.

### How to Contribute

1. **Fork the repository** and create your branch from `main`
2. **Install dependencies** and test your changes locally
3. **Make your changes** and ensure they follow the existing code style
4. **Add tests** if your changes affect functionality
5. **Update documentation** if needed
6. **Submit a pull request** with a clear description of your changes

Currently, the bot focuses on pull request notifications, but it can handle many more webhook events. Feel free to extend it for other Gitea events like issues, merges, or pushes!

Please note that all contributions are reviewed, and I may ask for changes.

Thank you for considering contributing! 🚀

## License

This project is open source and available under the MIT License.
