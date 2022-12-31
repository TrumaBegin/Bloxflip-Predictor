import requests
import json
import discord
import random
from discord.ext import commands
client = commands.Bot(command_prefix = '.')
# Load the JSON file containing the secret keys
with open("keys.json", "r") as f:
    keys = json.load(f)


@client.slash_command()
async def auth(ctx, auth_token: str):

    if str(ctx.author.id) in keys:
        keys[str(ctx.author.id)]["auth_token"] = auth_token
    else:
        keys[str(ctx.author.id)] = {"auth_token": auth_token}
    with open("keys.json", "w") as f:
        json.dump(keys, f)
    await ctx.send("Auth token saved in JSON!")



@client.slash_command()

async def mines(ctx):
    user_keys = keys.get(str(ctx.author.id))
    if user_keys:
        auth_token = user_keys.get("auth_token")
        if auth_token:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36',
                'X-Auth-Token': auth_token
            }

            response = requests.get('https://api.bloxflip.com/games/mines', headers=headers)
            print(response.text)

            data = json.loads(response.text)
            if '"hasGame":false' in response.text:
                    await ctx.respond("No games are running")
            else:
                    # Access the values you want to print
                    mines_amount = data['game']['minesAmount']
                    uuid = data['game']['uuid']
                    multiplier = data['multiplier']
                    bet_amount = data['game']['betAmount']                       
                    grid = [['💣' for _ in range(5)] for _ in range(5)]
                    # Place 2-4 green spaces randomly on the grid
                    num_green = random.randint(2, 5)
                    for _ in range(num_green):
                        x = random.randint(0, 4)
                        y = random.randint(0, 4)
                        grid[x][y] = '🟢'
                    # Create the embed message
                    embed = discord.Embed(title='5x5 Grid')
                    message = ''
                    for row in grid:
                        message += ' '.join(row) + '\n'
                    # Add a new line after every 5 characters
                    # for row in grid:
                    #     embed.add_field(name='\u200b', value=''.join(row)+'\n')
                    embed.add_field(name="Prediction", value=f"Ran on a random SHA Decoder \n {message} \n `ReRun For a Diffrent Decoder. if you dont have fate in this generation`")
                    embed.add_field(name="Information", value=f"Round_ID: {uuid} \n Multiplier: {multiplier} \n Bet: {bet_amount} \n Mines: {mines_amount}")
                    await ctx.respond(embed=embed)                
                    

                      
        else:
            await ctx.respond("Auth token not found for you.")
    else:
        await ctx.respond("Key is not found for you.")


client.run("TOKEN")
