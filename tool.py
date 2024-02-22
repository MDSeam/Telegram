import requests,random

morse_code_dict = {
    'A': '..-..-',
    'B': '-...',
    'C': '-.-.',
    'D': '-..',
    'E': '--..--..',
    'F': '..-.',
    'G': '--.',
    'H': '....-',
    'I': '--.-.-',
    'J': '.---',
    'K': '-.-',
    'L': '-.-.-',
    'M': '--..-.-',
    'N': '-.',
    'O': '..--..-',
    'P': '.--.',
    'Q': '--.-',
    'R': '.-.',
    'S': '...',
    'T': '-',
    'U': '..-',
    'V': '..---.',
    'W': '.--',
    'X': '-..-',
    'Y': '--..--..-',
    'Z': '--..',
    'a': '~..-..-',
    'b': '~-...',
    'c': '~-.-.',
    'd': '~-..',
    'e': '~--..--..',
    'f': '~..-.',
    'g': '~--.',
    'h': '~....-',
    'i': '~--.-.-',
    'j': '~.---',
    'k': '~-.-',
    'l': '~-.-.-',
    'm': '~--..-.-',
    'n': '~-.',
    'o': '~..--..-',
    'p': '~.--.',
    'q': '~--.-',
    'r': '~.-.',
    's': '~...',
    't': '~-',
    'u': '~..-',
    'v': '~..---.',
    'w': '~.--',
    'x': '~-..-',
    'y': '~--..--..-',
    'z': '~--..',
    '1': '.----',
    '2': '..---',
    '3': '...--',
    '4': '....',
    '5': '.....',
    '6': '-....',
    '7': '--...',
    '8': '---..',
    '9': '.-...',
    '0': '-----',
    '.': '.-.-.-',
    ',': '--..--',
    '?': '..--..',
    "'": '.----.',
    '!': '-.-.--',
    '/': '-..-.',
    '(': '-.--.',
    ')': '-.--.-',
    '&': '----.',
    ':': '---...',
    ';': '-.-.-.',
    '=': '-...-',
    '+': '.-.-.',
    '-': '-....-',
    '_': '..--.-',
    '@': '.--.-.',
    ' ': '/'
}

salt = [
    '.-', '..', '--', '.-..', '---', '...-', '.', '-.--', '...---', '~.-',
    '~..', '~--', '~.-..', '~---', '~...-', '~.', '~-.--', '~...---'
]

reverse_morse = {v: k for k, v in morse_code_dict.items()}


def encode(text, blue):
  morse_code = []
  for char in text:
    if char in morse_code_dict:
      morse_code.append(morse_code_dict[char])
    if blue:
      morse_code.append(' ')
      morse_code.append(random.choice(salt))
      morse_code.append(' ')
  return ' '.join(morse_code)


def decode(msg):
  words = msg.split(' / ')
  decoded_text = ''
  for word in words:
    letters = word.split(' ')
    for letter in letters:
      if letter in reverse_morse:
        decoded_text += reverse_morse[letter]
    decoded_text += ' '
  return decoded_text


def html_download(url):
  response = requests.get(url)
  if response.status_code == 200:
    with open('index.html', 'w', encoding='utf-8') as file:
      file.write(response.text)
  else:
    print(
        f'Failed to download index.html . Status code: {response.status_code}')


#weather


def sweather(city):
  url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid=bd5e378503939ddaee76f12ad7a97608&units=metric'
  response = requests.get(url)

  if response.status_code == 200:
    data = response.json()
    return data
  else:
    return None


#SHORT


def tiny(url):
  endpoint = f"http://tinyurl.com/api-create.php?url={url}"
  response = requests.get(endpoint)
  if response.status_code == 200:
    return response.text
  else:
    return 'Url Error !\nUrl Must start with http:// or https://\nUrl Must end with // \nUrl EX : http://google.com/'


def isgd(url):
  endpoint = f"https://is.gd/create.php?format=json&url={url}"
  response = requests.get(endpoint)

  if response.status_code == 200:
    data = response.json()
    try:
      return data['shorturl']
    except KeyError:
      return 'Url Error !\nUrl Must start with http:// or https://\nUrl Must end with // \nUrl EX : http://google.com/'
  else:
    return 'Url Error !\nUrl Must start with http:// or https://\nUrl Must end with // \nUrl EX : http://google.com/'
