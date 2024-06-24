import telebot,os,re
import random , requests
import string , json,pytz
from datetime import datetime , timedelta
from tool import *
from gtts import gTTS
from urllib.parse import urlparse
from keep import keep_alive
from difflib import get_close_matches
from PIL import Image
from io import BytesIO
from pywebcopy import save_webpage
import shutil 
keep_alive()


tz= pytz.timezone('Asia/Dhaka')
bdt = datetime.now(tz)
bdt = int(datetime.timestamp(bdt))


BOT_TOKEN = os.environ['BOT_TOKEN']

# Creating Telebot Object
bot = telebot.TeleBot(BOT_TOKEN)
def logg(user,text : str):
  if user.chat.first_name:
    idname = f'{user.chat.first_name} {user.chat.last_name}'
  else:
    idname = f'{user.chat.title}'
  
  nowtime = datetime.fromtimestamp(bdt)
  nowtime = nowtime + timedelta(hours=6)
  nowtime = nowtime.strftime('%d-%b-%y %I:%M:%S %p')

  file_path = 'log.txt'
  new_data = f'{nowtime} # {idname} # {user.chat.id} # {text}\n'
  with open(file_path, 'r') as file:
    existing_content = file.read()
  combined_content = new_data + existing_content
  with open(file_path, 'w') as file:
    file.write(combined_content)

  
def check(user,text=None):
    if text:
      logg(user,text)
    with open('user.json', 'r') as file:
        data = json.load(file)
    if str(user.chat.id) in data:
        if data[str(user.chat.id)][0] > bdt :
            return False
        else:
            bot.send_message(user.chat.id, f'Your subscription Expired !')
            return True
    else:
        if user.chat.first_name:
          idname = f'{user.chat.first_name} {user.chat.last_name}'
        else:
          idname = f'{user.chat.title}'
        logg(user,'New Member added')
        data[str(user.chat.id)] = [bdt + (3 * 24 * 3600) , 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',idname]

        with open('user.json', 'w') as file:
            json.dump(data, file)
        bot.send_message(user.chat.id, 'Just Now you Start 3 days Trial Version of Seam Bot .\nWhen expire trial version purchase subscription .')
        return True

def useragent(act,msg):
    with open('user.json', 'r') as file:
        data = json.load(file)
    if act == 'act':
        return data[str(msg.chat.id)][1]
    else:
        if msg.text.replace('/useragent','').replace(' ','') == "":
            bot.send_message(msg.chat.id, 'use /useragent <my user agent>')
            return
        data[str(msg.chat.id)][1] = msg.text.replace('  ','').replace('/useragent ','').replace('/useragent','')
        with open('user.json', 'w') as file:
            json.dump(data, file)
        bot.send_message(msg.chat.id, 'Useragent save successfully !')

# Whenever Starting Bot
@bot.message_handler(commands=['start'])
def start(msg):
  if check(msg):
    return
  bot.send_message(msg.chat.id, 'Hello, Welcome to Seam TG Bot !\nSuggestion : /help /hello')

@bot.message_handler(commands=['useragent'])
def start(msg):
  if check(msg):
    return
  useragent('',msg)

@bot.message_handler(commands=['hello'])
def start(msg):
    if check(msg):
      return
    bot.send_message(msg.chat.id, f'Hello {msg.chat.first_name} {msg.chat.last_name}  , Welcome to Seam TG Bot !')
    with open('user.json', 'r') as file:
        data = json.load(file)
    if data[str(msg.chat.id)][0] > bdt :
        date = datetime.fromtimestamp(data[str(msg.chat.id)][0])
        date = date.astimezone(tz)
        date= date.strftime('%Y-%m-%d %I:%M:%S %p')
        bot.send_message(msg.chat.id, f'Your Subscript Expire in : {date}')
    else:
        bot.send_message(msg.chat.id, f'Your subscription Expired shhdhehe !')

@bot.message_handler(commands=['help'])
def start(msg):
  if check(msg):
      return
  bot.send_message(msg.chat.id, f' 1. /tool ---  For Tool')

#Admin

@bot.message_handler(commands=['adm'])
def admin(msg):
  if check(msg):
      return
  
  bot.send_message(msg.chat.id, msg.text)
  
# Tool

@bot.message_handler(commands=['tool'])
def start(msg):
  if check(msg):
      return
  with open('tool.txt','r') as file:
    txt = file.read()
  bot.send_message(msg.chat.id, txt)

#Morse

@bot.message_handler(commands = ['morse'])
def morse(msg):
  if check(msg,'Use Morse'):
      return
  split_parts = msg.text.replace('\xa0', ' ').replace('~', ' ~').split(' ')
  try:
      morse_code = ' '.join(split_parts[2:])
      option = split_parts[1]
      if option == 'e':
          bot.send_message(msg.chat.id, encode(morse_code,False))
      elif option == 'es':
          bot.send_message(msg.chat.id, encode(morse_code,True))
      elif option == 'd':
          bot.send_message(msg.chat.id, decode(morse_code))
      else:
          bot.send_message(msg.chat.id, f'Invaild Morse Command Format\n1. Enode without salt = morse e text\n4. Encode with Salt = morse es text\n3. Decode = morse d text')
  except IndexError:
      bot.send_message(msg.chat.id, f'Invaild Morse Command Format\n1. Enode without salt = morse e text\n4. Encode with Salt = morse es text\n3. Decode = morse d text')

# html 
@bot.message_handler(commands = ['html'])
def html_download(msg):
    if check(msg,'Use Html'):
      return
    try:
        link = msg.text.split(' ')[1]
        save_webpage(
              url=link,
              project_folder="./",
              project_name="html",
              bypass_robots=True,
              debug=False,
              open_in_browser=False,
              delay=None,
              threaded=False
        )
        shutil.make_archive('./index', 'zip', 'html')
      
        bot.send_document(msg.chat.id, open('./index.zip', 'rb'))
      
        if os.path.isdir('html'):
          shutil.rmtree('html')
        if os.path.isfile('index.zip'):
          os.remove('index.zip')
        
    except IndexError:
      bot.send_message(msg.chat.id, f'Type Error . Ex: /html <website link>')

# pass gen
@bot.message_handler(commands = ['genpass'])
def generate_password(msg):
    if check(msg,'Use GenPassword'):
      return
    characters = string.ascii_letters + string.digits + string.punctuation
    try:
        password = ''.join(random.choice(characters) for _ in range(int(msg.text.split(' ')[1])))
        bot.send_message(msg.chat.id, password)
    except IndexError:
      bot.send_message(msg.chat.id, f'Type Error . Ex: /genpass 12')

#weather

@bot.message_handler(commands = ['weather'])
def weather(msg):
    if check(msg,'Use Weather'):
      return
    try:
        city = msg.text.split(' ')[1]
        weather_data = sweather(city)
        bot.send_message(msg.chat.id, f"Weather in {weather_data['name']} \n    Temperature: {weather_data['main']['temp']}°C\n    Temperature Feel : {weather_data['main']['feels_like']}°C\n    Min Temperature: {weather_data['main']['temp_min']}°C\n    Max Temperature: {weather_data['main']['temp_max']}°C\n    Description :  {weather_data['weather'][0]['description']}\n    Humidity :  {weather_data['main']['humidity']}%\n    Wind Speed :  {weather_data['wind']['speed']} m/s\n    Cloudiness : {weather_data['clouds']['all']}%\n    Longtitude : {weather_data['coord']['lon']}\n    Latitude : {weather_data['coord']['lat']}\n   Sunrise :  {datetime.utcfromtimestamp(weather_data['sys']['sunrise']).strftime('%Y-%m-%d %I:%M:%S %p')}\n   Sunset :  {datetime.utcfromtimestamp(weather_data['sys']['sunset']).strftime('%Y-%m-%d %I:%M:%S %p')}\n   Pressure :  {weather_data['main']['pressure']}")
    except IndexError:
      bot.send_message(msg.chat.id, f'Type Error . Ex: /weathet Dhaka')

#Print

@bot.message_handler(commands = ['print'])
def hmhello(msg):
    if check(msg , 'Use Print'):
      return
    try:
        split_parts = msg.text.split(' ')
        string = ' '.join(split_parts[2:])
        amount = split_parts[1]
        message = ""
        for  i in range(1, int(amount)+1):
            message += f"{i}. {string}\n"

        bot.send_message(msg.chat.id, message)
    except IndexError:
        bot.send_message(msg.chat.id, f'Type Error . Ex: /print 20 i love you')
    except:
      bot.send_message(msg.chat.id, f'Messgae is too long.\nTelegram does not support long msg')

@bot.message_handler(commands = ['short'])
def fshort(msg):
    if check(msg,'Use Short'):
      return
    try:              
        split_parts = msg.text.split(' ')
        string = ' '.join(split_parts[2:])
        cmd = split_parts[1]
        if cmd == 't':
            bot.send_message(msg.chat.id, tiny(string))
        elif cmd == 'i':
            bot.send_message(msg.chat.id, isgd(string))
        else:
            bot.send_message(msg.chat.id, f'Type Error. Ex: /short <cmd> <link>\nReplace cmd with t for tiny or i for isgd')

    except IndexError:
        bot.send_message(msg.chat.id, f'Type Error . Ex :  /short <cmd> <link>\nReplace cmd with t for tiny or i for isgd')

@bot.message_handler(commands = ['terabox'])
def fshort(msg):
    if check(msg,'Use Terabox'):
      return


    try:              
        split_parts = msg.text.split(' ')
        cmd = split_parts[-1]

        if cmd:
        #if re.match(r'^https://teraboxapp\.com/s/.*$', cmd):
            #parsed_url = urlparse(cmd)
            #parsed_url = parsed_url.path.split('/')
            parsed_url = cmd# parsed_url[-1]
            #parsed_url = "1LRj8Kg-wTAmpQKwr6LkLCg"
            url = "https://terabox-dl.qtcloud.workers.dev/api/get-download"
            url1 = f"https://terabox-dl.qtcloud.workers.dev/api/get-info?shorturl={str(parsed_url)}&pwd="
            
            headers1 = {
                "accept": "*/*",
                "accept-language": "en-US,en;q=0.9",
                "sec-ch-ua": "\"Not)A;Brand\";v=\"24\", \"Chromium\";v=\"116\"",
                "sec-ch-ua-mobile": "?1",
                "sec-ch-ua-platform": "\"Android\"",
                "sec-fetch-dest": "empty",
                "sec-fetch-mode": "cors",
                "sec-fetch-site": "same-origin",
                "Referer": "https://terabox-dl.qtcloud.workers.dev/",
                "Referrer-Policy": "strict-origin-when-cross-origin"
              } 
            response = requests.get(url1,headers= headers1)

            headers = {
            "User-Agent": str(useragent('act',msg)),
            "Accept": "*/*",
            "Accept-Language": "en-US,en;q=0.5",
            
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "same-origin",
            }

            if response.status_code == 200:
                response = response.json()
                i = 0
                while i<len(response['list']):
                   payload = {
                  "shareid": response["shareid"],
                  "uk": response["uk"],
                  "sign": response["sign"],
                  "timestamp": response["timestamp"],
                  "fs_id": response["list"][i]["fs_id"]
                  }
                   post = requests.post(url, headers=headers, data=json.dumps(payload), verify=True).json()
                   if post['ok'] == True :
                        bot.send_message(msg.chat.id, f'1. Filename : {response["list"][i]["filename"]}\n2. Size : {round(int(response["list"][i]["size"])/(1024 * 1024),3)} MB\n3. DownloadLink : {post["downloadLink"]}')
                   else:
                       bot.send_message(msg.chat.id, f"Request Failed with Status Code: {str(post)} \nContact With us if you known me")
                   i += 1

            else:
                bot.send_message(msg.chat.id, f"Request Failed with Status Code : {str(response.text)}/n {parsed_url}\nContact With us if you known me")
        else:
            bot.send_message(msg.chat.id, f'Type Error. Ex: /terabox <link>\nLink Type : https://teraboxapp.com/s/1pC4YAlnfnpTxBbqjA')

    except IndexError:
        bot.send_message(msg.chat.id, f'If you got "error_code":31362,"error_msg":"sign error","error_info":"","request_id":8680947624767799086  this type of error .\n\nThen use your browser useragent to avoid this error .\n\nVisit your browser search <my useragent> . Copyit and user this command .\nUse /useragent <your user agent> for update your useragent')
        bot.send_message(msg.chat.id, f'Type Error . Ex :  /terabox <link>\nLink Type : https://teraboxapp.com/s/1pC4YAlnfnpTxBbqjA')


# Test to speech
@bot.message_handler(commands = ['text2s'])
def html_download(msg):
    if check(msg,'Use Text 2 Speech'):
      return
    try:
        split_parts = msg.text.split(' ')
        string = ' '.join(split_parts[1:])
        tts = gTTS(text=string, lang='en', slow=False)
        audio_buffer = BytesIO()
        tts.write_to_fp(audio_buffer)
        audio_buffer.seek(0)
        bot.send_voice(msg.chat.id, audio_buffer)
    except:
        bot.send_message(msg.chat.id,'Ex : /text2s dhf sdkfjh jkfhsjkh')



# Chat bot

def load_knowledge(file_path: str) -> dict :
  with open(file_path, 'r') as file:
    data: dict = json.load(file)
  return data

def best_find(user_question: str, questions: list[str]) -> str | None:
  matches: list = get_close_matches(user_question, questions, n=1,cutoff=0.6)
  return matches[0] if matches else None

def get_ans(question: str, knowledge_base: dict) -> str | None:
  for q in knowledge_base["questions"]:
    if q["question"] == question:
      return q["answer"]


#Chat bot

@bot.message_handler(func=lambda message: True)
def echo_all(message):
  knowledge_base: dict = load_knowledge('chatbot.json')
  best_match: str | None = best_find(message.text, [q["question"] for q in knowledge_base["questions"]])
  answer : str = get_ans(best_match, knowledge_base)
  bot.send_message(message.chat.id, answer)

# img resize

# Function to resize the image
def resize_image(image_url, new_width, new_height):
    response = requests.get(image_url)
    image = Image.open(BytesIO(response.content))
    resized_image = image.resize((new_width, new_height))
    output = BytesIO()
    resized_image.save(output, format='JPEG')
    output.seek(0)
    return output, len(output.getvalue())

# Function to compress the image
def compress_image(image_url, compression_quality):
    response = requests.get(image_url)
    image = Image.open(BytesIO(response.content))
    output = BytesIO()
    image.save(output, format='JPEG', quality=compression_quality)
    output.seek(0)
    return output, len(output.getvalue())

# Function to format file size in KB or MB
def format_size(size_bytes):
    if size_bytes >= 1048576:  # 1 MB = 1024 KB = 1048576 bytes
        return f"{size_bytes / 1048576:.2f} MB"
    elif size_bytes >= 1024:
        return f"{size_bytes / 1024:.2f} KB"
    else:
        return f"{size_bytes} bytes"

# Handler for image messages
@bot.message_handler(content_types=['photo'])
def handle_images(message):
    if check(message,'Use Photo'):
      return
    file_id = message.photo[-1].file_id

    file_info = bot.get_file(file_id)
    file_path = file_info.file_path

    file_url = f"https://api.telegram.org/file/bot{bot.token}/{file_path}"

    response = requests.head(file_url)
    original_file_size = int(response.headers['Content-Length'])

    caption_text = message.caption


    if caption_text:
        caption_text = caption_text.split(' ')

        try:
          caption_text[0] = int(caption_text[0])
        except:
            bot.send_message(message.chat.id, 'pls provide data as integer .')
            return
        if len(caption_text) == 1:
            compressed_image, compressed_file_size = compress_image(file_url, caption_text[0])
            formatted_compressed_size = format_size(compressed_file_size)
            formatted_original_size = format_size(original_file_size)
            bot.send_photo(message.chat.id, compressed_image, caption=f"Compressed\nImage Size: {formatted_compressed_size}\nOriginal Image Size: {formatted_original_size}")
        elif len(caption_text) == 2:
            try:
              caption_text[1] = int(caption_text[1])
            except:
              bot.send_message(message.chat.id, 'pls provide data as integer .')
              return
            resized_image, resized_file_size = resize_image(file_url, caption_text[0] , caption_text[1])
            formatted_resized_size = format_size(resized_file_size)
            formatted_original_size = format_size(original_file_size)
            bot.send_photo(message.chat.id, resized_image, caption=f"Resized\nImage Size: {formatted_resized_size}\nOriginal Image Size: {formatted_original_size}")
        else:
            bot.send_message(message.chat.id, 'pls Resize provide width and height . Ex: 300 200\nCompress : provide a quantity . Ex: 70')
    else:
      bot.send_message(message.chat.id, 'pls provide caption')




# Waiting For New Messages
print('Bot Starting')
bot.infinity_polling()
