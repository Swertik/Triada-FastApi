from triada.config.settings import GROUP_ID, JUDGE_CHAT_ID
from triada.api.vk_api import send_message
from fastapi.responses import PlainTextResponse
from triada.utils.patterns import BATTLE_PLAYERS_PATTERN, MESSAGE_PATTERN
from triada.config.logg import logger
from triada.commands.judje_commands import VerdictCommand, CloseCommand, OpenCommand, PauseCommand, RePauseCommand, ExtendCommand, SuspectsCommand, HelloCommand
from typing import Optional, Tuple


async def handle_message(message: dict):
    if message["text"].startswith("."):
        logger.info(f"Received message: {message}")
        command, link, text = await parse_message(message)
        command, text = command.strip(), text.strip()
        if message["peer_id"] == JUDGE_CHAT_ID:
            await handle_battle_commands(command, link, text, message)
            return {'response': 'ok', 'status': 200, 'message': 'Message from judges', 'peer_id': message['peer_id'], 'command': command}
        else:
            return {'response': 'ok', 'status': 200, 'message': 'Message from user', 'peer_id': message['peer_id'], 'command': command}
        
    return {'response': 'ok', 'status': 200, 'message': 'Not a command', 'peer_id': message['peer_id']}


async def handle_battle_commands(command: str, link: int, text: str, message: dict) -> None:
    """
    Обрабатывает команды, связанные с боями
    """
    commands = {
        'вердикт': lambda: VerdictCommand(link, text, message['peer_id'], message.get('attachments', [])),
        'закрыть': lambda: CloseCommand(link, text, message['peer_id']),
        'открыть': lambda: OpenCommand(link, text, message['peer_id']),
        'пауза': lambda: PauseCommand(link, text, message['peer_id']),
        'возобновить': lambda: RePauseCommand(link, text, message['peer_id']),
        'продление': lambda: ExtendCommand(link, text, message['peer_id']),
        'подсудимые': lambda: SuspectsCommand(link=message['from_id'], text='', peer_id=message['peer_id']),
        'привет': lambda: HelloCommand(message['peer_id'])
    }

    if command_creator := commands.get(command.lower()):
        logger.info(f"Executing command: {command}")
        try:
            text = await command_creator().execute()
            logger.debug(f"Command executed: {text}")
            return {'response': 'ok', 'status': 200, 'message': message['text'], 'peer_id': message['peer_id'], 'answer': text}
        except Exception as e:
            logger.error(f"Error executing command: {e}")
            return {'response': 'ok', 'status': 200, 'message': 'Not a command', 'peer_id': message['peer_id']}

async def parse_message(msg: dict) -> Optional[Tuple[str, str, str]]:
    """
    Разбирает сообщение на команду, ссылку и текст
    
    Returns:
        Tuple[команда, ссылка, текст] или None если сообщение не соответствует паттерну
    """
    if pattern := MESSAGE_PATTERN.match(msg['text']):
        return pattern.groups()
    return None