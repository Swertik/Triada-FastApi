from triada.api.vk_api import send_message, send_comment, VkBotEventType
from triada.config.settings import GROUP_ID, GROUP_TOKEN
from triada.handlers.message import handle_message
from triada.handlers.post import handle_post
from triada.handlers.reply import handle_reply
from fastapi import FastAPI
from fastapi.responses import PlainTextResponse
app = FastAPI()


@app.post("/callback")
async def callback(data: dict):
    if data["type"] == VkBotEventType.CONFIRMATION:
        return {"type": "confirmation", "group_id": GROUP_ID}
    
    elif data["type"] == VkBotEventType.MESSAGE_NEW:
        await handle_message(data["object"]["message"])

    elif data["type"] == VkBotEventType.WALL_POST_NEW:
        await handle_post(data["object"]["wall_post"])

    elif data["type"] == VkBotEventType.WALL_REPLY_NEW:
        await handle_reply(data["object"]["wall_reply"])

    return PlainTextResponse("ok")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="26.208.140.30", port=8080, reload=True)

