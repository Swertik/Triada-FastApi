import logging

def setup_logging():
    logging.basicConfig(
        level=logging.DEBUG,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        filename=r'C:\Users\herob\PycharmProjects\Triada\main.log',
        filemode='a'
    )
    
    # Создаем корневой логгер
    root_logger = logging.getLogger()
    
    # Добавляем обработчик для вывода в консоль
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    console_handler.setFormatter(formatter)
    root_logger.addHandler(console_handler)

# Инициализируем логирование
setup_logging()

# Создаем логгер для текущего модуля
logger = logging.getLogger(__name__)