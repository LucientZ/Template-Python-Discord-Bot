import discord
from discord.ext import commands

client = commands.Bot(command_prefix = '$')

@client.event
async def on_ready():
    print("Bot is ready.")

@client.command
async def ping(ctx):
    await ctx.channel.send(f"Pong! {int(client.latency * 1000)} ms")

def write_token(TOKEN) -> None:
    """
    Writes a token to .token.
    If .token does not exist, creates .token and writes the token.

    Parameters:
    TOKEN (str): Token to be written to file

    Returns:
    None
    """
    tokenfile = open(".token", "w")
    tokenfile.write(TOKEN)
    tokenfile.close()

def get_token() -> str:
    """
    Obtains token from a file named '.token' or from the user.
    If '.token' does not have a token or is empty, asks the user if they would like to write to '.token'

    Parameters:
    None

    Returns:
    str: token to be used by bot
    """
    # Initializes TOKEN and choice as strings
    TOKEN = ""
    choice = ""

    #At the moment, this code assumes the only error is .token not existing
    try:
        # opens up .token which should only contain the bot token
        with open('.token') as tokenfile:
            print("Logging in with TOKEN from .token")
            TOKEN = tokenfile.read()

            if(TOKEN == ""):
                # If TOKEN == "", this means that .token is empty
                
                while(choice != "Y" and choice != "n"):
                    choice = input("\nIt looks like there isn't anything in '.token'.\nWould you like to add a token to this file? (It is recommended that this is done manually) [Y/n] ")
                
                if(choice == 'Y'):
                    TOKEN = input('\nPlease enter the bot token: ')
                    write_token(TOKEN)
                else:
                    print(f"\nNo token will be added to '.token'")
                    TOKEN = input('Please enter the bot token: ')                
    except OSError:
        # Handling when .token does not exist.
        while(choice.lower() != "y" and choice.lower() != "n"):
            choice = input("\nIt looks like there isn't a file named '.token' in this directory.\nWould you like to create this file? [Y/n] ")

        if(choice.lower() == 'y'):
            TOKEN = input('\nPlease enter the bot token: ')
            write_token(TOKEN)
        else:
            print("\n.dat will not be created")
            TOKEN = input('Please enter the bot token: ')

    return TOKEN

def main():
    # Obtain token for bot login

    # Attempt to login with token
    try:
        TOKEN = get_token()
        client.run(TOKEN)
    except discord.LoginFailure as e:
        #This error is raised when the token is not valid
        print("[ERROR] Issue logging into bot:",e,'\n')
        print("The program will exit.\n")
        choice = input("Would you like to enter a new token? [Y/n] ")
        while(choice.lower() != "y" and choice.lower() != "n"):
            choice = input("\nWould you like to write a new token? [Y/n] ")    
        if(choice.lower() == "y"):
            TOKEN = input("Please enter bot token: ")
            write_token(TOKEN)
        print("Terminating program...\n")
        exit()
    except Exception as e:
        print("[ERROR] Issue logging into bot:",e,'\n')
        print("Terminating program...\n")
        exit()



if __name__ == '__main__':
    main()
