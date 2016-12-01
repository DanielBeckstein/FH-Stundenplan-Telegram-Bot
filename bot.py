import logging
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')             
import json

####################################
# Telegram python api
# -->   for how to install, see
#       pip install python-telegram-bot --upgrade
#       https://github.com/python-telegram-bot/python-telegram-bot
####################################
import telegram

# Imports configuration data from conf.py
import conf


def send_msg(msg, endpoints=[], flag_notify_admin_only = 0, flag_send = 1): 
               
    """
    FH-Stundenplan-Bot
    telegram.me/FH_Stundenplan_Bot
    """
    
    ####################################
    # Auth token from Telegram
    # -->   for how to get one, see
    #       https://core.telegram.org/bots#3-how-do-i-create-a-bot
    ####################################
    
    # token looks like this: 9873234:OWHIGEerjo3jh27khn....
    token =  conf.token
    
    ####################################
    # Id of telegram account from admin (yourself)
    # -->   for how to find your id, see
    #       http://stackoverflow.com/questions/31078710/how-to-obtain-telegram-chat-id-for-a-specific-user
    #       http://stackoverflow.com/questions/32683992/find-out-my-own-user-id-for-sending-a-message-with-telegram-api
    ####################################
    
    # id looks like this: 78925...
    id_my_admin = conf.id_my_admin
    
    # Init bot
    bot = telegram.Bot(token=token)
    me = bot.getMe()
    
    bot_msg = msg
    
    # Set parse mode
    # parse_mode = telegram.ParseMode.HTML, telegram.ParseMode.MARKDOWN
    parse_mode = None
    
    # Print bot message infos
    if 1:
        print "="*30
        print "  - Message - ", "to", endpoints
        try:
            print bot_msg
        except:
            print "ERROR: error occured, while printing msg"
        print "="*30
        
    # Flag to disable message sending
    if flag_send:
        # Flag to send message only to admin, not to any endpoints
        if flag_notify_admin_only:
            if id_my_admin != "":
                bot.sendMessage(chat_id=id_my_admin,text=bot_msg, parse_mode = parse_mode)
            else:
                print "WARNING: You did not enter a id_my_admin in conf.py - so no messages will be send to admin"
        else:
            for chat_id in endpoints:
                bot.sendMessage(chat_id=chat_id, text=bot_msg, parse_mode = parse_mode)
            
    # Print all messages that were send to bot by users
    if 0:
    
        # Fetch messages send to bot
        updates = bot.getUpdates()
        
        for i,update in enumerate(updates):
            msg = str(update)
            open("msg.json","a").write(msg+"\n")
            if 0:
                if i ==16:
                    print "="*40
                    print "="*10, "Message ", i
                    print "="*40
                    print type(u)
                    print msg
                    print ""
                    #open("msg.json","a").write(msg)
                    #parsed = json.loads(msg)
                    #print json.dumps(parsed, indent=3, sort_keys=True)

if __name__ == "__main__":    
    send_msg("t-test-",flag_send = 1)

