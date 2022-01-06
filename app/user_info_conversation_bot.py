import uuid
from telegram import ReplyKeyboardRemove, Update
from telegram.ext import (
    CommandHandler,
    MessageHandler,
    Filters,
    ConversationHandler,
    CallbackContext,
)
from tools.state_index import StateIndex
from logger.logger import Logger
from models import User
from conversation import Conversation, ConversationBot, ConversationState
from app.multi_language_text import MultiLanguageText as MLT
from tools.keyboard import Key, MultiLanguageKey as MLK
from tools.language import Language
from abc import ABC

logger = Logger(__name__, print_start_message=True)


class SimpleConversation(Conversation):
    def __init__(self):
        super().__init__()
        self._user = User()
        self._state_index = StateIndex(['GENDER', 'PHOTO', 'LOCATION', 'BIO', 'CHANGE_LANGUAGE'])
        self._lang = Language(['ENG', 'RUS'])

    def _save_user(self) -> None:
        self._user.save()

    def _reset_user(self) -> None:
        self._user = User()

    def send_reply(self, update, text, reply_markup, **kwargs):
        update.message.reply_text(text=text, reply_markup=reply_markup, **kwargs)


class UserInfoConversationState(ConversationState, ABC):
    def __init__(self, state_index: StateIndex, lang: Language, user: User):
        super().__init__(state_index, lang)
        self._user = user


class Start(UserInfoConversationState):
    def __init__(self, state_index: StateIndex, lang: Language, user: User):
        super().__init__(state_index, lang, user)
        self.phrase = MLT(
            {
                Language(['ENG']): 'Hi! My name is Professor Bot. I will hold a ext_conversation with you. '
                                           'Send /cancel to stop talking to me.\n\n'
                                           'Are you a man or a woman?',
                Language(['RUS']): 'Привет! Меня зовут профессор Бот. Я хочу с тобой поговорить. '
                                           'Отправь /cancel, чтобы завершить разговор. \n\n'
                                           'Вы мужчина или женщина?',
            },
            current_lang=self.lang
        )

        self.keyboard.keys = [
            [
                MLK({Language(['ENG']): 'Man', Language(['RUS']): 'Мужчина'}, current_lang=self.lang),
                MLK({Language(['ENG']): 'Woman', Language(['RUS']): 'Женщина'}, current_lang=self.lang),
                MLK({Language(['ENG']): 'Other', Language(['RUS']): 'Другое'}, current_lang=self.lang)
            ]
        ]

        self.keyboard.fallback_keys = [Key('/cancel'), Key('/lang')]
        self.keyboard.input_field_placeholder = 'Man or Woman?'

    def handle_response(self, update, context):
        self.state_index.reset_state()
        return self.state_index.current


class Gender(UserInfoConversationState):
    def __init__(self, state_index: StateIndex, lang: Language, user: User):
        super().__init__(state_index, lang, user)

        self.phrase = MLT(
            {
                Language(['ENG']): 'I see! Please send me a photo of yourself, '
                                           'so I know what you look like, or send /skip if you don\'t want to.',
                Language(['RUS']): 'Пожалуйста, пришлите мне свое фото, чтобы я знал, как вы выглядите, '
                                           'или отправьте /skip, если не хотите. '
            },
            current_lang=self.lang
        )

        self.keyboard.reset()

        self.keyboard.fallback_keys = [Key('/cancel'), Key('/lang')]

    def handle_response(self, update, context):
        genders = {'Man': 'MAN', 'Woman': 'WOMAN', 'Other': 'OTHER',
                   'Мужчина': 'MAN', 'Женщина': 'WOMAN', 'Другое': 'OTHER'}
        self._user.gender = genders[update.message.text]
        return self.state_index.next()


class Photo(UserInfoConversationState):
    def __init__(self, state_index: StateIndex, lang: Language, user: User):
        super().__init__(state_index, lang, user)

        self.phrase = MLT(
            {
                Language(['ENG']): 'Gorgeous! Now, send me your location please, or send /skip if you don\'t want to.',
                Language(['RUS']): 'Великолепно! Теперь пришлите мне свое местоположение '
                                  'или отправьте /skip, если не хотите'

            },
            current_lang=self.lang
        )

        self.keyboard.fallback_keys = [Key('/cancel'), Key('/lang'), Key('/skip')]

    def handle_response(self, update, context):
        photo_file = update.message.photo[-1].get_file()
        photo_path = f'images/{uuid.uuid4()}.jpg'
        photo_file.download(photo_path)
        self._user.photo_path = photo_path
        return self.state_index.next()


class SkipPhoto(UserInfoConversationState):
    def __init__(self, state_index: StateIndex, lang: Language, user: User):
        super().__init__(state_index, lang, user)

        self.phrase = MLT(
            {
                Language(['ENG']): 'I bet you look great! Now, send me your location please, or send /skip.',
                Language(['RUS']): 'Бьюсь об заклад, ты отлично выглядишь! А теперь пришлите мне ваше местоположение '
                                  'или отправьте /skip.'

            },
            current_lang=self.lang
        )

        self.keyboard.fallback_keys = [Key('/cancel'), Key('/lang'), Key('/skip')]

    def handle_response(self, update, context):
        return self.state_index.next()


class Location(UserInfoConversationState):
    def __init__(self, state_index: StateIndex, lang: Language, user: User):
        super().__init__(state_index, lang, user)

        self.phrase = MLT(
            {
                Language(['ENG']): 'Maybe I can visit you sometime! At last, tell me something about yourself.',
                Language(['RUS']): 'Может быть, я смогу навестить тебя когда-нибудь! '
                                  'Наконец-то расскажи мне что-нибудь о себе.',
            },
            current_lang=self.lang
        )

        self.keyboard.fallback_keys = [Key('/cancel'), Key('/lang')]
        self.keyboard.input_field_placeholder = 'Something about yourself'

    def handle_response(self, update, context):
        user = update.message.from_user
        user_location = update.message.location
        self._user.latitude = user_location.latitude
        self._user.longitude = user_location.longitude
        return self.state_index.next()


class SkipLocation(UserInfoConversationState):
    def __init__(self, state_index: StateIndex, lang: Language, user: User):
        super().__init__(state_index, lang, user)

        self.phrase = MLT(
            {
                Language(['ENG']): 'You seem a bit paranoid! At last, tell me something about yourself.',
                Language(['RUS']): 'А ты немного параноик, верно? Наконец-то расскажи мне что-нибудь о себе',
            },
            current_lang=self.lang
        )

        self.keyboard.fallback_keys = [Key('/cancel'), Key('/lang')]
        self.keyboard.input_field_placeholder = 'Something about yourself'

    def handle_response(self, update, context):
        return self.state_index.next()


class Bio(UserInfoConversationState):
    def __init__(self, state_index: StateIndex, lang: Language, user: User):
        super().__init__(state_index, lang, user)

        self.phrase = MLT(
            {
                Language(['ENG']): 'Thank you! I hope we can talk again some day.',
                Language(['RUS']): 'Спасибо! Я надеюсь, что когда-нибудь мы сможем снова поговорить.',
            },
            current_lang=self.lang
        )

        self._keyboard.reset(fallback_keys_too=True)
        self.keyboard.fallback_keys = [Key('/start'), Key('/lang')]

    def handle_response(self, update, context):
        self._user.bio = update.message.text
        self._user.save()
        self._user = User()
        return ConversationHandler.END


class Cancel(UserInfoConversationState):
    def __init__(self, state_index: StateIndex, lang: Language, user: User):
        super().__init__(state_index, lang, user)

        self.phrase = MLT(
            {
                Language(['ENG']): 'Bye! I hope we can talk again some day.',
                Language(['RUS']): 'Спасибо! Я надеюсь, что когда-нибудь мы сможем снова поговорить.'
            },
            current_lang=self.lang
        )

        self._keyboard.reset(fallback_keys_too=True)
        self.keyboard.fallback_keys = [Key('/start'), Key('/lang')]

    def handle_response(self, update, context):
        return ConversationHandler.END


class AskLanguage(UserInfoConversationState):
    def __init__(self, state_index: StateIndex, lang: Language, user: User):
        super().__init__(state_index, lang, user)

        self.phrase = MLT(
            {
                Language(['ENG']): 'Choose your language',
                Language(['RUS']): 'Выберите язык',
            },
            current_lang=self.lang
        )

        self._keyboard.keys = [[Key('Eng'), Key('Rus')]]

        self._keyboard.fallback_keys = [Key('/cancel')]

    def handle_response(self, update, context):
        return self.state_index.get_state('CHANGE_LANGUAGE')


class ChangeLanguage(UserInfoConversationState):
    def __init__(self, state_index: StateIndex, lang: Language, user: User):
        super().__init__(state_index, lang, user)

        self.phrase = MLT(
            {
                Language(['ENG']): f'The language has been changed.',
                Language(['RUS']): f'Язык был изменён.',
            },
            current_lang=self.lang
        )

        self.keyboard.reset()

        self.keyboard.fallback_keys = [Key('/cancel'), Key('/lang')]
        self.keyboard.input_field_placeholder = ''

    def handle_response(self, update, context):
        language = update.message.text
        self.lang.current = language.upper()  # TODO назначение языка в виде строки
        return self.state_index.current


class UserInfoConversationBot(ConversationBot):
    def __init__(self, api_key: str, conversation: Conversation = None,  **kwargs):
        super().__init__(api_key, conversation, **kwargs)
        self._conversation = SimpleConversation()
        self._user = User()

        self._entry_points = [
            CommandHandler(
                'start',
                Start(self.conversation.state, self.conversation.lang, self._user).run
            )
        ]
        self._states = {
                self.conversation.state.states['GENDER']: [
                    MessageHandler(
                        Filters.regex('^(Man|Woman|Other|Мужчина|Женщина|Другое)$'),
                        Gender(self.conversation.state, self.conversation.lang, self._user).run
                    )
                ],
                self.conversation.state.states['PHOTO']: [
                    MessageHandler(
                        Filters.photo,
                        Photo(self.conversation.state, self.conversation.lang, self._user).run
                    ),
                    CommandHandler(
                        'skip',
                        SkipPhoto(self.conversation.state, self.conversation.lang, self._user).run
                    )
                ],
                self.conversation.state.states['LOCATION']: [
                    MessageHandler(
                        Filters.location,
                        Location(self.conversation.state, self.conversation.lang, self._user).run
                    ),
                    CommandHandler(
                        'skip',
                        SkipLocation(self.conversation.state, self.conversation.lang, self._user).run
                    )
                ],
                self.conversation.state.states['BIO']: [
                    MessageHandler(
                        Filters.text & ~Filters.command,
                        Bio(self.conversation.state, self.conversation.lang, self.user).run
                    )
                ],
                self.conversation.state.states['CHANGE_LANGUAGE']: [
                    MessageHandler(
                        Filters.regex('^(Eng|Rus)$'),
                        ChangeLanguage(self.conversation.state, self.conversation.lang, self._user).run
                    )
                ]
            }
        self._fallbacks = [
            CommandHandler(
                'cancel',
                Cancel(self.conversation.state, self.conversation.lang, self._user).run
            ),
            CommandHandler(
                'lang',
                AskLanguage(self.conversation.state, self.conversation.lang, self._user).run
            )
        ]

        conv_handler = ConversationHandler(
            entry_points=self._entry_points,
            states=self._states,
            fallbacks=self._fallbacks,
            allow_reentry=self._allow_reentry,
            per_chat=self._per_chat,
            per_user=self._per_user,
            per_message=self._per_message,
            conversation_timeout=self._conversation_timeout,
            name=self._name,
            persistent=self._persistent,
            map_to_parent=self._map_to_parent,
            run_async=self._run_async,
        )

        self._dispatcher.add_handler(conv_handler)

    def run(self):
        self._updater.start_polling()
        self._updater.idle()

    @property
    def user(self):
        return self._user

    @user.setter
    def user(self, val):
        if isinstance(val, User):
            self._user = val
        else:
            raise Exception('Val is not User!')

