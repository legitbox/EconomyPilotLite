import sqlite3

from endstone_economy_pilot_lite.config import check_config, load_config
from endstone import ColorFormat
from pathlib import Path


database_directory = "endstone"

check_config()
currency = load_config()

directory_path = Path('databases/economy-pilot/')

if not directory_path.exists():
    directory_path.mkdir(parents=True, exist_ok=True)

# this function creates the main table if it doesn't exist
# The table stores player's uuid as a KEY, username for command usage and money
def check_main_table():
    connection = sqlite3.connect(f'{directory_path}/database.db')
    cursor = connection.cursor()
    command = """
    CREATE TABLE IF NOT EXISTS database(
    uuid TEXT PRIMARY KEY,
    username TEXT,
    money INTEGER DEFAULT 0 NOT NULL
    );
    """
    cursor.execute(command)
    connection.commit()
    connection.close()

# this function creates a database entry in the table if the user joined for the first time or his entry got deleted
def check_user_data(uuid, username):
    connection = sqlite3.connect(f'{directory_path}/database.db')
    cursor = connection.cursor()
    command = """
    INSERT OR IGNORE INTO database (uuid, username)
    VALUES (?, ?);
    """
    cursor.execute(command, (str(uuid), str(username)))
    connection.commit()
    connection.close()

# this function fetches the amount of money the user has and returns it to the main.py script
def fetch_balance(username):
    connection = sqlite3.connect(f'{directory_path}/database.db')
    cursor = connection.cursor()
    cursor.execute("SELECT money FROM database WHERE username = ?;", (str(username),))

    balance = str(cursor.fetchone()).replace("(", "").replace(")", "").replace(",", "")
    connection.commit()
    connection.close()

    return balance

# this function checks for username changes in the server, so if a player changes their username, they wouldn't loose their money
def check_player_username_for_change(uuid, unchecked_username):
    connection = sqlite3.connect(f'{directory_path}/database.db')
    cursor = connection.cursor()
    cursor.execute("SELECT username FROM database WHERE uuid = ?;", (str(uuid),))

    database_username = str(cursor.fetchone()).replace("(", "").replace(")", "").replace(",", "")
    if database_username != unchecked_username:
        cursor.execute("""
        UPDATE database
        SET username = ?
        WHERE uuid = ?;
        """, (str(unchecked_username), str(uuid)))

    connection.commit()
    connection.close()

# basically the entire transaction engine, sends money from one user to another
def pay_to_player(sender_username, reciever_username, amount) -> str:
    connection = sqlite3.connect(f'{directory_path}/database.db')
    cursor = connection.cursor()

    return_string = f"{ColorFormat.RED}You don't have that much money to send{ColorFormat.RESET}"


    cursor.execute("SELECT EXISTS(SELECT 1 FROM database WHERE username = ?)", (str(reciever_username),))
    reciever_exists = int(cursor.fetchone()[0])
    if reciever_exists == 0:
        return_string = f"{ColorFormat.RED}This user isnt logged in the database{ColorFormat.RESET}"
        connection.close()
        return return_string

    cursor.execute("SELECT money FROM database WHERE username = ?;", (str(sender_username),))
    sender_balance = str(cursor.fetchone()).replace("(", "").replace(")", "").replace(",", "")

    if str(reciever_username) == str(sender_username):
        return_string = f"{ColorFormat.RED}You cannot send money to yourself{ColorFormat.RESET}"
        connection.close()
        return return_string

    if abs(int(sender_balance)) - int(amount) < 0:
        connection.close()
        return return_string

    else:
        cursor.execute("UPDATE database SET money = money - ? WHERE username = ?;", (abs(int(amount)), str(sender_username)))
        cursor.execute("UPDATE database SET money = money + ? WHERE username = ?;", (abs(int(amount)), str(reciever_username)))
        return_string = f"{ColorFormat.GOLD}You have sent {ColorFormat.AQUA}{abs(int(amount))}{currency}{ColorFormat.RESET}{ColorFormat.GOLD} to {ColorFormat.GREEN}{reciever_username}{ColorFormat.RESET}"

    connection.commit()
    connection.close()
    return return_string

# this function sets the players balance
def set_balance(username, balance) -> str:
    connection = sqlite3.connect(f'{directory_path}/database.db')
    cursor = connection.cursor()

    cursor.execute("SELECT EXISTS(SELECT 1 FROM database WHERE username = ?)", (str(username),))
    reciever_exists = int(cursor.fetchone()[0])
    if reciever_exists == 0:
        return_string = f"{ColorFormat.RED}This user isnt logged in the database{ColorFormat.RESET}"
        connection.close()
        return return_string

    return_message = f"{ColorFormat.GOLD}Player's {ColorFormat.GREEN}{username}{ColorFormat.RESET} {ColorFormat.GOLD}balance was set to {ColorFormat.AQUA}{balance}{currency}{ColorFormat.RESET}"

    cursor.execute("UPDATE database SET money = ? WHERE username = ?;", (abs(int(balance)), str(username)))

    connection.commit()
    connection.close()
    return return_message

# it's like the /pay command but it can be sent from a non player, must be op though
def server_pay(username, amount) -> str:
    connection = sqlite3.connect(f'{directory_path}/database.db')
    cursor = connection.cursor()

    cursor.execute("SELECT EXISTS(SELECT 1 FROM database WHERE username = ?)", (str(username),))
    reciever_exists = int(cursor.fetchone()[0])
    if reciever_exists == 0:
        return_string = f"{ColorFormat.RED}This user isnt logged in the database{ColorFormat.RESET}"
        connection.close()
        return return_string

    cursor.execute("UPDATE database SET money = money + ? WHERE username = ?;",(abs(int(amount)), str(username)))
    return_string = f"{ColorFormat.GOLD}The Server has sent {ColorFormat.AQUA}{abs(int(amount))}{currency}{ColorFormat.RESET}{ColorFormat.GOLD} to {ColorFormat.GREEN}{username}{ColorFormat.RESET}"

    connection.commit()
    connection.close()
    return return_string

# this command lets the server deduct from the player's balance
def server_deduct(username, amount) -> str:
    connection = sqlite3.connect(f'{directory_path}/database.db')
    cursor = connection.cursor()

    cursor.execute("SELECT EXISTS(SELECT 1 FROM database WHERE username = ?)", (str(username),))
    reciever_exists = int(cursor.fetchone()[0])
    if reciever_exists == 0:
        return_string = f"{ColorFormat.RED}This user isnt logged in the database{ColorFormat.RESET}"
        connection.close()
        return return_string

    cursor.execute("UPDATE database SET money = money - ? WHERE username = ?;",(abs(int(amount)), str(username)))
    return_string = f"{ColorFormat.GOLD}The Server has deducted {ColorFormat.AQUA}{abs(int(amount))}{currency}{ColorFormat.RESET}{ColorFormat.GOLD} from {ColorFormat.GREEN}{username}{ColorFormat.RESET}"

    connection.commit()
    connection.close()
    return return_string

# lets the server fetch the player's balance
def server_balance_fetch(username) -> str:
    connection = sqlite3.connect(f'{directory_path}/database.db')
    cursor = connection.cursor()

    cursor.execute("SELECT EXISTS(SELECT 1 FROM database WHERE username = ?)", (str(username),))
    reciever_exists = int(cursor.fetchone()[0])
    if reciever_exists == 0:
        return_string = f"{ColorFormat.RED}This user isnt logged in the database{ColorFormat.RESET}"
        connection.close()
        return return_string

    cursor.execute("SELECT money FROM database WHERE username = ?;", (str(username),))
    return_string = str(cursor.fetchone()).replace("(", "").replace(")", "").replace(",", "")
    connection.commit()
    connection.close()

    return return_string

# Nukes and recreates the database
def nuke_database():
    connection = sqlite3.connect(f'{directory_path}/database.db')
    cursor = connection.cursor()
    command1 = """
    DROP TABLE IF EXISTS database;
    """
    command2 = """
    CREATE TABLE IF NOT EXISTS database(
    uuid TEXT PRIMARY KEY,
    username TEXT,
    money INTEGER DEFAULT 0 NOT NULL
    );
    """
    cursor.execute(command1)
    cursor.execute(command2)
    connection.commit()
    connection.close()