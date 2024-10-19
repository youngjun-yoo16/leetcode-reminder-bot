# leetcode-reminder-bot 🤖

A simple Discord bot that sends a daily reminder at 9 PM to solve one LeetCode problem, with a motivational message to help your ass stay consistent.

## Setup 🛠

### Prerequisites
- Python 3.8 or higher
- A Discord account with a server where you can add the bot
- A Discord bot token (from the [Discord Developer Portal](https://discord.com/developers/applications))

### Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/your-username/leetcode-reminder-bot.git
    ```

2. Navigate to the project directory:
    ```bash
    cd leetcode-reminder-bot
    ```

3. Install the dependencies:
    ```bash
    pip install -r requirements.txt
    ```

4. Create a `.env` file in the root directory and add the following environment variables:
    ```env
    DISCORD_TOKEN=your_discord_bot_token
    CHANNEL_ID=your_channel_id
    USER_ID=your_user_id
    ```

### Running the Bot

To run the bot locally, use the following command:
```bash
python3 main.py
```