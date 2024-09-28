from openai import OpenAI


class Sentiment:
    PROMPT = 'Twoim zadaniem jest okreslenie sentymentu wypowiedzi. Określ ton wypowiedzi (pozytywny, negatywny, neutralny). Dodatkowo określ jakie emocje może wywołać w odbiorcy. Jeśli wypowiedź zawiera mowę nienawiści, określ emocje odbiorcy jako "nienawiść".'

    SAMPLES = [
        ("nienawidzę czarnoskórych", ("negatywny", "nienawiść")),
        (
            "Działania rządu w sprawie COVID-19 uderzają w wolność obywateli.",
            ("negatywny", "gniew"),
        ),
        ("W końcu zaczęto dbać o środowisko", ("pozytywny", "radość")),
        ("nie mam zdania na ten temat.", ("neutralny", "obojętność")),
        (
            "Nie podoba mi się ten pomysł.",
            ("negatywny", "niezadowolenie, rozczarowanie"),
        ),
        ("Jesteśmy zadowoleni z wyników", ("pozytywny", "zadowolenie")),
        ("wszystko jest w porządku", ("neutralny", "spokój, troska")),
        (
            "orlen osiągnął rekordowe zyski w tym roku",
            ("neutralny", "przekaz informacyjny"),
        ),
    ]

    LLM_MODEL = "gpt-4o-mini"

    def __init__(self):
        self.client = OpenAI()

        self.messages = [{"role": "system", "content": Sentiment.PROMPT}]
        for sample in Sentiment.SAMPLES:
            self.messages.append({"role": "user", "content": sample[0]})
            self.messages.append(
                {
                    "role": "assistant",
                    "content": f"Ton wypowiedzi: {sample[1][0]}\nEmocje: {sample[1][1]}",
                }
            )

    def estimate(self, input: str) -> tuple[str, str, bool]:
        self.messages.append({"role": "user", "content": input})

        completion = self.client.chat.completions.create(
            model=Sentiment.LLM_MODEL,
            messages=self.messages,
        )

        res = completion.choices[0].message

        # If refused, set hate speech
        if res.refusal:
            return "negatywny", "niebezpieczne treści", True

        content = res.content

        tone = content.split("\n")[0].split(": ")[1].lower().strip()
        emotions = content.split("\n")[1].split(": ")[1].lower().strip()
        hate = "nienawi" in emotions

        return tone, emotions, hate


sentiment = Sentiment()
for input in [
    "Niepełnosprawni w naszym kraju nie przyczyniają się do rozwoju gospodarczego.",
    "Orlen osiągnął rekordowe zyski w tym roku",
    "Prezydent Duda nie wsparł protestujących przeciwko reformie sądownictwa.",
    "Wiemy, że politycy i urzędnicy unijni bywają czasem trudnym partnerem – przekonywaliśmy się o tym w ostatnich latach wielokrotnie. Interesy unijnej biurokracji oraz niektórych państw członkowskich nieraz bywają sprzeczne z polskimi. W Unii każdego dnia trwa walka, twarda walka o interesy poszczególnych krajów i trzeba o nie skutecznie zabiegać.",
    "Nasza obecność w Unii Europejskiej jest częścią naszej wielkiej wspaniałej historii. Historii Polski, która jest historią wolności.",
    "Nasz głos ma znaczenie. Dlatego każdego dnia musimy zabiegać o polskie sprawy w Unii Europejskiej!",
]:
    print(input)
    print("->", sentiment.estimate(input))
