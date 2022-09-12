import asyncio
import random
import interactions
from interactions import Button, ActionRow
from discord.ext.commands import Bot, is_owner
import os

from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

bot = interactions.Client(TOKEN)

class game:
    def __init__(self, guild, channel, player1, player2, p1score = 0, p2score = 0):
        self.guild = guild 
        self.channel = channel
        self.player1 = player1
        self.player2 = player2
        self.p1score = p1score
        self.p2score = p2score
    
games = []

@bot.event
async def on_ready():
    print("Ready!")

@bot.command(
    name = "rps",
    description = "Start a rock-paper-scissors game!",
)



async def rps(ctx: interactions.CommandContext):
    sp_button = Button(
        style = 1,
        custom_id = "sp",
        label = "Singleplayer", 
    )
    mp_button = Button(
        style = 1,
        custom_id = "mp",
        label = "Multiplayer"
    )
    action_row = ActionRow(components = [sp_button, mp_button])
    await ctx.send("Choose a game option!", components = action_row)
    

@bot.component("sp")
async def primary_component(ctx: interactions.ComponentContext):
    rock_button = Button(
        style = 1,
        custom_id = "rock",
        label = "Rock!"
    )
    paper_button = Button(
        style = 1,
        custom_id = "paper",
        label = "Paper!"
    )
    scissors_button = Button(
        style = 1,
        custom_id = "scissors",
        label = "Scissors!"
    )
    quit_button = Button(
        style = 1,
        custom_id = "quit",
        label = "Quit"
    )

    action_row = ActionRow(components = [rock_button, paper_button, scissors_button, quit_button])

    await ctx.edit("Rock, paper, scissors!", components = action_row)

    @bot.component("rock")
    async def primary_component(ctx: interactions.CommandContext):

        bot_choice = random.choice(["rock", "paper", "scissors"])
        if(bot_choice == "paper"):
            await ctx.send(f"{ctx.author.mention} The bot chose paper 🧻. You lost!")
        if(bot_choice == "rock"):
            await ctx.send(f"{ctx.author.mention} The bot chose rock 🪨. You tied!")
        if(bot_choice == "scissors"):
            await ctx.send(f"{ctx.author.mention} The bot chose scissors ✂️. You won!")
    
        

    @bot.component("paper")
    async def primary_component(ctx: interactions.CommandContext):
        bot_choice = random.choice(["rock", "paper", "scissors"])
        if(bot_choice == "paper"):
            await ctx.send(f"{ctx.author.mention} The bot chose paper 🧻. You tied!")
        if(bot_choice == "rock"):
            await ctx.send(f"{ctx.author.mention} The bot chose rock 🪨. You won!")
        if(bot_choice == "scissors"):
            await ctx.send(f"{ctx.author.mention} The bot chose scissors ✂️. You lost!")

    @bot.component("scissors")
    async def primary_component(ctx: interactions.CommandContext):
        bot_choice = random.choice(["rock", "paper", "scissors"])
        if(bot_choice == "paper"):
            await ctx.send(f"{ctx.author.mention} The bot chose paper 🧻. You won!") 
        if(bot_choice == "rock"):
            await ctx.send(f"{ctx.author.mention} The bot chose rock 🪨. You lost!")
        if(bot_choice == "scissors"):
            await ctx.send(f"{ctx.author.mention} The bot chose scissors ✂️. You tied!")

    @bot.component("quit")
    async def danger_component(ctx: interactions.CommandContext):
        await ctx.edit("Game over!", components = [])

@bot.component("mp")
async def primary_component(ctx: interactions.ComponentContext):
    join_button = Button(
        style = 3,
        custom_id = "join",
        label = "Join"
    )
    action_row = ActionRow(components = [join_button])
    await ctx.edit(f"This lobby was started by {ctx.author.mention}...", content = [action_row])


@bot.command()
@is_owner()
async def shutdown(ctx):
    exit()

    
bot.start()