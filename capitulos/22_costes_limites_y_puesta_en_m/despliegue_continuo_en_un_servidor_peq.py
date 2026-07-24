import logging
from logging.handlers import RotatingFileHandler

handler = RotatingFileHandler(
    "logs/agente.log",
    maxBytes=10 * 1024 * 1024,  # 10 MB por archivo
    backupCount=5               # conservar los últimos 5 archivos
)
handler.setFormatter(logging.Formatter(
    "%(asctime)s %(levelname)s %(name)s %(message)s"
))
logging.getLogger().addHandler(handler)
