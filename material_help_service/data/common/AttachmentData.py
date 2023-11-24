from dataclasses import dataclass


@dataclass
class AttachmentData:
    id: int
    mime_type: str
    source: str
