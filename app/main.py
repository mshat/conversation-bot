from user_info_conversation_bot import UserInfoConversationBot
from models import models
from settings import DB, CONFIG


def run_user_info_conversation():
    user_info_conversation = UserInfoConversationBot(CONFIG['API_KEY'])
    user_info_conversation.run()


def main():
    DB.connect()
    DB.create_tables(models)

    run_user_info_conversation()  # must be last line in the main function


if __name__ == "__main__":
    main()
    # try:
    #     main()
    # except Exception as e:
    #     print(f'Error!!! {e}')
    # finally:
    #     DB.close()



