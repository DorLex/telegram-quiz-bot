from logging import Logger, getLogger

logger: Logger = getLogger(__name__)


def log_query(query: str) -> None:
    logger.info(f'SQL Query: {query}')
