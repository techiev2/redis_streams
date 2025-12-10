__all__ = ("logger", "INFO")

from logging import Logger, INFO, basicConfig

basicConfig(filename='redis-streams.log', level=INFO)
logger = Logger(name="redis-streams", level=INFO)
