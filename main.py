import logging
import cv2
import pytesseract
from aiogram import Bot, Dispatcher, types, executor

logging.basicConfig(level=logging.INFO)

BOT_TOKEN = "ТОКЕН"

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe' 

@dp.message_handler(content_types=types.ContentType.PHOTO)
async def handle_photo(message: types.Message):
    """
    Обработчик фотографий: получает изображение, распознает текст и возвращает его.
    """
    photo = message.photo[-1] 
    photo_path = f"photo_{message.from_user.id}.jpg"
    await photo.download(destination_file=photo_path)

    img = cv2.imread(photo_path)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)  
    _, thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY)  

    text = pytesseract.image_to_string(thresh, lang='rus+eng')  

    if text.strip():
        await message.reply(f"Распознанный текст:\n{text}")
    else:
        await message.reply("Не удалось распознать текст. Убедитесь, что изображение содержит чёткий текст.")

@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    await message.reply("Привет! Отправь мне изображение с текстом, и я его распознаю.")

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
