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


class round:
    def __init__(self, player1, player2):
        self.player1 = player1
        self.player2 = player2

    p1_option = ""   # 0 - none, 1 - rock, 2 - paper, 3 - scissors
    p2_option = ""

    def choose(self, player, option):    # 0 - not ready yet, 1 - player1 wins, 2 - player2 wins, 3 - tie
        if(player == self.player1):
            p1_option = option
        else:
            p2_option = option

        if(p1_option != "" and p2_option != ""):
            if(p1_option == p2_option): 
                return 3
            if(p1_option == "paper" and p2_option == "scissors"):
                return 2
            if(p1_option == "scissors" and p2_option == "paper"):
                return 1
            if(p1_option < p2_option):
                return 1
            else:
                return 2
        
        return 0

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

def game_options():
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
        style = 4,
        custom_id = "quit",
        label = "Quit"
    )

    return ActionRow(components = [rock_button, paper_button, scissors_button, quit_button])  

@bot.component("sp")
async def primary_component(ctx: interactions.ComponentContext):
    action_row = game_options()

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
    game_msg = await ctx.edit(f"This lobby was started by {ctx.author.mention}...", components = [action_row])
    player1 = ctx.author
    @bot.component("join")
    async def success_container(ctx: interactions.CommandContext):
        if(player1 == ctx.author):
            await ctx.send("You have already joined the game!", ephemeral = True)
        else:
            await ctx.send("You have successfully joined the game!", ephemeral = True)
            player2 = ctx.author
            
            current_round = round(player1, player2)

            await game_msg.edit("Rock, paper, scissors!", components = game_options())

            @bot.component("quit")
            async def danger_component(ctx: interactions.CommandContext):
                if(ctx.author != player1 and ctx.author != player2):
                    await ctx.send("You cannot quit other people's games!", ephemeral = True)
                else:
                    await game_msg.edit("Game over!", components = [])

            result = 0

            @bot.component("rock")
            async def primary_component(ctx: interactions.CommandContext):
                if((ctx.author == player1 and current_round.p1_option != 0) or (ctx.author == player2 and current_round.p2_option != 0)):
                    await ctx.send("You have already made your decision!", ephemeral = True)
                else:
                    result = current_round.choose(ctx.author, 1)
            
            @bot.component("paper")
            async def primary_component(ctx: interactions.CommandContext):
                if((ctx.author == player1 and current_round.p1_option != 0) or (ctx.author == player2 and current_round.p2_option != 0)):
                    await ctx.send("You have already made your decision!", ephemeral = True)
                else:
                    result = current_round.choose(ctx.author, 2)

            @bot.component("scissors")
            async def primary_component(ctx: interactions.CommandContext):
                if((ctx.author == player1 and current_round.p1_option != 0) or (ctx.author == player2 and current_round.p2_option != 0)):
                    await ctx.send("You have already made your decision!", ephemeral = True)
                else:
                    result = current_round.choose(ctx.author, 3)

            if(result > 0):
                if(result == 1):
                    game_msg.edit(f"The winner is {player1.mention} . . .\n{player1.mention} chose {current_round.p1_option} and {player2.mention} chose {current_round.p2_option}.", components = [])
                if(result == 2):
                    game_msg.edit(f"The winner is {player2.mention} . . .\n{player1.mention} chose {current_round.p1_option} and {player2.mention} chose {current_round.p2_option}.", components = [])   
                if(result == 3):
                    await game_msg.edit(f"The game is a tie! Nobody wins . . .\nBoth players chose {current_round.p1_option}.") 
        

    await game_msg.edit()





@bot.command()
@is_owner()
async def shutdown(ctx):
    await ctx.send("Shutting bot down ... :(")
    exit()

    
bot.start()