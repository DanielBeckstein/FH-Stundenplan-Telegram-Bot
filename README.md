# FH Stundenplan Telegramm Bot

# Description

 This is code for a Telegram bot in python.
 The bot listens for changes to the Stundenplan 
 (course table) of the FH Hof (University of Applied Sciences - Hof)
 When a change occurs, bot posts messages to telegram groups

# Description of files

- start_bot.py [starts the bot]
- bot.py [contains bot functions]
- mypkl.py [makes pickle-functions nicer - util tool]
- link.txt [url to read Stundenplan (course table) from]

- conf.py [contains telegram auth token and telegram id of admin]
- conf_sample.py [contains example code for conf.py file]
    to start bot :
        - rename conf_sample.py to conf.py 
        - put your token in it
        - add conf.py to your .gitignore file
        
# Further work

- cooldown function for bot (stop bot from writing more than one message, each 2 hours)
- custom bot configuration for students in other majors (not only Allgemeine Informatik)

[I am currently not going to implement this, feel free to send a pull request]
