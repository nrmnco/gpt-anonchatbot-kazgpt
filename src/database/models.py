from sqlalchemy import BigInteger, ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.ext.asyncio import AsyncAttrs, async_sessionmaker, create_async_engine

from config_reader import config

engine = create_async_engine(config.SQLALCHEMY_URL.get_secret_value())
async_session = async_sessionmaker(engine)

class Base(AsyncAttrs, DeclarativeBase):
    pass

class User(Base):
    __tablename__ = "users"
    
    user_tg_id = mapped_column(BigInteger, primary_key=True)
    bio: Mapped[str] = mapped_column()

class ChatSession(Base):
    __tablename__ = "chatsessions"

    session_id: Mapped[int] = mapped_column(primary_key=True)
    user_tg_id_1 = mapped_column(BigInteger, ForeignKey('users.user_tg_id'))
    user_tg_id_2 = mapped_column(BigInteger, ForeignKey('users.user_tg_id'))
    # user_tg_id_1 = mapped_column(BigInteger)
    # user_tg_id_2 = mapped_column(BigInteger)

class Queue(Base):
    __tablename__ = "queue"

    user_tg_id = mapped_column(BigInteger, primary_key=True)


async def async_main():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)