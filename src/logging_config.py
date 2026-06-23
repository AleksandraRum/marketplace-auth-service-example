import logging

from src.trace import get_trace_id

_FORMAT = "%(asctime)s %(levelname)s [%(name)s] [trace_id=%(trace_id)s] %(message)s"


class TraceFilter(logging.Filter):
    def filter(self, record: logging.LogRecord) -> bool:
        record.trace_id = get_trace_id()  # type: ignore[attr-defined]
        return True


def configure_logging() -> None:
    handler = logging.StreamHandler()
    handler.addFilter(TraceFilter())
    handler.setFormatter(logging.Formatter(_FORMAT))
    logging.basicConfig(handlers=[handler], level=logging.INFO, force=True)
