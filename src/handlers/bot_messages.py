from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from states import MainState
from database.requests import get_interlocutor_id


router = Router()


@router.edited_message()
async def editing_messages(message: Message) -> None:
    interlocutor = get_interlocutor_id(message.from_user.id)
    
    if interlocutor:
        if message.text:
            await message.bot.edit_message_text(message.text, interlocutor, message.message_id + 1)
        elif message.caption:
            await message.bot.edit_message_caption(
                message.caption,
                interlocutor,
                message.message_id + 1,
                caption_entities=message.caption_entities,
                parse_mode=None
            )


@router.message(
    F.content_type.in_(
        [
            "text", "audio", "voice",
            "sticker", "document", "photo",
            "video"
        ]
    ), MainState.chatting
)
async def echo(message: Message, state:FSMContext) -> None:
    interlocutor = await get_interlocutor_id(message.from_user.id)
    
    if interlocutor:
        if message.content_type == "text":
            reply = None
            if message.reply_to_message:
                if message.reply_to_message.from_user.id == message.from_user.id:
                    reply = message.reply_to_message.message_id + 1
                else:
                    reply = message.reply_to_message.message_id - 1

            await message.bot.send_message(
                interlocutor,
                message.text,
                entities=message.entities,
                reply_to_message_id=reply,
                parse_mode=None
            )
        if message.content_type == "photo":
            await message.bot.send_photo(
                interlocutor,
                message.photo[-1].file_id,
                caption=message.caption,
                caption_entities=message.caption_entities,
                parse_mode=None,
            )
        if message.content_type == "audio":
            await message.bot.send_audio(
                interlocutor,
                message.audio.file_id,
                caption=message.caption,
                caption_entities=message.caption_entities,
                parse_mode=None
            )
        if message.content_type == "voice":
            await message.bot.send_voice(
                interlocutor,
                message.voice.file_id,
                caption=message.caption,
                caption_entities=message.caption_entities,
                parse_mode=None
            )
        if message.content_type == "document":
            await message.bot.send_document(
                interlocutor,
                message.document.file_id,
                caption=message.caption,
                caption_entities=message.caption_entities,
                parse_mode=None
            )
        if message.content_type == "sticker":
            await message.bot.send_sticker(
                interlocutor,
                message.sticker.file_id
            )
        if message.content_type == "video":
            await message.bot.send_video(
                interlocutor,
                message.video.file_id,
                caption=message.caption,
                caption_entities=message.caption_entities,
                parse_mode=None,
            )
