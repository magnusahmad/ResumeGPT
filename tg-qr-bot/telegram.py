import telebot
from usage_tracker import usage_db
import sqlite3
import os
from doc_handler import parse_document_for_bot, parse_document

import subprocess
#from agent import MyBot

BOT_TOKEN = '6104446946:AAE0t74qmKEHSvToKiOxzy-5C_YuhDPDIao'

bot = telebot.TeleBot(BOT_TOKEN)

# DB_FILE = os.path.join(os.path.dirname(__file__), 'chats.db') 

# def create_tables():
#   conn = sqlite3.connect(DB_FILE)
#   c = conn.cursor()  
#   c.execute('''
#     CREATE TABLE IF NOT EXISTS chat_log (
#       message_id INTEGER PRIMARY KEY,
#       chat_id INTEGER NOT NULL,  
#       message BLOB NOT NULL
#     )
#   ''')
#   conn.commit()
#   conn.close()

# open(DB_FILE, 'w').close()
# create_tables()  

# @bot.message_handler(commands=['greet']) 
# def greet(message):
#   print('second handler')
# @bot.message_handler(chat_types=['private'])
# def handle_private_chat(message):
#   print('first handler')


@bot.message_handler(content_types=["document"])
def handle_doc(message):
    try:
        file_info = bot.get_file(message.document.file_id)
        downloaded_file = bot.download_file(file_info.file_path)
        
        with open("input.docx", 'wb') as f:
            f.write(downloaded_file)
        
        #with open ("output.md", "wb") as fp:
            # Call pandoc to convert docx to md
        subprocess.run(["pandoc", "input.docx", "-o", "output.md"])
            #fp.write(pandoc_1)
        print("converted to md")

        # Send to bot
        pandoc_md = "output.md"
        parse_document_for_bot(pandoc_md)   

       # with open("output.docx", "wb") as fpp:
            # Convert bot response to doc
        bot_response_md = "chat.md"
        with open(bot_response_md, 'r') as f:
            first_char = f.read(1)
            if first_char == "`":
                with open(bot_response_md, 'r') as f:
                    lines = f.readlines()[1:-1]
                with open(bot_response_md, "w") as f:
                    f.writelines(lines)

        subprocess.run(["pandoc", bot_response_md, "-o", "output.docx"])
            #fpp.write(pandoc_2)
        print("converted to docx")

        # Send back md file
        with open("output.docx", "rb") as f:
            bot.send_document(message.chat.id, f)

        bot.reply_to(message, "Review complete! Your new CV is attached.")

    except Exception as e:
        bot.reply_to(message, "Error occurred: " + str(e))


# @bot.message_handler(content_types=['document'])
# def handle_doc(message):
#     try:
#         file_info = bot.get_file(message.document.file_id)
#         downloaded_file = bot.download_file(file_info.file_path)
#         try:
#             parse_document(downloaded_file)
#         except Exception as e:
#             print(f"Error parsing document: {e}")
#         # file = message.get("document")
#         # file_id = file.get("file")
#         # url = f"https://api.telegram.org/file/bot{BOT_TOKEN}/{file_id}"

#         # try:
#         #     response = requests.get(url)
#         #     open("url_output.docx", "wb").write(response.content)
#         # except Exception as e:
#         #     print(f"Failed, error: {e}")

#         # with open("input.docx", 'wb') as f:
#         #     f.write(downloaded_file)
        
#         # # Convert docx to Markdown
#         # with open("input.docx", "rb") as docx_file:
#         #     result = mammoth.convert_to_markdown(docx_file)
#         # md_text = result.value

#         # # Create new Word docx from Markdown
#         # doc = docx.Document()
#         # doc.add_paragraph(md_text)
#         # doc.save("output.docx")

#         # Send new docx file
#         print("hello")
#         prompt = "input.html"
#         parse_document_for_bot(prompt)
#         print("hello")
#         with open('output.md', "rb") as f:
#             bot.send_document(message.chat.id, f)

#         bot.reply_to(message, "Conversion done! New docx file sent.")

#     except Exception as e:
#         bot.reply_to(message, "Oops, something went wrong")
        

@bot.message_handler(chat_types=['private'])
def handle_private_chat(message):
  message_id = message.id
  chat_id = message.chat.id
  message_content = message.text

  if message.text == '/greet':
    bot.reply_to(message, "Hello!")

# Log chat in usage db for tracking
  try: 
      usage_db.create_tables()
  except Exception as e:
      print(f'Error creating tables: {e}') 

  try:
      usage_db.log_new_chat(message_id, chat_id, message_content)
  except Exception as e:
      print(f'Exception logging new chat: {e}')

  # conn = sqlite3.connect(DB_FILE)
  # c = conn.cursor()
  # try:
  #   c.execute('INSERT OR IGNORE INTO chat_log VALUES (?, ?, ?)', (message_id, chat_id, message_content))
  #   conn.commit()
  #   conn.close()
  #   print('Successfully logged data')
  # except Exception as e:
  #   print(f"Error logging to database: {e}") # Print any database errors

# @bot.message_handler(chat_types=['private'])
# def handle_private_chat(message):
#    chat_id = message.chat.id
#    print(f"Extracted chat ID: {chat_id}")
#    try:
#     usage_tracker.log_new_chat(chat_id)  
#     print("Logged new chat to database") # Print if database call succeeded 
#    except Exception as e:
#     print(f"Error logging to database: {e}") # Print any database errors

# @bot.message_handler(commands=['greet']) 
# def greet(message):
#   #print(f"Received new chat event: {message}") # Print full message ob
#   bot.reply_to(message, "Hello!")



bot.polling()

