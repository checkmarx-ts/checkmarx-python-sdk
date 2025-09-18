from dataclasses import dataclass


@dataclass
class GPTMessage:
    role: str = None
    content: str = None


def construct_gpt_message(item):
    return GPTMessage(
        role=item.get("role"),
        content=item.get("content")
    )
