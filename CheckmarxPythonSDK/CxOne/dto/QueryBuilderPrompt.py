from dataclasses import dataclass


@dataclass
class QueryBuilderPrompt:
    prompt: str = None

    def to_dict(self):
        return {
            "prompt": self.prompt
        }
