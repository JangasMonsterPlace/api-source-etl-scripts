from datetime import datetime
from dataclasses import dataclass
from typing import Optional


@dataclass
class TransformedTextData:
    id: str
    source: str     # twitter, youtube, file, ...
    text: str
    user: str
    written_by_user_at: datetime
    sentiment: Optional[float] = None
