"""
Реализации команд для судьи
"""
from typing import List
from triada.api.vk_api import send_message, send_comment, closeComments, openComments
from triada.api.db_api import get_battle, get_user
from triada.config.settings import GROUP_ID, JUDGE_CHAT_ID
from .base import BaseCommand
from triada.api.db_api import engine, Battles
from sqlmodel import Session, select, text

JUDGE_COMMANDS = [
    "вердикт",
    "закрыть",
    "открыть",
    "пауза",
    "снять паузу",
    "продлить",
    "подсудимые",]

class VerdictCommand(BaseCommand):
    def __init__(self, link: int, text: str, peer_id: int, attachments: List[dict]):
        super().__init__(link, text, peer_id)
        self.attachments = attachments

    async def _execute_command(self) -> None:
        attachment_lst = [] # TODO: Добавить вложения
        await send_comment(self.link, self.text, attachments=attachment_lst)

    async def _send_success_message(self) -> None:
        await send_message(self.peer_id, 'Комментарий в пост размещен!')


class CloseCommand(BaseCommand):
    async def _execute_command(self) -> None:
        await closeComments(self.link)

    async def _send_success_message(self) -> None:
        await send_message(self.peer_id, 'Пост закрыт!')

class OpenCommand(BaseCommand):
    async def _execute_command(self) -> None:
        await openComments(self.link)

    async def _send_success_message(self) -> None:
        await send_message(self.peer_id, 'Пост открыт!')

class PauseCommand(BaseCommand):
    async def _execute_command(self) -> None:
        with Session(engine) as session:
            battle = session.exec(select(Battles).where(Battles.link == self.link)).one()
            battle.status = 'paused'
            session.add(battle)
            session.commit()
        send_comment(self.link, comment="УВЕДОМЛЕНИЕ\n\nБой поставлен на паузу")

    async def _needs_commit(self) -> bool:
        return True

    async def _send_success_message(self) -> None:
        await send_message(JUDGE_CHAT_ID, 'Бой успешно поставлен на паузу!')

class RePauseCommand(BaseCommand):
    async def _execute_command(self) -> None:
        with Session(engine) as session:
            battle = session.exec(select(Battles).where(Battles.link == self.link)).one()
            battle.status = 'active'
            session.add(battle)
            session.commit()
        send_comment(self.link, comment="УВЕДОМЛЕНИЕ\n\nБой снят с паузы")

    async def _needs_commit(self) -> bool:
        return True
    
    async def _send_success_message(self) -> None:
        await send_message(JUDGE_CHAT_ID, 'Бой успешно снят с паузы!')

class ExtendCommand(BaseCommand):
    async def _execute_command(self) -> None:
        with Session(engine) as session:
            query = text("SELECT * FROM process_add_time(:link, :time)")  # Имя функции в PostgreSQL
            result = session.exec(query, {"link": self.link, "time": self.text})
            stats = result.fetchone()  # Получение результата
            print(stats)
        send_comment(self.link, comment=f"УВЕДОМЛЕНИЕ\n\nБой продлён на {self.text} часов.")

    async def _needs_commit(self) -> bool:
        return True

    async def _send_success_message(self) -> None:
        await send_message(JUDGE_CHAT_ID, 'В бою успешно проведено продление!')


class SuspectsCommand(BaseCommand):

    async def _execute_command(self) -> None:
        with Session(engine) as session:
            result = session.exec(select(Battles).where(Battles.judge_id == self.link))
            links = result.fetchall()
            print(links)
            suspects = "\n".join(f"https://vk.com/wall-{GROUP_ID}_{link[0]}" for link in links)
        send_message(self.peer_id, f"Подсудимые:\n\n{suspects}")
    
    async def _send_success_message(self) -> None:
        pass

class HelloCommand():
    def __init__(self, peer_id: int):
        self.peer_id = peer_id


    async def execute(self) -> None:
        text = 'Привет!'
        await send_message(self.peer_id, text)

        

