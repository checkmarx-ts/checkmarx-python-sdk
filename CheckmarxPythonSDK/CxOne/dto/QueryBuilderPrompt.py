
class QueryBuilderPrompt(object):
    def __init__(self, prompt: str = None):
        self.prompt = prompt

    def __str__(self):
        return f"QueryBuilderPrompt(prompt={self.prompt})"
