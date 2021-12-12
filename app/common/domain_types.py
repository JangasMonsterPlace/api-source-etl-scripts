from datetime import datetime
from dataclasses import dataclass
from typing import Optional


@dataclass
class TransformedTextData:
    source_id: str
    source: str     # twitter, youtube, file, ...
    text: str
    use_case: str
    written_by_user_at: Optional[datetime] = None
    author: Optional[str] = None
    sentiment: Optional[float] = None
