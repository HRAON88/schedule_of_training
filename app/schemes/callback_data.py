from pydantic import BaseModel


class CallBackData(BaseModel):
    tag: str
    trace_id: str | None = None
