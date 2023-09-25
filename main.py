from aiogram import Bot, Dispatcher
from asyncio import sleep, create_task, run
from input import TOKEN, ID, PATH
from DB.executes import Executions
from aiogram.types import Message
from functions import *
import time



dp   = Dispatcher()
BASE = Executions(PATH)
BASE.check_bd_existing()

SAVE_FLAG          = False
DELETE_FLAG        = False
COULD_USE_DEL_FLAG = False
PERMANENT_SAVE     = False
keyboard = make_buttons(['/save_note', '/save_note_permanently' , '/nearest_note', '/all_notes', '/start', '/help'])
little_board = make_buttons(['/start', '/delete_note'])
bot = Bot(token=TOKEN)


async def START() -> None:
    try:
        await dp.start_polling(bot)
    except Exception as ex:
        print(ex)
    finally: 
        await bot.session.close()


@dp.startup()
async def command_start(bot: Bot):
    global keyboard
    await bot.send_message(ID, 'Бот запущен!\n' + \
                                'Список возможных комманд:\n' + \
                                '/help /save_note /nearest_note\n' + \
                                '/all_notes /delete_note /start', reply_markup = keyboard)


@dp.message()
async def get_message(message: Message):
    global SAVE_FLAG
    global DELETE_FLAG
    global COULD_USE_DEL_FLAG
    global PERMANENT_SAVE
    

    if message.text == '/start':
        await message.answer('Список возможных комманд:\n' + \
                            '/help /save_note /nearest_note\n' + \
                            '/all_notes /delete_note /start', reply_markup = keyboard)
        COULD_USE_DEL_FLAG = False
        SAVE_FLAG          = False
        DELETE_FLAG        = False
        

    elif message.text == '/all_notes':
        TEXT = all_notes()
        await message.answer(TEXT, reply_markup = little_board, parse_mode = "HTML")
        COULD_USE_DEL_FLAG = True
        SAVE_FLAG          = False
        DELETE_FLAG        = False
        PERMANENT_SAVE     = False


    elif message.text == '/help':
        await message.answer('Пояснения к коммандам:\n' + \
            '/start - выводит свисок всех возможных комманд\n' + \
            '/save_note - позволяет сохранить заметку\n' + \
            '/all_notes - показывает списко всех заметок\n' + \
            '/nearest_note - выводит близжайшее напоминание\n' + \
            '/delete_note - удаляет выбранную вами заметку\n' + \
            '(доступно только после вызова /all_notes)', reply_markup = keyboard)


    elif message.text == '/nearest_note':
        answer = nearest_note()
        await message.answer(answer, reply_markup = keyboard, parse_mode = "HTML")


    elif message.text == '/save_note':
        await message.answer('Напишите заметку в формате <число> <месяц> <время через двоеточие> <текст_заметки>\n' + \
                             'За более подробной информацией воспользуйтесь /help.')
        SAVE_FLAG          = True
        DELETE_FLAG        = False
        COULD_USE_DEL_FLAG = False
        PERMANENT_SAVE     = False
    

    elif message.text == '/save_note_permanently':
        await message.answer('Напишите заметку в формате <число> <месяц> <время через двоеточие> <текст_заметки>\n' + \
                             'За более подробной информацией воспользуйтесь /help.')
        SAVE_FLAG          = True
        DELETE_FLAG        = False
        COULD_USE_DEL_FLAG = False
        PERMANENT_SAVE     = True
        

    elif message.text == '/delete_note' and COULD_USE_DEL_FLAG == True:
        await message.answer('Укажите уникальный номер записи, которую желаете удалить.')
        SAVE_FLAG          = False
        DELETE_FLAG        = True
        COULD_USE_DEL_FLAG = False
        PERMANENT_SAVE     = False
    
    
    elif message.text == '/delete_note' and COULD_USE_DEL_FLAG == False:
        await message.answer('В данный момент это сделать невозможно.',)
        SAVE_FLAG          = False
        DELETE_FLAG        = False
        COULD_USE_DEL_FLAG = False
        PERMANENT_SAVE     = False
        

    else:
        if SAVE_FLAG == True:
            mes = message.text.split()
            if PERMANENT_SAVE == False:
                answer = save_note(mes)
            else:
                answer = save_note(mes, PERMANENT_SAVE)
            if answer == 0:
                await message.reply("Дата введена в неверном формате, повторите попытку снова:")
            else:
                await message.answer("Заметка сохранена!", reply_markup = keyboard)
                SAVE_FLAG      = False
                PERMANENT_SAVE = False
        
        
        elif DELETE_FLAG == True:
            answer = del_note(message.text)
            if answer == 1:
                await message.answer('Запись удалена!', reply_markup = keyboard)
                DELETE_FLAG = False
            else:
                await message.reply(answer)


        else:
            await message.reply('Данной команды не существует!', reply_markup = keyboard)


async def check_base():
    while True:
        res = need_to_remind()
        if res != 0:
            await bot.send_message(ID, f'Напоминание: <b>{res}</b>', parse_mode = "HTML")
        await sleep(40)


async def murge():
    checker = create_task(check_base())
    main = create_task(START())
    while True:
        try:
            await checker
            await main
        except:
            time.sleep(10)



if __name__ == '__main__':
    run(murge())