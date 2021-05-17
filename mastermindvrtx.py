from telebot import TeleBot, types
from io import BytesIO
from PIL import Image
import os, re
from config import BOT_TOKEN

TOKEN = Config.BOT_TOKEN
mastermindvrtx = TeleBot(TOKEN)

list_image = {}

@mastermindvrtx.message_handler(commands = ["start"])
def start(message):
	name = re.sub(r"[*_`]", "", message.from_user.first_name)
	msg = f"""
Hi _{name}_!
I will convert your images to .pdf

		<<<| ʍǟֆȶɛʀʍɨռɖ ʋʀȶӼ™ |>>>
--------------------------------------------------
- Visit @vrtxmusic for chatting
- My other bots can be found in here @vrtxwork
--------------------------------------------------

		*[COMMANDS]*
/PDF -- To start convertion
/FINISH -- To ge the pdf file 
 """

	markup = types.InlineKeyboardMarkup()
	markup.add(types.InlineKeyboardButton("HOME", url = "https://t.me/vrtxwork"))
	mastermindvrtx.send_message(message.from_user.id, msg, reply_markup = markup, parse_mode = "Markdown")

@mastermindvrtx.message_handler(content_types = ["photo"])
def add_photo(message):
	if not isinstance(list_image.get(message.from_user.id), list):
		mastermindvrtx.reply_to(message, "Send /pdf for initialization")
		return

	if len(list_image[message.from_user.id]) >=50:
		mastermindvrtx.reply_to(message, "Sorry! Only 50 images can be converted for now")
		return

	file = mastermindvrtx.get_file(message.photo[1].file_id)
	downloaded_file = mastermindvrtx.download_file(file.file_path)
	image = Image.open(BytesIO(downloaded_file))

	list_image[message.from_user.id].append(image)
	mastermindvrtx.reply_to(message, f"[{len(list_image[message.from_user.id])}] Success add image, send command /done if finish")

@mastermindvrtx.message_handler(commands = ["PDF"])
def PDF(message):
	mastermindvrtx.send_message(message.from_user.id, "Get Set Send me images...")

	if not isinstance(list_image.get(message.from_user.id), list):
		list_image[message.from_user.id] = []

@mastermindvrtx.message_handler(commands = ["FINISH"])
def FINISH(message):
	images = list_image.get(message.from_user.id)

	if isinstance(images, list):
		del list_image[message.from_user.id]

	if not images:			
		mastermindvrtx.send_message(message.from_user.id, "First send me images..")
		return

	path = str(message.from_user.id) + ".pdf"
	images[0].save(path, save_all = True, append_images = images[1:])
	mastermindvrtx.send_document(message.from_user.id, open(path, "rb"), caption = "From @vrtxpdf_bot")
	os.remove(path)

print("""		<<<| ʍǟֆȶɛʀʍɨռɖ ʋʀȶӼ™ |>>>
--------------------------------------------------
|		Visit @vrtxmusic for chatting            |
|	My other bots can be found in here @vrtxwork |
--------------------------------------------------""")
mastermindvrtx.polling()
