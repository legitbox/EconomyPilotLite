from endstone.plugin import Plugin
from endstone.event import event_handler, EventPriority, PlayerJoinEvent
from endstone.command import Command, CommandSender
from endstone import ColorFormat

from endstone_economy_pilot_lite.config import check_config, load_config
from endstone_economy_pilot_lite.database_controller import check_main_table, check_user_data, fetch_balance, \
    check_player_username_for_change, pay_to_player, set_balance, server_pay, server_deduct, server_balance_fetch, \
    nuke_database, delete_user

check_config()
currency = load_config()
version = "0.0.5"

class Main(Plugin):
    api_version = "0.5"


    commands = {
        "balance": {
            "description": "Gives the amount of money the player has",
            "usages": ["/balance"],
            "aliases": ["bal"],
            "permissions": ["economy_pilot_lite.command.balance"]
        },
        "pay": {
            "description": "Let's a player to pay another player",
            "usages": ["/pay <player: str> <amount: int>"],
            "permissions": ["economy_pilot_lite.command.pay"]
        },
        "serverpay": {
            "description": "Let's the Server to pay another player",
            "usages": ["/serverpay <player: str> <amount: int>"],
            "permissions": ["economy_pilot_lite.command.serverpay"]
        },
        "serverdeduct": {
            "description": "Let's a Server to deduct from an another player",
            "usages": ["/serverdeduct <player: str> <amount: int>"],
            "permissions": ["economy_pilot_lite.command.serverdeduct"]
        },
        "serverbalance": {
            "description": "Let's a Server to fetch the balance of an another player",
            "usages": ["/serverbalance <player: str>"],
            "permissions": ["economy_pilot_lite.command.serverbalance"]
        },
        "setbalance": {
            "description": "Lets the administrator set the balance of a player",
            "usages": ["/setbalance <player: str> <balance: int>"],
            "aliases": ["setbal"],
            "permissions": ["economy_pilot_lite.command.setbalance"]
        },
        "nukedatabase": {
            "description": "WARNING!!! Resets the database! STOPS THE SERVER!!!",
            "usages": ["/nukedatabase"],
            "permissions": ["economy_pilot_lite.command.nukedatabase"]
        },
        "deluser": {
            "description": "Deletes the selected user",
            "usages": ["/deluser <player: str>"],
            "permissions": ["economy_pilot_lite.command.deluser"]
        }
    }
    permissions = {
        "economy_pilot_lite.command.balance": {
            "description": "Allows the users to use the balance command",
            "default": True
        },
        "economy_pilot_lite.command.pay": {
            "description": "Allows the users to use the pay command",
            "default": True
        },
        "economy_pilot_lite.command.serverpay": {
            "description": "Allows the Server to use the paydeduct command",
            "default": "op"
        },
        "economy_pilot_lite.command.serverdeduct": {
            "description": "Allows the Server to use the serverdeduct",
            "default": "op"
        },
        "economy_pilot_lite.command.serverbalance": {
            "description": "Allows the Server to use the serverbalance",
            "default": "op"
        },
        "economy_pilot_lite.command.setbalance": {
            "description": "Allows the user to use the setbalance command",
            "default": "op"
        },
        "economy_pilot_lite.command.nukedatabase": {
            "description": "Allows the user to use nukedatabase",
            "default": "op"
        },
        "economy_pilot_lite.command.deluser": {
            "description": "Allows the user to delete a user from the database",
            "default": "op"
        }
    }
    def on_enable(self):
        self.register_events(self)

    def on_load(self):
        self.logger.info(f"""
        {ColorFormat.GOLD}
                                                                                       ╱|、
         ___  __   __        __                __          __  ___           ___  ___ (•˕ •7
        |__  /  ` /  \ |\ | /  \  |\/| \ /    |__) | |    /  \  |     |    |  |  |__   |、⁻〵ノ)
        |___ \__, \__/ | \| \__/  |  |  |     |    | |___ \__/  |     |___ |  |  |___  じしˍ,)ノ
        By Lunatechnika studios
        {ColorFormat.RESET}
        """)
        self.logger.info(f"{ColorFormat.GOLD}Version - {version}{ColorFormat.RESET}")
        self.logger.info(f"{ColorFormat.GOLD}Economy Pilot Lite has been loaded :3{ColorFormat.RESET}")
        self.logger.info(f"{ColorFormat.GOLD}Checking Database...{ColorFormat.RESET}")
        data_location = self.data_folder

        check_main_table()

    def on_disable(self):
        self.logger.info(f"{ColorFormat.GOLD}Closing Database Connection{ColorFormat.RESET}")
        self.logger.info(f"{ColorFormat.GOLD}Connection Closed, Shutting down!{ColorFormat.RESET}")

    @event_handler
    def on_player_join(self, event: PlayerJoinEvent):
        player = event.player
        self.logger.info(f"{ColorFormat.GOLD}Economy Pilot Lite is checking user's {ColorFormat.GREEN}{player.name}{ColorFormat.RESET} {ColorFormat.GOLD}records on the database{ColorFormat.RESET}")
        check_user_data(player.unique_id, player.name)
        check_player_username_for_change(player.unique_id, player.name)

    def on_command(self, sender: CommandSender, command: Command, args: list[str]):
        match command.name:
            case "balance":
                player = sender.name
                if player == "Server":
                    sender.send_message(f"{ColorFormat.RED}This command only can be ran by a player{ColorFormat.RESET}")
                else:
                    sender.send_message(f"{ColorFormat.GOLD}You have {ColorFormat.AQUA}{fetch_balance(player)}{currency}{ColorFormat.RESET}")
            case "pay":
                player = sender.name
                if player == "Server":
                    sender.send_message(f"{ColorFormat.RED}This command only can be ran by a player, use serverpay instead{ColorFormat.RESET}")
                else:
                    sender.send_message(f"{pay_to_player(player, args[0], args[1])}")
            case "setbalance":
                sender.send_message(f"{set_balance(args[0], args[1])}")
            case "serverpay":
                sender.send_message(f"{server_pay(args[0], args[1])}")
            case "serverdeduct":
                sender.send_message(f"{server_deduct(args[0], args[1])}")
            case "serverbalance":
                sender.send_message(f"{ColorFormat.GREEN}{args[0]}{ColorFormat.GOLD} has {ColorFormat.AQUA}{server_balance_fetch(args[0])}{currency}{ColorFormat.RESET}")
            case "nukedatabase":
                nuke_database()
                self.server.dispatch_command(self.server.command_sender, "stop")
            case "deluser":
                sender.send_message(f"{delete_user(args[0])}")
                self.server.dispatch_command(self.server.command_sender, f"kick {args[0]}")






