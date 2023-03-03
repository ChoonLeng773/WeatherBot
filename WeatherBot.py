import os
from telegram.ext import Updater, CommandHandler
import pyowm
import config

owm = pyowm.OWM(config.api_key)

def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id,
     text="Hi! I'm a weather bot. Please send me your location so I can tell you the weather.")

def weather(update, context):
    user_location = update.message.location
    observation = owm.weather_at_coords(user_location.latitude, user_location.longitude)
    w = observation.weather
    temperature = w.temperature('celsius')['temp']
    description = w.detailed_status
    context.bot.send_message(chat_id=update.effective_chat.id, 
        text=f"The weather in your location is {temperature}°C and {description}.")

def main():
    updater = Updater(config.api_key, use_context=True) # why do we have use_context=True here?
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(Filters.location, weather))
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
