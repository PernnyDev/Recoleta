"""config.py"""

from typing import Tuple

# Flask configuration
class Config:
    SECRET_KEY: str = 'your-secret-key'
    SQLALCHEMY_DATABASE_URI: str = 'sqlite:///site.db'
    SQLALCHEMY_TRACK_MODIFICATIONS: bool = False

    # Flask-Mail configuration
    MAIL_SERVER: str = 'smtp.googlemail.com'
    MAIL_PORT: int = 587
    MAIL_USE_TLS: bool = True
    MAIL_USERNAME: str = 'your-email@gmail.com'
    MAIL_PASSWORD: str = 'your-password'
    ADMINS: Tuple[str, ...] = ('your-email@gmail.com',)

    # Flask-SocketIO configuration
    SOCKETIO_MESSAGE_QUEUE: str = 'redis://'
