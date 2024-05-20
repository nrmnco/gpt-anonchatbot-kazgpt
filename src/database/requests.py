from datetime import datetime, timedelta, timezone

from src.database.models import async_session
from src.database.models import User, ChatSession, ChatSessionLog, Queue, Friend

from time import sleep, time

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

        ch = await session.scalar(
            select(ChatSessionLog).where(
                or_(ChatSessionLog.user_tg_id_1 == tg_id_2 and ChatSessionLog.user_tg_id_2 == tg_id_1,
                    ChatSessionLog.user_tg_id_2 == tg_id_2 and ChatSessionLog.user_tg_id_1 == tg_id_1))
        )
        if ch:
            await session.execute(
                update(ChatSessionLog)
                .where(ChatSessionLog.session_id == ch.session_id)
                .values(date_and_time=datetime.now(timezone.utc))
            )
        else:
            session.add(
                ChatSessionLog(user_tg_id_1=tg_id_1, user_tg_id_2=tg_id_2, date_and_time=datetime.now(timezone.utc)))

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
        time_threshold = datetime.now(timezone.utc) - timedelta(hours=24)

        result = await session.execute(select(Queue))
        records = result.scalars().all()

        for record in records:
            ch = await session.scalar(
                select(ChatSessionLog).where(or_(
                    (ChatSessionLog.user_tg_id_1 == record.user_tg_id) &
                    (ChatSessionLog.user_tg_id_2 == tg_id),
                    (ChatSessionLog.user_tg_id_2 == record.user_tg_id) &
                    (ChatSessionLog.user_tg_id_1 == tg_id)
                ))
            )

            if record.user_tg_id == tg_id:
                continue
            else:
                if ch:
                    if ch.date_and_time < time_threshold:
                        await session.execute(
                            update(ChatSessionLog)
                            .where(ChatSessionLog.session_id == ch.session_id)
                            .values(date_and_time=datetime.now(timezone.utc))
                        )
                        await session.execute(
                            delete(Queue).where(Queue.user_tg_id == record.user_tg_id)
                        )
                        await session.execute(
                            delete(Queue).where(Queue.user_tg_id == tg_id)
                        )
                        await session.commit()
                        return record

                    else:
                        continue
                await session.execute(
                    delete(Queue).where(Queue.user_tg_id == record.user_tg_id)
                )
                await session.execute(
                    delete(Queue).where(Queue.user_tg_id == tg_id)
                )
                await session.commit()
                return record

        return None

async def get_friends(tg_id):
    async with async_session() as session:
        friends = await session.scalar(select(Friend).where(Friend.user_tg_id == tg_id))
        if friends:
            return friends

async def add_friend(tg_id, interlocutor_tg_id, nickname):
    async with async_session() as session:
        friend_object = await get_friends(tg_id)
        if friend_object:
            friends = friend_object.friends
            friends[interlocutor_tg_id] = nickname
            await session.execute(update(Friend).where(Friend.user_tg_id == tg_id).values(friends=friends))
            await session.commit()
        else:
            friends = {interlocutor_tg_id: nickname}
            session.add(Friend(user_tg_id=tg_id, friends=friends))
            await session.commit()


async def delete_friend(tg_id, interlocutor_tg_id):
    async with async_session() as session:
        friends = (await get_friends(tg_id)).friends
        friends.pop(str(interlocutor_tg_id))
        await session.execute(update(Friend).where(Friend.user_tg_id == tg_id).values(friends=friends))
        await session.commit()


async def get_people_online():
    async with async_session() as session:
        total_counter = 0

        queue_counter = await session.execute(
            select(func.count()).select_from(Queue)
        )
        session_counter = await session.execute(
            select(func.count()).select_from(ChatSession)
        )

        total_counter += queue_counter.scalar()
        total_counter += 2*session_counter.scalar()


        return total_counter

async def delete_old_rows():
    async with async_session() as session:
        now = datetime.now()
        time_threshold = now - timedelta(hours=24)
        await session.execute(
            delete(ChatSessionLog).where(ChatSessionLog.date_and_time < time_threshold)
        )
        await session.commit()