from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command

import config
import bot.utils as utils
from db.database import add_user, add_group, add_message, count_message_in_group, \
    clean_form_database_group

SEND_GPT_MESSAGE = 50


router = Router()


@router.message(Command("prison_online"))
async def message_answer(msg: Message):
    list_send_message = await clean_form_database_group(msg.chat.id)
    await generate_text(list_send_message, msg)


@router.message()
async def message_handler(msg: Message):
    if msg.chat.type == 'group' or msg.chat.type == 'supergroup':
        user_id = await add_user(msg.from_user.id, msg.from_user.first_name, msg.from_user.username)
        if user_id == -1:
            return
        group_id = await add_group(msg.chat.id, msg.chat.type, msg.chat.title)
        if group_id == -1:
            return
        if await count_message_in_group(msg.chat.id) >= SEND_GPT_MESSAGE:
            await message_answer(msg)
        await add_message(msg.message_id, user_id, group_id, msg.text)


async def generate_text(list_mes: list, msg):
    prompt = ''
    if not list_mes:
        return
    for i in list_mes:
        prompt += f'@{i[0]}: {i[1]}\n'
    chatgpt_instance = utils.ChatGPT()
    res = await chatgpt_instance.send_message(
                    prompt,
                    dialog_messages=[],
                )
    if not res:
        return await msg.answer('gg')
    if "нарушений нет" in res[0].lower():
        await msg.answer(res[0])
    else:
        await msg.answer(f"{config.chat_modes['assistant']['message_start']}\n\n{res[0]}\n\n"
                        f"{config.chat_modes['assistant']['message_finish']}")