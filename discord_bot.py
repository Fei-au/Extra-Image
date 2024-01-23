import discord
import xlwings as xw
from discord.ext import tasks

# Discord bot token
BOT_TOKEN = 'MTEzNTY0MTk1NDEzMTExNjEwNQ.G0rfGN.8XbR_A7t6u9ZQtV5M0kvvkRKbNjz2z9qdMFvZc'
EXCEL_PATH = "AmazonExtraction -Auction2.xlsm"

# Create intents to specify which events your bot should listen to
intents = discord.Intents.default()
intents.message_content = True  # Enable message content reading

# Connect to the open Excel workbook using xlwings
app = xw.apps.active  # This will connect to the existing Excel application
workbook = app.books[EXCEL_PATH]  # Connect to the existing workbook by file path
sheet = workbook.sheets.active

# Discord bot client
client = discord.Client(intents=intents)


# Heartbeat interval in seconds (e.g., 60 seconds for a heartbeat every minute)
HEARTBEAT_INTERVAL = 60


@tasks.loop(seconds=HEARTBEAT_INTERVAL)
async def send_heartbeat():
    # This function will run every HEARTBEAT_INTERVAL seconds
    pass


@send_heartbeat.before_loop
async def before_send_heartbeat():
    await client.wait_until_ready()


@send_heartbeat.after_loop
async def after_send_heartbeat():
    print("Heartbeat task stopped.")


@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')
    send_heartbeat.start()  # Start the heartbeat task when the bot is ready


@client.event
async def on_message(message):
    # Check if the message is from the desired channel and not from the bot itself
    if message.channel.name == 'bot-amazon' and not message.author.bot:
        print("yay")
        content = str(message.content)
        if content[0] == '0':
            content = "'" + content
        # Find the first empty row in column A
        row_number = sheet.range('A1').end('down').row + 1
        # Write the message to the Excel file
        sheet.range(f'A{row_number}').value = content


# Run the bot
client.run(BOT_TOKEN)
