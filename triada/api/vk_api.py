from fastapi import FastAPI, Request, status
from fastapi.responses import PlainTextResponse
from pydantic import BaseModel
import httpx
from triada.config.settings import GROUP_TOKEN, MY_TOKEN, GROUP_ID
import asyncio
from random import randint

app = FastAPI()

class VkBotEventType():
    MESSAGE_NEW = 'message_new'
    MESSAGE_REPLY = 'message_reply'
    MESSAGE_EDIT = 'message_edit'
    MESSAGE_EVENT = 'message_event'

    MESSAGE_TYPING_STATE = 'message_typing_state'

    MESSAGE_ALLOW = 'message_allow'

    MESSAGE_DENY = 'message_deny'

    PHOTO_NEW = 'photo_new'

    PHOTO_COMMENT_NEW = 'photo_comment_new'
    PHOTO_COMMENT_EDIT = 'photo_comment_edit'
    PHOTO_COMMENT_RESTORE = 'photo_comment_restore'

    PHOTO_COMMENT_DELETE = 'photo_comment_delete'

    AUDIO_NEW = 'audio_new'

    VIDEO_NEW = 'video_new'

    VIDEO_COMMENT_NEW = 'video_comment_new'
    VIDEO_COMMENT_EDIT = 'video_comment_edit'
    VIDEO_COMMENT_RESTORE = 'video_comment_restore'

    VIDEO_COMMENT_DELETE = 'video_comment_delete'

    WALL_POST_NEW = 'wall_post_new'
    WALL_REPOST = 'wall_repost'

    WALL_REPLY_NEW = 'wall_reply_new'
    WALL_REPLY_EDIT = 'wall_reply_edit'
    WALL_REPLY_RESTORE = 'wall_reply_restore'

    WALL_REPLY_DELETE = 'wall_reply_delete'

    BOARD_POST_NEW = 'board_post_new'
    BOARD_POST_EDIT = 'board_post_edit'
    BOARD_POST_RESTORE = 'board_post_restore'

    BOARD_POST_DELETE = 'board_post_delete'

    MARKET_COMMENT_NEW = 'market_comment_new'
    MARKET_COMMENT_EDIT = 'market_comment_edit'
    MARKET_COMMENT_RESTORE = 'market_comment_restore'

    MARKET_COMMENT_DELETE = 'market_comment_delete'

    GROUP_LEAVE = 'group_leave'

    GROUP_JOIN = 'group_join'

    USER_BLOCK = 'user_block'

    USER_UNBLOCK = 'user_unblock'

    POLL_VOTE_NEW = 'poll_vote_new'

    GROUP_OFFICERS_EDIT = 'group_officers_edit'

    GROUP_CHANGE_SETTINGS = 'group_change_settings'

    GROUP_CHANGE_PHOTO = 'group_change_photo'

    VKPAY_TRANSACTION = 'vkpay_transaction'

    CONFIRMATION = 'confirmation'


async def send_message(peer_id: int, text: str, attachments: list = []):
    """
    Отправляет сообщение через группу ВК
    
    Args:
        peer_id: ID получателя
        msg: текст сообщения
        attachments: список вложений
    
    Returns:
        json: ответ от ВК
    """
    async with httpx.AsyncClient() as client:
        response = await client.post(
            "https://api.vk.com/method/messages.send",
            params={
                "access_token": GROUP_TOKEN,  # Токен сообщества
                "peer_id": peer_id,
                "message": text,
                "random_id": randint(1, 1000000000),  # Уникальный идентификатор (можно использовать random.randint)
                "v": "5.199",     # Версия API (актуальная)
                "attachment": attachments
            }
        )
    return PlainTextResponse("ok")



async def send_comment(post_id: int, text: str, attachments: list = []):
    """
    Отправляет комментарий к посту
    
    Args:
        post_id: ID поста
        text: текст комментария
    
    Returns:
        json: ответ от ВК
    """
    async with httpx.AsyncClient() as client:
        response = await client.post(
            "https://api.vk.com/method/wall.createComment",
            params={
                "owner_id": -GROUP_ID,
                "access_token": GROUP_TOKEN,
                "post_id": post_id,
                "message": text,
                "v": "5.199",
                "attachment": attachments
            }
        )
    return PlainTextResponse("ok")


async def getUploadServer(album_id: int):
    """
    Получает URL для загрузки фотографий
    
    Args:
        group_id: ID группы
        album_id: ID альбома
    """
    async with httpx.AsyncClient() as client:
        response = await client.post(
            "https://api.vk.com/method/photos.getUploadServer",
            params={
                "access_token": MY_TOKEN,
                "group_id": GROUP_ID,
                "album_id": album_id,
                "v": "5.199"
            }
        )
    return response.json()


async def closeComments(post_id: int):
    async with httpx.AsyncClient() as client:
        response = await client.post(
            "https://api.vk.com/method/wall.closeComments",
            params={"owner_id": -GROUP_ID, "post_id": post_id, "v": "5.199"}
        )
    return PlainTextResponse("ok")


async def openComments(post_id: int):
    async with httpx.AsyncClient() as client:
        response = await client.post(
            "https://api.vk.com/method/wall.openComments",
            params={"owner_id": -GROUP_ID, "post_id": post_id, "v": "5.199"}
        )
    return PlainTextResponse("ok")


async def uploadPhoto(upload_url: str, photo: str):
    """
    Загружает фотографию на сервер
    
    Args:
        upload_url: URL для загрузки фотографий
        photo: полный путь к фотографии
    
    Returns:
        json: ответ от ВК
    """
    async with httpx.AsyncClient() as client:
        with open(photo, "rb") as f:
            response = await client.post(
                upload_url,
                files={
                    "file": ('test.jpeg', f, "image/jpeg")
                }
            )
    return response.json()


async def savePhoto(server: str, photos_list: str, aid: int, hash: str, gid: int):
    """
    Сохраняет фотографию на сервер
    
    Args:
        server: сервер для загрузки фотографий
        photo: фотография
        hash: хэш фотографии
    
    Returns:
        json: ответ от ВК
    """

    async with httpx.AsyncClient() as client:
        response = await client.post(
            "https://api.vk.com/method/photos.save",
            params={
                "access_token": MY_TOKEN,
                "server": server,
                "photos_list": photos_list,
                "hash": hash,
                "album_id": aid,
                "group_id": gid,
                "v": "5.199"
            }
        )
    return PlainTextResponse("ok")

class LoadPhotoModel(BaseModel):
    album_id: int
    photo: str


async def LoadPhoto(data: LoadPhotoModel):
    upload_server = await getUploadServer(data.album_id)
    upload_url = upload_server["response"]["upload_url"]
    upload_photo = await uploadPhoto(upload_url, data.photo)
    saved_photo = await savePhoto(**upload_photo)
    return saved_photo


@app.get("/opa")
async def root():
    return {"message": "Hello World"}


if __name__ == "__main__":
    asyncio.run(send_comment(1,'fff'))
    #import uvicorn
    #uvicorn.run("vk_api:app", host="26.208.140.30", port=8080, reload=True)