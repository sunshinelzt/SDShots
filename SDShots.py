# 🔒 Licensed under the GNU AGPLv3
# 🌐 https://www.gnu.org/licenses/agpl-3.0.html

# meta developer: @sunshinelzt

import io
from telethon.tl.types import Message, Document, Photo, Video, Voice, Audio
from .. import loader, utils


@loader.tds
class SDShotsMod(loader.Module):
    """Module to save self-destructing media"""

    strings = {
        "name": "SDShots",
        "usage": "🚫 <b>Please, reply to self-destructing media</b>",
    }

    strings_ru = {
        "usage": "🚫 <b>Пожалуйста, ответь на самоуничтожающееся фото</b>",
        "_cls_doc": "Модуль для сохранения самоуничтожающихся фото и медиа",
        "_cmd_doc_s": "<Реплай на самоуничтожающееся фото/видео/документ>",
    }

    async def scmd(self, message: Message):
        """<reply to self-destructing media>"""
        reply = await message.get_reply_message()

        # Check if the reply exists and contains media with TTL (time-to-live) property
        if not reply or not hasattr(reply.media, 'ttl_seconds') or not reply.media.ttl_seconds:
            return  # Do nothing if the media is not self-destructing

        # Delete the message to keep the process hidden
        await message.delete()

        # Handle different media types (Photo, Video, Audio, Voice, Document)
        file = None
        if isinstance(reply.media, Photo):
            file = io.BytesIO(await reply.download_media(bytes))
            file.name = reply.file.name if reply.file else "self_destructing_photo"
        elif isinstance(reply.media, Video):
            file = io.BytesIO(await reply.download_media(bytes))
            file.name = reply.file.name if reply.file else "self_destructing_video"
        elif isinstance(reply.media, Voice):
            file = io.BytesIO(await reply.download_media(bytes))
            file.name = reply.file.name if reply.file else "self_destructing_voice"
        elif isinstance(reply.media, Audio):
            file = io.BytesIO(await reply.download_media(bytes))
            file.name = reply.file.name if reply.file else "self_destructing_audio"
        elif isinstance(reply.media, Document):
            file = io.BytesIO(await reply.download_media(bytes))
            file.name = reply.file.name if reply.file else "self_destructing_document"

        # If file exists, send it to "me" (your personal Telegram) without notifying in the chat
        if file:
            await self._client.send_file("me", file)
