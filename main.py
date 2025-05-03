import json
import asyncio

from llama_cpp import Llama

from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command
from aiogram.types import Message

#initialization

config = json.load(open('config.json'))
#bot
bot_token = config['bot_token']
bot = Bot(token=bot_token, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher()
#llm
llm = Llama(model_path=config['model_path'])



@dp.message(Command("start"))
async def cmd_start(message: Message):
    await message.answer("Здарова, заебал!")


@dp.message(F.chat.type == "private")
async def message_handler(message: Message) -> None:
    await message.reply('Думаю... (мой создатель еблан и тыкнул ллм на гнилую малину, это сука надолго)')
    ai_answer = llm.create_chat_completion(messages=[{'role' : 'user', 'content' : message.text}])
    await message.answer(ai_answer['choices'][-1]['message']['content'], parse_mode="Markdown")


# starting
async def main() -> None:
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
