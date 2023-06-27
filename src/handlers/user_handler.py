from src.models.user import User


class UserHandler:

    @staticmethod
    def add_user(chat_id, session):
        try:
            user = User(chat_id)
            session.add(user)
            session.commit()
            print("Пользователь успешно создан.")
        except Exception as e:
            print("Ошибка при создании пользователя:", str(e))
            session.rollback()


    # @staticmethod
    # def get_user(chat_id, session):
    #     user = session.query(User).get(chat_id)
    #
    #     return user
