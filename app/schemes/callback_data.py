from pydantic import BaseModel


class CallBackData(BaseModel):
    tag: str | None = None
    trace_id: str | None = None
