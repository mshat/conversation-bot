import sys
sys.path.append("..")
import datetime
from abc import ABC, abstractmethod
from telegram import ReplyKeyboardRemove
from telegram.ext import Updater
from tools.keyboard import MyReplyKeyboardMarkup
from tools.state_index import StateIndex
from app.multi_language_text import MultiLanguageText as MLT
from tools.language import Language
from logger.logger import Logger


class Conversation(ABC):
    def __init__(self, lang=Language(['ENG', 'RUS'])):
        self._state_index = None
        self._lang = lang

    @property
    def lang(self):
        return self._lang

    @lang.setter
    def lang(self, lang):
        self._lang = lang

    @property
    def state(self):
        return self._state_index


class ConversationBot(ABC):
    def __init__(
            self,
            api_key: str,
            conversation: Conversation = None,
            allow_reentry: bool = True,
            per_chat: bool = True,
            per_user: bool = True,
            per_message: bool = False,
            conversation_timeout: float | datetime.timedelta = None,
            name: str = None,
            persistent: bool = False,
            map_to_parent=None,
            run_async: bool = True,
    ):
        self._api_key = api_key
        self._conversation = conversation
        self._allow_reentry = allow_reentry
        self._per_chat = per_chat
        self._per_user = per_user
        self._per_message = per_message
        self._conversation_timeout = conversation_timeout
        self._name = name
        self._persistent = persistent
        self._map_to_parent = map_to_parent
        self._run_async = run_async

        self._updater = Updater(self._api_key)
        self._dispatcher = self._updater.dispatcher

    @property
    def conversation(self):
        return self._conversation

    @abstractmethod
    def run(self):
        pass


class ConversationState(ABC):
    def __init__(self, state_index: StateIndex, lang: Language):
        self._state_index = state_index
        self._keyboard = MyReplyKeyboardMarkup(lang)
        self._lang = lang
        self._logger = Logger(__name__, log_file_name='new_log.txt', print_start_message=True)
        self._phrase = None

    @property
    def phrase(self):
        self._phrase.current_lang = self.lang
        return self._phrase

    @phrase.setter
    def phrase(self, text: MLT):
        self._phrase = text

    @property
    def lang(self):
        return self._lang

    @property
    def state_index(self):
        return self._state_index

    @property
    def keyboard(self):
        return self._keyboard

    def run(self, update, context):
        # self._logger.info()  # TODO
        next_state = self.handle_response(update, context)
        self.say_phrase(update, context)
        return next_state

    @abstractmethod
    def handle_response(self, update, context):
        pass

    def say_phrase(self, update, context):
        context.bot.send_message(chat_id=update.effective_chat.id, text=self.phrase.text,
                                 reply_markup=self.keyboard.keyboard)



