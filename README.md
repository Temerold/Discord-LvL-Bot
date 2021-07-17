# Discord LvL-Bot

### This is a Discord bot. It has a leveling system that allows Discord server members to earn XP and levels, writing messages. It comes with a rebirth command, that allows the members to reset their levels and XP, in exchange for XP-earning bonuses.


## How to use

### 1. Create a Discord bot
If you don't already have a Discord account, go create one at https://discord.com. If (or when) you have an account, go to https://discord.com/developers/applications and create a new application. Go to the 'Bot' settings tab and click 'Add Bot'.
After you've created the bot, go to the 'OAuth2' settings tab and select 'bot' in 'Scopes'. Then, copy the link underneath, it looks something like this: https://discord.com/api/oauth2/authorize?client_id=xxxxxxxxxxxxxxxxxx&permissions=0&scope=bot. Use the link you copied to invite the bot to your Discord server. It needs no permissions, except being able to read messages.

### 2. Set up the code
Download the code, and input the token from the Discord application's 'Bot' settings tab into the auth.py file, as the `token` variable.

### 3. Run the code
Make sure you have Python 3.x installed, preferably the latest version - https://www.python.org/. If they're not already installed, install the following pip libraries:

| Library | PyPI link                            | Website                              |
| ------- | ------------------------------------ | ------------------------------------ |
| discord | https://pypi.org/project/discord.py/ | https://github.com/Rapptz/discord.py |

At last, run the bot.py file using Python 3.x and watch the magic happen!

## Notes
The default language is Swedish (since I'm from Sweden), and all the strings are in Swedish. However, all the comments and documentation are in English.
