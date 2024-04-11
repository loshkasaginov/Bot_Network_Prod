import logging

# Создаем логгер
logger = logging.getLogger('logger')
logger.setLevel(logging.DEBUG)

# Создаем обработчик для записи логов в файл
file_handler = logging.FileHandler('logfile.log')
file_handler.setLevel(logging.DEBUG)

# Создаем обработчик для вывода логов на консоль
# console_handler = logging.StreamHandler()
# console_handler.setLevel(logging.DEBUG)

# Настраиваем форматирование
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)
# console_handler.setFormatter(formatter)

# Добавляем обработчики к логгеру
logger.addHandler(file_handler)
# logger.addHandler(console_handler)

# Тестовые сообщения
