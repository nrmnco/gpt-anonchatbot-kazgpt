from src.database.models import async_session
from src.database.models import User, ChatSession, Queue, Friend
from sqlalchemy import func, select, update, delete, or_

async def set_user(tg_id, bio) -> None:
    async with async_session() as session:
        session.add(User(user_tg_id = tg_id, bio = bio, credits = 0))
        await session.commit()

async def get_bio(tg_id):
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.user_tg_id == tg_id))
        if user:
            return user.bio
        
async def update_bio(tg_id, new_bio):
    async with async_session() as session:
        await session.execute(update(User).where(User.user_tg_id == tg_id).values(bio=new_bio))
        await session.commit()
        

async def check_user(tg_id) -> bool:
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.user_tg_id == tg_id))
        if user:
            return True
        
        return False
    
async def add_session(tg_id_1, tg_id_2) -> None:
    async with async_session() as session:
        session.add(ChatSession(user_tg_id_1 = tg_id_1, user_tg_id_2 = tg_id_2))
        await session.commit()

async def get_interlocutor_id(tg_id):
    async with async_session() as session:
        user = await session.scalar(select(ChatSession).where(or_(ChatSession.user_tg_id_1 == tg_id, ChatSession.user_tg_id_2 == tg_id)))
        if user.user_tg_id_1 == tg_id:
            return user.user_tg_id_2
        elif user.user_tg_id_2 == tg_id:
            return user.user_tg_id_1

        return None
async def is_in_session(tg_id):
    async with async_session() as session:
        user = await session.scalar(select(ChatSession).where(or_(ChatSession.user_tg_id_1 == tg_id, ChatSession.user_tg_id_2 == tg_id)))
        if user:
            return True
        return False
        
    
async def delete_session(tg_id):
    async with async_session() as session:
        await session.execute(delete(ChatSession).where(or_(ChatSession.user_tg_id_1 == tg_id, ChatSession.user_tg_id_2 == tg_id)))
        await session.commit()

async def add_to_queue(tg_id):
    async with async_session() as session:
        try:
            session.add(Queue(user_tg_id = tg_id))
            await session.commit()
        except:
            pass

async def delete_from_queue(tg_id):
    async with async_session() as session:
        await session.execute(
            delete(Queue).where(Queue.user_tg_id == tg_id)
        )
        await session.commit()

async def get_random_record(tg_id):
    async with async_session() as session:
        count = await session.execute(
            select(func.count()).select_from(Queue)
        )
        
        count = count.scalar()
        if count > 1:
            random_record = await session.scalar(
                select(Queue).order_by(func.random()).limit(1)
            )

            while random_record.user_tg_id == tg_id:
                random_record = await session.scalar(
                    select(Queue).order_by(func.random()).limit(1)
                )

            await delete_from_queue(random_record.user_tg_id)
            await delete_from_queue(tg_id)
            return random_record
        return False

async def get_friends(tg_id):
    async with async_session() as session:
        friends = await session.scalar(select(Friend).where(Friend.user_tg_id == tg_id))
        if friends:
            return friends.friends

async def add_friend(tg_id, interlocutor_tg_id, nickname):
    async with async_session() as session:
        friends = await get_friends(tg_id)
        if friends:
            friends[interlocutor_tg_id] = nickname
            await session.execute(update(Friend).where(Friend.user_tg_id == tg_id).values(friends=friends))
            await session.commit()
        else:
            friends = {interlocutor_tg_id: nickname}
            session.add(Friend(user_tg_id=tg_id, friends=friends))
            await session.commit()
