# Use official Python image
FROM python:3.12-slim

# Set working directory
WORKDIR /app

# Install dependencies
RUN pip install --no-cache-dir fastapi uvicorn[standard] discord.py python-dotenv

# Copy bot files
COPY discord-bot.py ./
COPY .env ./

# Expose port 8234
EXPOSE 8234

# Run the bot
CMD ["python", "discord-bot.py"]
