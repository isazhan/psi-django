from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.conf import settings
from bot.bot import Bot
from bot.handler import CommandHandler, BotButtonCommandHandler
import secrets
import string
import json
from db import get_db_handle


TOKEN = open(settings.BASE_DIR / 'apps/users/management/commands/token.txt').read()
bot = Bot(token=TOKEN)


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        
        def start(bot, event):
            bot.send_text(chat_id=event.from_chat, 
                        text='Выберите функцию',
                        inline_keyboard_markup='{}'.format(json.dumps([[
                        {'text':'Получить первичный пароль', 'callbackData': 'call_back_id_1', 'style': 'primary'},
                        ]])))
        
        def buttons_answer_cb(bot, event):
            if event.data['callbackData'] == 'call_back_id_1':
                create_user(bot, event)
        
        def create_user(bot, event):
            if event.from_chat[-13:] == '@psi-group.kz':
                User = get_user_model()
                #print(User)
                try:
                #if get_db_handle()['users'].count_documents({'email': event.from_chat}) > 0:
                    user = User.objects.get(username=event.from_chat[:-13])
                    bot.send_text(chat_id=event.from_chat, text='Вы уже получали первичный пароль!')
                except:
                #else:
                    letters = string.ascii_letters
                    digits = string.digits
                    alphabet = letters + digits
                    pwd_length = 6
                    pwd = ''
                    for i in range(pwd_length):
                        pwd += ''.join(secrets.choice(alphabet))
                    ########
                    print(1)
                    #from ...models import CustomUser
                    #from ...models import CustomUserManager

                    #user = CustomUserManager.create_user(email=event.from_chat, password=pwd, first_name='fn', last_name='ln')
                    
                    #CustomUserManager.create_user(email=event.from_chat, password='123456789')
                    print(2)
                    """
                    col = get_db_handle()['users']
                    val = {
                        'email': event.from_chat,
                        'password': '123456789',
                        'first_name': 'firstname',
                        'last_name': 'lastname',
                        }
                    col.insert_one(val)
                    """
                    user = User.objects.create_user(username=event.from_chat, password=pwd, first_name='fn', last_name='ln')
                    print(user)
                    user.save()

                    

                    bot.send_text(chat_id=event.from_chat, text='Поздравляем! Ваша учетная запись успешно создана. Ваш пароль для входа на сайт: \n\n{}'.format(pwd))
                    bot.send_text(chat_id=event.from_chat, text='Сайт доступен по ссылке: \nhttp://192.168.1.33:8000')
            else:
                bot.send_text(chat_id=event.from_chat, text='Вы не сотрудник нашей компании!')


        bot.dispatcher.add_handler(CommandHandler(command='start', callback=start))
        bot.dispatcher.add_handler(BotButtonCommandHandler(callback=buttons_answer_cb))
        bot.start_polling()
        bot.idle()