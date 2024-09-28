from openai import OpenAI


class ConditionedGPT:
    def __init__(self, model: str, prompt: str, samples: list[tuple[str, str]]):
        self.client = OpenAI()
        self.model = model

        self.messages = [{"role": "system", "content": prompt}]
        for sample in samples:
            self.messages.append({"role": "user", "content": sample[0]})
            self.messages.append({"role": "assistant", "content": sample[1]})

    def request(self, input: str) -> list[str]:
        msgs = self.messages.copy()
        msgs.append({"role": "user", "content": input})
        completion = self.client.chat.completions.create(
            model=self.model, messages=msgs
        )
        res = completion.choices[0].message
        return res
