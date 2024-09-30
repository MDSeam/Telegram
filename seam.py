import telebot
import os

Token = os.environ["Autha"]
bot1 = telebot.TeleBot(Token)


@bot1.message_handler(content_types="text")
def message_reply(message):
  if message.reply_to_message == None:
    bot1.forward_message("1906998334",message.chat.id,message.message_id)
  else:
    bot1.send_message(message.reply_to_message.forward_from.id,message.text)
  
def seam_main():
  print("seam starting......")
  bot1.infinity_polling()
