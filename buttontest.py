import telepot
from telepot.loop import MessageLoop
from telepot.namedtuple import InlineKeyboardMarkup, InlineKeyboardButton

TOKEN = '5995420796:AAFLGPoYyOYaLl5xtGRDneXhOe35foKHCWw'

def handle_message(msg):
    content_type, chat_type, chat_id = telepot.glance(msg)
    
    if content_type == 'text':
        if msg['text'] == '/start':
            send_button(chat_id)
        elif msg['text'] == '/help':
            send_help(chat_id)
        elif msg['text'] == '/helloworld':
            send_message(chat_id, 'Hello, World!')
    
    elif content_type == 'callback_query':
        query_id = msg['id']
        query_data = msg['data']
        message_id = msg['message']['message_id']
        chat_id = msg['message']['chat']['id']
        
        if query_data == 'red':
            send_message(chat_id, 'You chose red')
        elif query_data == 'blue':
            send_message(chat_id, 'You chose blue')
        
        # Optional: Answer the callback query to remove the "loading" status
        bot.answerCallbackQuery(query_id)
        # Optional: Edit the original message to remove the button
        bot.editMessageReplyMarkup((chat_id, message_id))

# Rest of the code...



def send_button(chat_id):
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='Red', callback_data='red')],
        [InlineKeyboardButton(text='Blue', callback_data='blue')]
    ])
    
    bot.sendMessage(chat_id, 'Choose a color:', reply_markup=keyboard)

def send_message(chat_id, text):
    bot.sendMessage(chat_id, text)

def send_help(chat_id):
    help_text = 'This is a simple bot. Use the following commands:\n\n' \
                '/start - Show the color selection button\n' \
                '/help - Show help information\n' \
                '/helloworld - Print "Hello, World!"\n'
    send_message(chat_id, help_text)

# Create a bot instance
bot = telepot.Bot(TOKEN)

# Set up the message handling loop
MessageLoop(bot, handle_message).run_as_thread()

print('Bot is running...')

# Keep the program running
while True:
    pass
