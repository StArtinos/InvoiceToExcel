import anthropic

import json
from collections import defaultdict
from operator import itemgetter

class ClaudeMF():
    def __init__(self,name="Bot",sys_prompt=""):
        self.client = anthropic.Anthropic( api_key="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")
        self.sys_prompt = sys_prompt
    def __str__(self):

        return f'Name: {self.name}, Job: {self.job}'
    def chat(self,prompt):
        message = self.client.messages.create(
            model="claude-3-haiku-20240307",
            max_tokens=4000,
            temperature=0.0,
            system=self.sys_prompt,
            messages=[{"role": "user",
                       "content": f"{prompt}"}]
        ).content[0].text
        return message