import os
import asyncio
from aiogram import Bot, Dispatcher, types
from config import API_TOKEN
from fpdf import FPDF


bot = Bot(API_TOKEN)
dp = Dispatcher(bot)
pages_count = 1
pdf = FPDF()


@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    """Greet user after /start or /help command"""

    name = message.from_user.first_name + message.from_user.last_name if message.from_user.last_name \
        else message.from_user.first_name
    welcome_message = f"Hello, {name}!\nSend me a .jpg or .png files and I'll convert it to PDF."
    await bot.send_message(message.chat.id, welcome_message)

    # Remove all .mp4 files
    files = os.listdir()

    for item in files:
        if item.endswith(".jpg") or item.endswith(".png") or item.endswith(".pdf"):
            os.remove(item)


@dp.message_handler(content_types=['photo'])
async def get_file(message: types.Message):
    global pages_count
    global pdf

    await message.photo[-1].download('test.jpg')

    pdf.set_display_mode('real')

    pdf.add_page()
    pdf.image('test.jpg', h=pdf.eph, w=pdf.epw)

    keyboard = types.InlineKeyboardMarkup()
    convert_button = types.InlineKeyboardButton('Convert', callback_data='Convert')
    keyboard.add(convert_button)
    pic_message = f'Added {pages_count} pictures.'
    pages_count += 1
    await bot.send_message(message.chat.id, pic_message, reply_markup=keyboard)


@dp.callback_query_handler(text=['Convert'])
async def send_pdf(callback: types.CallbackQuery):
    global pages_count
    global pdf
    pages_count = 1
    pdf.output('yourfile.pdf', 'F')
    await callback.message.answer_document(open("yourfile.pdf", "rb"))
    pdf = FPDF()


async def main():
    await dp.start_polling(dp)

if __name__ == '__main__':
    asyncio.run(main())
