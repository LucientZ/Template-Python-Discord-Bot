import discord
from discord import app_commands

class aclient(discord.Client):
    def __init__(self):
        super().__init__(command_prefix = 's-', activity = discord.Game(name = "s-help"), intents=discord.Intents.all())
        self.synced = False

    async def on_ready(self):
        await self.wait_until_ready()
        if not self.synced:
            await tree.sync(guild = discord.Object(id = get_token(".syncid", "Command Syncing")))
            self.synced = True
        print(f"Bot is ready and logged in as {self.user}.")

client = aclient()
tree = app_commands.CommandTree(client)


@tree.command(name = "ping", description = "says client latency")
async def slash_ping(ctx: discord.Interaction, name: str):
    await ctx.response.send_message(f"Pong! {int(client.latency * 1000)} ms")

def write_token(TOKEN: str, filename: str) -> None:
    """
    Writes a token to a specified file.
    If filename does not exist, creates filename and writes the token.

    Parameters:
    TOKEN (str): Token to be written to file
    filename (str): File for TOKEN to be written

    Returns:
    None
    """
    with open(filename, "w") as tokenfile:
        tokenfile.write(TOKEN)
        tokenfile.close()

def get_token(filename: str, use_case = "Unspecified") -> str:
    """
    Obtains token from a file specified asks the user.
    If the file does not have a token or is empty, asks the user if they would like to write to the file

    Parameters:
    filename (str): name of file to be used in obtaining token

    Returns:
    str: token to be used by bot
    """
    # Initializes TOKEN and choice as empty strings
    TOKEN = ""
    choice = ""

    #Currently, this code assumes the only error is the file not existing
    try:
        # opens up filename which should only contain the bot token
        with open(filename) as tokenfile:
            print(f"Using token from '{filename}' for use case: {use_case}")
            TOKEN = tokenfile.read()

            if(TOKEN == ""):
                # If TOKEN == "", this means that the file is empty
                
                while(choice.lower() != "y" and choice.lower() != "n"):
                    choice = input(f"\nIt looks like there isn't anything in '{filename}'.\nWould you like to add a token to this file? [Y/n] ")
                
                if(choice.lower() == 'y'):
                    TOKEN = input('\nPlease enter the bot token: ')
                    write_token(TOKEN, filename)
                else:
                    print(f"\nNo token will be added to '{filename}'")
                    TOKEN = input('Please enter the bot token: ')                
    except OSError:
        # Handling when the file does not exist.
        while(choice.lower() != "y" and choice.lower() != "n"):
            choice = input(f"\nIt looks like there isn't a file named '{filename}' in this directory.\nWould you like to create this file? [Y/n] ")

        if(choice.lower() == 'y'):
            TOKEN = input('\nPlease enter the bot token: ')
            write_token(TOKEN, filename)
        else:
            print("\n.dat will not be created")
            TOKEN = input('Please enter the bot token: ')

    return TOKEN

def main():
    # Obtain token for bot login

    # Attempt to login with token
    try:
        TOKEN = get_token(".token", "Logging In")
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
            write_token(TOKEN, ".token")
        print("Terminating program...\n")
        exit()
    except Exception as e:
        print("[ERROR] Issue logging into bot:",e,'\n')
        print("Terminating program...\n")
        exit()



if __name__ == '__main__':
    main()
