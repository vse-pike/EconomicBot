from src.models.user import User


class UserHandler:

    @staticmethod
    def add_user(chat_id, session):
        user = User(chat_id)

        session.add(user)
        session.commit()

    # @staticmethod
    # def get_user(chat_id, session):
    #     user = session.query(User).get(chat_id)
    #
    #     return user
