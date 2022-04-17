<p align="center">
  <a href="" rel="noopener">
 <img width=200px height=200px src="https://user-images.githubusercontent.com/43346016/163686086-15297ceb-c506-48b4-8dc1-3bdece598fb6.jpg" alt="WhaBot Logo"></a>
</p>

<h3 align="center">WhaBot</h3>

<div align="center">

  [![Status](https://img.shields.io/badge/status-active-success.svg)]() 
  [![PyPI version](https://badge.fury.io/py/WhaBot.svg)](https://badge.fury.io/py/WhaBot)
  [![License](https://img.shields.io/badge/license-MIT-blue.svg)](/LICENSE)

</div>

<p align="center"> The (not so official) WhatsApp automation framework!
    <br> 
</p>

## 📝 Table of Contents
- [About](#About)
- [Getting Things Ready](#Starting)
- [Usage](#Usage)
- [TODO](../TODO.md)
- [Contributing](../CONTRIBUTING.md)
- [Authors](#Authors)
- [Disclaimer](#Disclaimer)

## 🧐 About <a name = "About"></a>
WhaBot is a framework that automates all the tasks that a human can do on WhatsApp! 

It's created to _(somehow)_ create powerfull bots in this platform, as we can do in others as Discord, Slack, Telegram, etc.

## 🏁 Getting Things Ready <a name = "Starting"></a>
If you follow this easy step by step guide, you will get you a copy of the project up and running on your local machine for development and testing purposes.

```bash
# Python 3.6+ required
python -m venv .venv
source .venv/bin/activate

pip install -U pip
pip install WhaBot
```

Also, the Core of this framework is Selenium, that's why you need to download a chromedriver binary that works with your chromium based browser and matches the correct version. You can find more information about this steup [here](https://chromedriver.chromium.org/getting-started#h.p_ID_36).

### Prerequisites
For you to create a functional bot, you will need a WhatsApp account. We recommend a WhatsApp Bussiness account and a phone number just dedicated to run the bot.

### Running it
After installing the framework via pip and downloading the correct chromedriver, we are ready to go!


Here is an example code to create a simple bot!

```python
from WhaBot import *

WhaBot = WhaBot(
	driver_location = os.getcwd() + "/drivers/chrome", # The location of your driver
	stored_session= os.getcwd() + "/wsp_session" # My whatsapp stored session folder
	)

chat = "Myself" # Change this to a contact from your contact lists! (This also works with phone numbers or groups!)

WhaBot.SendMessage(chat=chat, message="Hello!\nWe are up and running!!")
```
Once you have that done, here you have an actual bot, with 2 commands!

```python
import time
from WhaBot import *

WhaBot = WhaBot(
	binary_location = '/Applications/Brave Browser.app/Contents/MacOS/Brave Browser', #Since I'm using Brave for the chromedriver
	driver_location = os.getcwd() + "/chromedriver" # The location of your driver
	)

def HandleCommands(ctx):
	for contact in ctx:
		if WhaBot.CommandHandler(ctx=contact, command="!ping"):
			message = "Pong!\nWe are working fine!"
			WhaBot.SendMessage(chat=contact["Chat_Name"], message=message)

		elif WhaBot.CommandHandler(ctx=contact, command="!help"):
			message = f"Hey @{contact['Chat_Name']}!\nWe are still working in this option!\n\nStay tune for new updates!"
			WhaBot.SendMessage(chat=contact["Chat_Name"], message=message)

while __name__ == '__main__':
	unreads = SendMessage.GetUnreadChats(scrolls=10)
	HandleCommands(ctx=unreads)
	time.sleep(0.5)
```
That's it! You now have your first bot up and running, listening for 2 commands: `!ping` and `!help`, try them!!

## ⚙️ Usage <a name="Usage"></a>
The functions are very self-explained, but here is the list of functions and params!
 
| **Function** | **Params** | **Description** | **Returns** |
|:----------:|:--------:|:-------------:|:---------:|
|GetUnreadChats |  `scrolls:int` | Retrieeves the unread chats that the bot has | `[["Chat_Name":"Lanfran02", "Last_Message":"Hey!", "Time":"10:00", "Unreads":1, "is_group": FALSE]]` |
|GetMutedChats |  `scrolls:int` | Retrieves Muted Chats | `["Lanfran02", "A Group", "Another User"]` |
|GetPinnedChats | None | Retrieves Pinned Chats | `["Lanfran02", "An special contact"]` |
|GetLastMessagesFrom |  `chat:str` | Retrieves the last messages from a chat | `["Hey", "Don't forget to support!"]` |
|GetChatName | None | Retrieves the conversation name where the bot is | `"Lanfran02"` |
|SendMessage |  `chat:str` `message:str` | Send a message to a desired chat | _`boolean`_ |
|SendImage |  `chat:str` `message:str` `image:str` | Send a message with a local image attached to a desired chat | _`boolean`_ |
|SendDocument |  `chat:str` `document:str` | Send a message with a local document attached to a desired chat | _`boolean`_ |
|CommandHandler |  `ctx` `command:str` | Tries to find a desired command within the context | _`boolean`_ |
|BlockContact | `chat:str` | Block a desired contact | _`boolean`_ |
|UnblockContact | `chat:str` | Unblock a desired contact | _`boolean`_ |
|ExitGroup |  `group_name:str` | Exit a desired group | _`boolean`_ |
|ArchiveChat |  `chat:str` | Archive the desired chat | _`boolean`_ |
|PinChat |  `chat:str` | Pin the desired chat | _`boolean`_ |
|MuteChat |  `chat:str` `mute_time:str` | Mute the desired chat | _`boolean`_ |
|UnmuteChat |  `chat:str` | Unmute the desired chat | _`boolean`_ |
|ChangeTheme |  `theme:str` | Change the theme to `dark` or `light` | _`boolean`_ |
|TerminateSession | `sure:str` | Terminate the WhatsApp session | _`boolean`_ |
|CloseDriver | None | Closes the driver | _`void`_ |


To initiate the framework, you can pass a different set of variables:
| **Variable** | **Type** | **Default** | **Description** |
|:----------:|:--------:|:-------------:|
| wait | _int_ | `15` (seconds) | Is the waiting time for different objects, this may vary depending on your internet speed |
| reloaded | _boolean_ | `False` | If you have already a chromedriver session active, maybe you don't want to reload the WhatsApp page |
| binary_location | _str_ (PATH) | `None` | The binary location for your chromium based browser. (Tested with Chrome and Brave browser) |
| port | _int_ | `None` | The port where you have your chromium based browser running. This option is often used for debug purposes | 
| stored_session | _str_ (PATH) | `None`  * | The path where the Selenium session is stored. * The default path will be in the same folder and the name of the session will be "stored_session"|
| driver_location | _str_ (PATH) | `None` * | The path where your chromedriver is stored. * The default will be in the same folder as the bot is running with the name "chromedriver" |


## ✍️ Authors <a name = "Authors"></a>
- [@lanfran02](https://github.com/lanfran02) - Idea & Main developer

Feel free to contribute, you will be add to the the list of [contributors](https://github.com/lanfran02/WhaBot/contributors) who participated in this project!

## ⚖️ Disclaimer <a name = "Disclaimer"></a>
We, the developers, are not responsible for any illegal actions carried out through the use of this software or that do not comply with the WhatsApp code of conduct.

The material embodied in this software is provided to you "as-is" and without warranty of any kind, express, implied or otherwise, including without limitation, any warranty of fitness for a particular purpose.