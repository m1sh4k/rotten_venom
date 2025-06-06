import json
import asyncio

from llama_cpp import Llama

from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.types.reaction_type import ReactionType

from transformers import AutoProcessor, AutoModelForImageTextToText
from PIL import Image
#initialization

config = json.load(open('config.json'))
#bot
bot_token = config['bot_token']
bot = Bot(token=bot_token, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher()
#llm
llm = Llama(model_path=config['model_path'], n_ctx=256)

# image-to-text
image_prompt = 'An image of'
processor = AutoProcessor.from_pretrained("Salesforce/blip-image-captioning-base")
model = AutoModelForImageTextToText.from_pretrained("Salesforce/blip-image-captioning-base")


slut_prompt = ['сделай реакцию на картинку по описанию "', '" так: сделай вид, что тебе очень интересна эта тем (но на самом деле нет) фальшиво прояви реакцию, но ответь в соответствии с описание картинки, чтобы было понятно, к чему реакция, отправь пару смайлов, пиши максимально коротко, не более двух или трех строк. Do not write any notes and so on! write answer in russian. Напоминаю НИКАКИХ ПРИМЕЧАНИЙ!!!']
@dp.message(Command("start"))
async def cmd_start(message: Message):
    await message.answer("Здарова, заебал!")


@dp.message(F.chat.type == "private")
async def message_handler(message: Message) -> None:
    try:
        #message.react([ReactionType(emoji=chr(0x1F44D))])
        await message.reply('Думаю... (мой создатель еблан и тыкнул ллм на гнилую малину, это сука надолго)')
        ai_answer = llm.create_chat_completion(messages=[{'role' : 'user', 'content' : message.text}], max_tokens=128)
        #ai_answer = await asyncio.to_thread(llm.create_chat_completion, messages=[{'role' : 'user', 'content' : message.text}], max_tokens=1024)

        await message.answer(ai_answer['choices'][-1]['message']['content'], parse_mode="Markdown")
    except Exception as e:
        await message.reply(f'!got an error!\n{e}')

@dp.message(lambda message: message.chat.id == -1002355380118 and message.chat.type in ['group', 'supergroup'])
async def slut(message: Message):
#    ai_answer = llm.create_chat_completion(messages=[{'role' : 'user', 'content' : message.text}], max_tokens=1024)
    if message.photo:
        await bot.download(message.photo[0], destination='tmp.png')
        print('pic downloaded!')
        image = Image.open('tmp.png')
        inputs = processor(images=image, text=image_prompt, return_tensors="pt")
        out = model.generate(**inputs)
        image_description = processor.decode(out[0], skip_special_tokens=True)
        print(f'image description: {image_description}')
        ai_answer = llm.create_chat_completion(messages=[{'role' : 'user', 'content' : slut_prompt[0] + image_description + slut_prompt[1]}], max_tokens=128)
        print(f'ai_answer: {ai_answer}')
        await message.reply(ai_answer['choices'][-1]['message']['content'], parse_mode=None)
        #await message.reply('вот ты kakashka!')
    else:
       ... 
        #await message.reply('вот ты сосунишка!')



# starting
async def main() -> None:
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
