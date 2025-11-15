from typing import TypedDict, List, Optional

class ChatState(TypedDict):
    history: Optional[str]
    input: Optional[str]
    intent: Optional[str]
    response: Optional[str]