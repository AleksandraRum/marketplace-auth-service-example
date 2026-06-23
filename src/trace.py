import contextvars

_trace_id_var: contextvars.ContextVar[str] = contextvars.ContextVar(
    "trace_id", default=""
)


def get_trace_id() -> str:
    return _trace_id_var.get()


def set_trace_id(trace_id: str) -> contextvars.Token[str]:
    return _trace_id_var.set(trace_id)


def reset_trace_id(token: contextvars.Token[str]) -> None:
    _trace_id_var.reset(token)
