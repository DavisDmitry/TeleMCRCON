import logging

from aiogram import Bot, Dispatcher, executor, types
from mcrcon import MCRcon

from config import Configuration


config = Configuration.from_env()


bot = Bot(config.token, parse_mode='html')
dp = Dispatcher(bot)


logging.basicConfig(level=config.log_level)
logger = logging.getLogger('bot')
logger.setLevel(config.log_level)


@dp.message_handler(commands='start')
async def start(message: types.Message):
    if message.from_user.id in config.admins_list:
        text = ('Привет, {}!\n'
                'Я передам любые твои команды на сервер Minecraft с помощью '
                'RCON.\n'
                'Не стесняйся обращаться ко мне в чатах. Я удалю свой '
                '@username из команды')
        text = text.format(message.from_user.first_name)
        return await message.answer(text)
    await message.answer('У тебя нет доступа для использования этого бота.')


@dp.message_handler()
async def text(message: types.Message):
    if message.from_user.id in config.admins_list:
        bot = await message.bot.get_me()
        command = message.text.replace('@ ' + bot.username, '')
        command = message.text.replace('@' + bot.username, '')
        if command[0] == '/':
            command = command[1:]
        logger.info(message.from_user.username + ' send: `%s`.' % command)
        with MCRcon(
                config.rcon_host,
                config.rcon_pass,
                config.rcon_port
                ) as mcr:
            resp = mcr.command(command)
            logger.info(resp)
            await message.reply('<code>%s</code>' % resp)


if __name__ == '__main__':
    executor.start_polling(dp)
