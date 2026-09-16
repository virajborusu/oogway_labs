import logging
import sys

try:
    import structlog
    HAS_STRUCTLOG = True
except ImportError:
    HAS_STRUCTLOG = False

from app.core.config import settings


def setup_logging():
    logging.basicConfig(
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        stream=sys.stdout,
        level=getattr(logging, settings.LOG_LEVEL.upper(), logging.INFO),
    )

    if HAS_STRUCTLOG:
        structlog.configure(
            processors=[
                structlog.contextvars.merge_contextvars,
                structlog.processors.add_log_level,
                structlog.processors.StackInfoRenderer(),
                structlog.dev.set_exc_info,
                structlog.processors.TimeStamper(fmt="iso"),
                structlog.processors.JSONRenderer(),
            ],
            wrapper_class=structlog.make_filtering_bound_logger(
                getattr(logging, settings.LOG_LEVEL.upper(), logging.INFO)
            ),
            context_class=dict,
            logger_factory=structlog.PrintLoggerFactory(),
            cache_logger_on_first_use=True,
        )


class SimpleLoggerAdapter:
    def __init__(self):
        self._logger = logging.getLogger("lenny_assistant")

    def info(self, event, **kwargs):
        self._logger.info(f"{event} {kwargs if kwargs else ''}")

    def warning(self, event, **kwargs):
        self._logger.warning(f"{event} {kwargs if kwargs else ''}")

    def error(self, event, **kwargs):
        self._logger.error(f"{event} {kwargs if kwargs else ''}")


if HAS_STRUCTLOG:
    logger = structlog.get_logger()
else:
    logger = SimpleLoggerAdapter()

