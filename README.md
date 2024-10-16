![logo](https://github.com/legitbox/EconomyPilotLite/blob/main/bitmap.png?raw=true)
# EconomyPilotLite<br>
This is a system/api plugin for an economy system for the endstone server software<br>

### Features<br>
- multithreaded SQLite database for fast and simple operations<br>
- the ability to use commands as an api to interact with other plugins<br>
- you can use custom symbols for currency<br>

### Installation<br>
Drag and drop the .whl file that you can get from releases and put it in your endstone's plugin folder<br>

### File Structure<br>
```
config/
├─ economy-pilot-lite.toml
databases/
├─ economy-pilot/
│  ├─ database.db
```
<br>
- Configuration file `economy-pilot-lite.toml`<br>
- Database file `database.db`<br>

### Command usage<br>
- Player commands<br><br>
`/balance or /bal` - if executed by the player it will give the players current balance
<br><br>
`/pay <username: str> <amount: int>` - if executed by the player it will let the player pay money to an another user, <br>for example `/pay legtibox7811 150`

- Server commands [needs op]<br>
`/serverpay <player: str> <amount: int>` - if executed by the server it will transfer money to the players balance, <br>for example `/serverpay legitbox7811 150`
<br><br>
`/serverdeduct <player: str> <amount: int>` - if executed by the server it will deduct money from the players balance, <br>for example `/serverdeduct legitbox7811 150`
<br><br>
`/serverbalance <player: str>` - if executed by the server it will show the selected player's balance, <br>for example `/serverlbalance legitbox7811`
<br><br>
`/setbalance <player: str> <balance: int>` - if executed by the server it will set the players balance to what you have selected, <br>for example `/setbalance legitbox7811 0`
<br><br>
`/deluser <player: str>` - if executed by the server it will remove the user's data from the database, <br>for example `/deluser legitbox7811`
<br><br>
`/nukedatabase` - WARNING!!! Nukes the database and stops the server

