import discord  # The main library to interact with Discord's API
import asyncio  # To run asynchronous tasks like sending messages on schedule
import schedule # To manage daily scheduling tasks
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

TOKEN = os.getenv('DISCORD_TOKEN')
CHANNEL_ID = int(os.getenv('CHANNEL_ID'))
USER_ID = int(os.getenv('USER_ID'))

# Set up the bot with the appropriate intents to send and read messages
intents = discord.Intents.default()
intents.message_content = True  # This allows the bot to interact with message content

client = discord.Client(intents=intents)

# Function to send the daily reminder
async def send_reminder():
    await client.wait_until_ready()  # Ensure bot is fully ready before sending a message
    channel = client.get_channel(CHANNEL_ID)
    user = await client.fetch_user(USER_ID)

    # Log to check if the function is being called
    print(f"Attempting to send reminder to {user} in {channel}")

    if channel and user:
        try:
            # Send a message to the channel and mention the user
            await channel.send(f"{user.mention}, it's 9 PM! Time to solve a LeetCode problem! 🚀\n"
                               f'💡 *Remember: One LeetCode a day keeps unemployment away!*')

            print("Reminder sent successfully")
        except Exception as e:
            print(f"Error sending reminder: {e}")
    else:
        print("Channel or User not found")

# Function to define the schedule for sending reminders at 9 PM every day
def schedule_reminder():
    # Schedule the task to run every day at 9 PM (21:00)
    schedule.every().day.at("05:50").do(
        asyncio.run_coroutine_threadsafe, send_reminder(), client.loop
    )

# Background task that constantly checks if the scheduled time has been reached
async def scheduled_task():
    # Continuously run the schedule check every second
    while True:
        schedule.run_pending()  # Check if any scheduled tasks need to be run
        await asyncio.sleep(1)  # Wait 1 second before checking again

# Event when bot is ready and logged in
@client.event
async def on_ready():
    print(f'Logged in as {client.user}')
    
    # Print channel and user to verify they are correct
    print(f"Channel: {client.get_channel(CHANNEL_ID)}")
    print(f"User: {await client.fetch_user(USER_ID)}")
    
    # Start scheduling the reminder
    schedule_reminder()
    # Start the scheduled task loop
    client.loop.create_task(scheduled_task())

# Event when bot gets disconnected
@client.event
async def on_disconnect():
    print("Bot disconnected from Discord")

# Start the bot using the token
client.run(TOKEN)
