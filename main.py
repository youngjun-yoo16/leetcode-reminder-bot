import discord  
import asyncio  
import schedule 
import random
import time
from dotenv import load_dotenv
import os

load_dotenv()

TOKEN = os.getenv('DISCORD_TOKEN')
CHANNEL_ID = int(os.getenv('CHANNEL_ID'))
USER_ID_1 = int(os.getenv('USER_ID_1'))  # First user ID
USER_ID_2 = int(os.getenv('USER_ID_2'))  # Second user ID

# Set up the bot with the appropriate intents to send and read messages
intents = discord.Intents.default()
intents.message_content = True  # This allows the bot to interact with message content

client = discord.Client(intents=intents)

motivational_messages = [
    "One LeetCode a day keeps unemployment away! 🚀",
    "FAANG dreams require LeetCode reality. Better get on it! 🐍",
    "Keep grinding, today's LeetCode problem is waiting! 💪",
    "Every solved problem is a step closer to proving you're unstoppable. 🔥",
    "Solve today's problem and save yourself from 'Why FAANG rejected me' Reddit threads. 📉",
    "If FAANG recruiters had a scoreboard, they'd see today's unsolved LeetCode problem. 😐",
    "LeetCoding is the closest you'll get to FAANG's 'easy' mode. Don't miss it. 🎮",
    "The longer you procrastinate, the easier you're making it for someone else to get that FAANG offer. 🚪",
    "Solve a LeetCode today, and future you will thank you! 🙌",
    "Your competition is LeetCoding right now. What are you doing? 😏",
    "Your competitors are solving LeetCode while you're... doing whatever this is. 💤",
    "Consistency is the key to success! Crack that LeetCode! 🔑",
    "LeetCode is just the price of admission to FAANG. Pay up! 💸",
    "Skip LeetCode today, and someone else will land your dream job. Take that in. 🧠",
    "LeetCode doesn't care about excuses, and neither do your future interviewers. Get it done! 🚀",
    "FAANG recruiters won't care how comfy your couch is. LeetCode, now! 🛋️",
    "This problem isn't hard, you've faced worse. Time to show it who's boss. 👊",
    "Every problem solved is a future interviewer impressed. Don't slack now. 🌟",
    "By all means, skip LeetCode. There's always next year's hiring cycle... maybe. 🕰️",
    "Solve LeetCode or get used to rejection - your choice. 💀",
    "You're right, today's LeetCode problem can wait. So can that job offer. 🚪",
    "Every unsolved problem is a recruiter crossing you off their list. 🔥",
    "LeetCode won't solve itself, but sure, pretend you're busy. 🙄",
    "Each LeetCode problem brings you closer to the life you're aiming for. Don't stop now! 🎯",
    "Every LeetCode problem you skip today is an opportunity lost tomorrow. Don't waste it. ⏳",
    "LeetCode's not for everyone... especially not for people who like being unemployed. 💼",
    "LeetCode isn't a chore, it's an investment in your future. Cash in today! 💰",
    "You're not just solving problems, you're building a career. Keep pushing! 🛠️",
    "Think of every LeetCode problem as a brick in the foundation of your success. Lay it down! 🧱",
    "You didn't come this far to only get this far. Smash that problem! 💥",
    "One more problem today could mean one less struggle tomorrow. Make it count! ⚡",
    "No one said it would be easy, but they did say it would be worth it. LeetCode awaits! 🌟",
    "Remember why you started - and keep going. This problem is just another stepping stone. 🚶‍♂️",
    "You're closer than you think. Today's LeetCode problem could be your breakthrough. 🚀",
    "LeetCode is your battleground. Conquer today's challenge and own your future! ⚔️",
    "The hardest part is showing up. You've got this. Now go solve that problem! 💪",
    "When it's hard, that's when you grow. Today's problem is building a stronger you. 🌱",
    "Every problem solved is a future interviewer impressed. Don't slack now. 🌟",
    "No LeetCode today? Looks like you're training to become a professional LinkedIn scroller. 📱",
    "Think of LeetCode as rent. You don't want to miss that payment. 🏠",
    "Skipping today's LeetCode? Good luck explaining that in your next interview. 😏",
    "LeetCode now or prepare to explain that gap on your resume. 😬",
    "Your future self is watching - solve that problem! 👀",
    "LeetCode now or practice saying, 'Do you want fries with that?' 🍟"
    "If you want a software engineer boyfriend/girlfriend, you need to be a software engineer first. 💻❤️"
]

# Function to send the daily reminder
async def send_reminder():
    await client.wait_until_ready()  # Ensure bot is fully ready before sending a message
    channel = client.get_channel(CHANNEL_ID)
    user1 = await client.fetch_user(USER_ID_1)
    user2 = await client.fetch_user(USER_ID_2)

    # Log to check if the function is being called
    print(f"Attempting to send reminder to {user1} and {user2} in {channel}")

    if channel and user1 and user2:
        try:
            # Randomly select a motivational message
            message = random.choice(motivational_messages)
            
            # Send a message to the channel and mention both users
            await channel.send(f"{user1.mention} and {user2.mention}, it's 11:44 PM! Time to solve a LeetCode problem! 🚀\n"
                               f'💡 *{message}*')
            print("Reminder sent successfully")
        except Exception as e:
            print(f"Error sending reminder: {e}")
    else:
        print("Channel or Users not found")

# Function to define the schedule for sending reminders at 9 PM every day
def schedule_reminder():
    # Schedule the task to run every day at 9 PM (21:00) EST
    # Railway run their servers in the UTC time zone: 01:00 UTC = 21:00 EST
    schedule.every().day.at("01:00").do(
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
    print(f"User 1: {await client.fetch_user(USER_ID_1)}")
    print(f"User 2: {await client.fetch_user(USER_ID_2)}")
    
    # Start scheduling the reminder
    schedule_reminder()
    # Start the scheduled task loop
    client.loop.create_task(scheduled_task())

# Handle disconnect event to log disconnections
@client.event
async def on_disconnect():
    print("Bot disconnected from Discord. Attempting to reconnect...")
    
# Handle reconnection or session resuming event
@client.event
async def on_resumed():
    print("Bot reconnected and resumed session.")

# Event when bot gets disconnected and attempts to reconnect automatically
@client.event
async def on_error(event, *args, **kwargs):
    print(f"An error occurred: {event} - {args if args else ''} {kwargs if kwargs else ''}")

# Run the bot with an auto-reconnect mechanism
def run_bot():
    while True:
        try:
            client.run(TOKEN)
        except Exception as e:
            print(f"Bot encountered an error: {e}")
            print("Reconnecting in 5 seconds...")
            time.sleep(5)  # Wait before attempting to reconnect

if __name__ == "__main__":
    run_bot()