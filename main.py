import discord
from discord.ext import commands
import requests

# Discord bot token
TOKEN = 'INPUT_TOKEN_HERE'
GUILD_ID = 'INPUT_GUILD_ID'  # Replace with your Discord server's ID
TICKET_MASTER_API_KEY = 'INPUT_TICKET_MASTER_API_KEY'

# Define your intents
intents = discord.Intents.default()
intents.message_content = True  # Required if you want to access message content


# Create the bot client instance
client = commands.Bot(command_prefix='$', intents=intents)


@client.event
async def on_ready():
    print(f'Logged in as {client.user}')
    guild = discord.Object(id=GUILD_ID)  # Replace with your server's ID
    client.tree.clear_commands(guild=guild)  # Clear old commands
    comm = await client.tree.sync(guild=guild)  # Sync commands again
    print(f"Slash commands synced with server: {GUILD_ID}")
    print(f"Commands: {[command.name for command in comm]}")


@client.command(name="test")
async def test(ctx):
    await ctx.send(f"This is a test command.")


# Command to check concert tickets for a specific artist
@client.command(name="search")
async def search_artist(ctx, arg):

    # Example API request to Ticketmaster (replace with actual API call)
    response = requests.get(
        f"https://app.ticketmaster.com/discovery/v2/events.json?keyword={arg}&apikey={TICKET_MASTER_API_KEY}")
    events = response.json().get('_embedded', {}).get('events', [])

    if events:
        event_url = events[0]['url']
        message = f"Tickets are now available for {arg}! Check it out here: {event_url}"
        await ctx.send(message)
    else:
        await ctx.send(f"No tickets found for {arg}.")


# Run the bot
client.run(TOKEN)
