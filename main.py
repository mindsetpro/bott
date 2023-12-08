import discord
from discord.ext import commands
import requests
from bs4 import BeautifulSoup

intents = discord.Intents.all()
bot = commands.Bot(command_prefix=";", intents=intents)

@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')

@bot.command(name='start', help='start your Dragon Ball Adventure!')
async def start_game(ctx):
    # Create an embed for starting character information
    embed = discord.Embed(
        title='<:Super_Recovery_Drink:1182699471591706664> Game Start <:Super_Recovery_Drink:1182699471591706664>',
        description='Choose your character:',
        color=0x7289DA  # Discord's blurple color
    )

    # Add starter characters
    starter_characters = ['Vegeta', 'Goku']
    characters_string = '\n'.join([f'• {char}' for char in starter_characters])
    embed.add_field(name='Starter Characters', value=characters_string, inline=False)
    
    # Set the footer
    embed.set_footer(text='DBZ Dokkan RV')

    # Send the embed with character information
    start_message = await ctx.send(embed=embed)

    # Ask for the user's choice
    await ctx.send('To choose your character, type the name of your selection.')

    def check(message):
        return message.author == ctx.author and message.channel == ctx.channel

    try:
        # Wait for the user to respond with their character choice
        choice_msg = await bot.wait_for('message', check=check, timeout=30)
        character_choice = choice_msg.content.capitalize()

        # Check if the chosen character is valid
        if character_choice in starter_characters:
            # Get the character image from the Dragon Ball Wiki
            image_url = get_character_image_url(character_choice)
            
            # Add the character image to the embed
            embed.set_image(url=image_url)

            # Send the updated embed
            await ctx.send(f'You have chosen {character_choice}! Let the adventure begin!', embed=embed)
        else:
            await ctx.send('Invalid choice. Please run !start again and choose a valid character.')

    except TimeoutError:
        await ctx.send('Character selection timed out. Please run !start again.')

# Function to get character image URL from Dragon Ball Wiki
def get_character_image_url(character_name):
    base_url = 'https://dragonball.fandom.com/wiki/'
    formatted_name = character_name.replace(' ', '_')
    full_url = f'{base_url}{formatted_name}'

    try:
        response = requests.get(full_url)
        soup = BeautifulSoup(response.text, 'html.parser')
        image_tag = soup.find('img', {'class': 'pi-image-thumbnail'})
        image_url = image_tag['src'] if image_tag else None
        return image_url
    except Exception as e:
        print(f'Error fetching character image: {e}')
        return None
        
import os

token = os.getenv('TOKEN')
if token is not None:
    bot.run(token)
else:
    print("Error: TOKEN environment variable is not set.")

