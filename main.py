import asyncio, logging, os, json
from dotenv import load_dotenv

from aiogram import Bot, Dispatcher
from aiogram.types import BotCommand, BotCommandScopeAllPrivateChats, BotCommandScopeAllGroupChats
from aiogram.filters import CommandStart
from aiogram import F, types

load_dotenv()
TOKEN=os.getenv("TOKEN")
HOMMER_ID=int(os.getenv("HOMMER_ID"))
bot = Bot(token=TOKEN)
dp = Dispatcher()

@dp.message(CommandStart())
async def startInfo(message: types.Message):
    user = str(message.from_user.id)
    with open("db.json", encoding='utf-8') as file:
        data = json.load(file)
    
    if user not in data.keys():
        data[user] = {
            "photo":'null',
            "geo":'null'
        }
    with open("db.json", "w", encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=4)

    await message.answer("Привет! Если ты зашел в бота, то скорее всего ты хочешь принять участие в розыгрыше на 50 звезд."
    "\nПоскольку я собираю статистику с определенного региона, принять участие смогут не все"
    "\nВ этого бота тебе нужно отправить скриншот с сайта с подтверждением прохождения опроса и указать населёныый пункт в котором ты находишься")

@dp.message(F.photo)
async def helloFriend(message: types.Message):
    user = str(message.from_user.id )
    caption = message.caption or 'null'
    photo_file_id = message.photo[-1].file_id

    with open("db.json", encoding='utf-8') as file:
        data = json.load(file)
    if user not in data.keys():
        data[user] = {
            "photo":photo_file_id,
            "geo":caption
        }
    else: 
        if data[user]["photo"] != 'null' and data[user]["geo"] != 'null': 
            return await message.answer("Ты уже участвуешь в розыгрыше. Если столкнулся с трудностями свяжись с @hommer_8677")
        data[user]["photo"] = photo_file_id

    with open("db.json", "w", encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=4)

    if caption == 'null':
        return await message.answer("Теперь напишите название вашего населенного пункта")

    bot.send_photo(
        chat_id=HOMMER_ID,
        photo = data[user]["photo"],
        caption = data[user]["geo"] + f"\n@{message.from_user.username}"
    )
    await message.answer("Теперь вы учавствуете в конкурсе!"
    "\nСледите за ходом проведения мероприятия и ждите результатов розыгрыша на <a href='https://t.me/hommer_dev'>Канале</a>", 
    parse_mode='HTML')

@dp.message(F.text)
async def geoInfo(message: types.Message):
    user = str(message.from_user.id)
    with open("db.json", encoding='utf-8') as file:
        data = json.load(file)
    
    if user not in data.keys():
        data[user] = {
            "photo":'null',
            "geo":'null'
        }
    else: 
        if data[user]["photo"] != 'null' and data[user]["geo"] != 'null': 
            return await message.answer("Ты уже участвуешь в розыгрыше. Если столкнулся с трудностями свяжись с @hommer_8677")
        data[user]["geo"] = message.text or 'null'        

    with open("db.json", "w", encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=4)

    if data[user]["photo"] == 'null': return await message.answer("Теперь отправь подтверждение прохождения опроса")

    await bot.send_photo(
            chat_id=HOMMER_ID,
            photo = data[user]["photo"],
            caption = data[user]["geo"] + f"\n@{message.from_user.username}"
        )
    await message.answer("Теперь вы учавствуете в конкурсе!"
    "\nСледите за ходом проведения мероприятия и ждите результатов розыгрыша на <a href='https://t.me/hommer_dev'>Канале</a>", parse_mode='HTML')


async def main():
    # dp.start_polling(int_router)
    # dp.start_polling(str_router)
    await dp.start_polling(bot)

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Бот выключен')