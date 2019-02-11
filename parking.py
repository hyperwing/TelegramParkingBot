from os import listdir
from os.path import isfile, join
import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

#user interacting with bot id
telegram_user_id = 0
bot_chat_id=0
chat_to_send = 0

APItoken = '758991141:AAHmbVvfq3zFB-QWwIDhqn9FTEQ45xF1WR8'
bot = telebot.TeleBot(APItoken)
print ('starting tool')

def generateDay(monthCSV):
    for row in monthCSV:
        columns = row.split(',')
        day = dayMessage(columns[0], columns[1], columns[2],columns[3],columns[4])

    return day

def generateDayText(day):
    print('———————————————\n| %s, %s | \t |\n', day.month, day.day)

    
    print('———————————————\n| %s | \t |\n', day.startTimex, day.day)

class timeSlot:
    def __init__(self, time, occupants, exit):
        self.time = time
        self.occupants = occupants
        self.exit = exit

class dayMessage:
    def __init__(self, month, day, slots):
        self.month = month
        self.day = day
        self.slots = slots

#starts bot
@bot.message_handler(commands=['start', 'help'])
def handle_start_help(message):
    global bot_chat_id 

    bot_chat_id= message.chat.id

    print("chat_id: "+ str(bot_chat_id))

    bot.send_message(bot_chat_id, "/view or /add")
    pass


@bot.message_handler(commands=['view'])
def handle_date_selection(message):
    if bot.send_message(bot_chat_id, "Enter [month] and [day]", reply_markup=gen_markup()): 
        pass
    else:
        #exception
        print("exception")


@bot.message_handler(commands=['add'])
def handle_start_transfer(message):
    bot.send_message(bot_chat_id, "beginning transfer")


def gen_markup():
    markup = InlineKeyboardMarkup()

    #adds rows to the inline keyboard
    #number of weeks
    markup.row_width = len(6)
    
    for week in range(0, 6):
        name = "week of the %d", (week*7+1)
        markup.add(InlineKeyboardButton(name, callback_data= True))
    return markup

@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    global selectedConversation

    print("callback handler :"+call.data)
    index = int(call.data)

    for conversation in conversationNames:
        if conversationNames[index] == conversation:
            bot.answer_callback_query(call.id, conversation+" chosen")
            selectedConversation = str(allo_ids[index])
            print("alloID: "+str(selectedConversation))
            print("choice: "+conversationNames[index])

    bot.send_message(bot_chat_id, "send a telegram contact")


@bot.message_handler(func=lambda message: True)
def handle_convo(message):
    bot.send_message(bot_chat_id, "choose a chat method", reply_markup=gen_markup())



bot.polling()