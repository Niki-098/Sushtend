from pydantic import BaseModel


class TranscriptIn(BaseModel):
    transcript: str
