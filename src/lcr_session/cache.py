__all__ = ["SavedSession", "SessionCache", "FileCache"]

import json
from abc import ABC, abstractmethod
from dataclasses import asdict, dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Any, Dict


class DateTimeEncoder(json.JSONEncoder):
    def default(self, o) -> Any:
        if isinstance(o, datetime):
            return {
                "_type": "datetime",
                "value": o.isoformat(),
            }
        return super().default(o)


class DateTimeDecoder(json.JSONDecoder):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(object_hook=self.object_hook, *args, **kwargs)

    def object_hook(self, o) -> Any:  # type: ignore
        if "_type" in o and o["_type"] == "datetime":
            return datetime.fromisoformat(o["value"])
        return o


@dataclass
class SavedSession:
    cookies: Dict[str, Any] = field(default_factory=dict)
    token: str = ""
    expires: datetime = field(default_factory=datetime.now)


class SessionCache(ABC):
    def __init__(self) -> None:
        super().__init__()

    @abstractmethod
    def save_session(self, session: SavedSession) -> None:
        pass

    @abstractmethod
    def load_session(self) -> SavedSession:
        pass


class FileCache(SessionCache):
    def __init__(self, session_file: str | Path) -> None:
        super().__init__()
        self._session_file = Path(session_file)

    def save_session(self, session: SavedSession) -> None:
        data = asdict(session)
        self._session_file.write_text(
            json.dumps(data, indent=4, sort_keys=True, cls=DateTimeEncoder)
        )

    def load_session(self) -> SavedSession:
        if not self._session_file.exists():
            return SavedSession()
        with self._session_file.open("rt") as fp:
            data = json.load(fp, cls=DateTimeDecoder)
        session = SavedSession(**data)
        return session
