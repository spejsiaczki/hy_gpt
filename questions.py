from openai import OpenAI


class Questions:
    PROMPT = "Twoim zadaniem jest wysłuchanie wypowiedzi i zadaine do niej 10 pytań."

    SAMPLES = [
        # (
        #     "orlen osiągnął rekordowe zyski w tym roku",
        #     ("neutralny", "przekaz informacyjny"),
        # ),
    ]

    LLM_MODEL = "gpt-4o-mini"

    def __init__(self):
        self.client = OpenAI()

        self.messages = [{"role": "system", "content": Questions.PROMPT}]
        for sample in Questions.SAMPLES:
            self.messages.append({"role": "user", "content": sample[0]})
            self.messages.append({"role": "assistant", "content": sample[1]})

    def estimate(self, input: str) -> list[str]:
        self.messages.append({"role": "user", "content": input})

        completion = self.client.chat.completions.create(
            model=Questions.LLM_MODEL,
            messages=self.messages,
        )

        res = completion.choices[0].message

        if res.refusal:
            return ""

        # keypoints = res.content.split("\n")
        return res.content



questions = Questions()
for input in [
    "Szanowni Państwo, Drodzy Rodacy! Przed Polską i przed Unią Europejską wiele wyzwań dotyczących bezpieczeństwa i gospodarki. Od tego, jak na nie odpowiemy, zależy nasza przyszłość. Będąc w Unii, możemy wpływać na jej kształt, nadawać kluczowe kierunki. Nasz głos ma znaczenie. Dlatego każdego dnia musimy zabiegać o polskie sprawy w Unii Europejskiej! Nasz wielki rodak – papież święty Jan Paweł II mówił do nas: „Europa potrzebuje Polski, a Polska potrzebuje Europy”. Te słowa są ciągle aktualne. Dlatego musimy aktywnie uczestniczyć w kształtowaniu Wspólnoty, zgodnie z wartościami wyznawanymi przez nas od ponad tysiąca lat. Od momentu, kiedy dołączyliśmy do rodziny chrześcijańskich narodów Europy. Dzisiaj jesteśmy świadkami wielkiego sporu o przyszły kształt Unii Europejskiej. Pojawiają się niepokojące tendencje do federalizacji, mówi się o zmianach traktatów, które ograniczą suwerenność państw członkowskich. Nasza obecność w Unii Europejskiej to polska racja stanu, ale opowiadamy się za Europą wolnych narodów! Europą Ojczyzn! Wiemy, że politycy i urzędnicy unijni bywają czasem trudnym partnerem – przekonywaliśmy się o tym w ostatnich latach wielokrotnie. Interesy unijnej biurokracji oraz niektórych państw członkowskich nieraz bywają sprzeczne z polskimi. W Unii każdego dnia trwa walka, twarda walka o interesy poszczególnych krajów i trzeba o nie skutecznie zabiegać. Dlatego tak ważne będą wybory do Parlamentu Europejskiego, które odbędą się 9 czerwca. Od tego, jakich reprezentantów wybierzemy, będzie zależał kierunek, w którym będzie podążała Unia, oraz jak polskie sprawy w Unii będą prowadzone. Zachęcam Państwa do udziału w tych wyborach.",
    "W budżecie na 2025 rok przeznaczymy ponad 221,7 mld zł na ochronę, rekordowy wzrost nakładów na ochronę zdrowia zgodnie z ustawą o blisko 31,7 mld zł, to jest to 6,1%. 0,5 mld zł na realizację programu in vitro, 8,4 mld zł na realizację świadczeń 'Aktywny rodzic', 62,8 mld zł na program 'Rodzina 800+'.",
    "Szanowni Państwo, Drodzy Rodacy! Przed Polską i przed Unią Europejską wiele wyzwań dotyczących bezpieczeństwa i gospodarki. Od tego, jak na nie odpowiemy, zależy nasza przyszłość. Będąc w Unii, możemy wpływać na jej kształt, nadawać kluczowe kierunki. Nasz głos ma znaczenie. 0,5 mld zł na realizację programu in vitro, 8,4 mld zł na realizację świadczeń 'Aktywny rodzic', 62,8 mld zł na program 'Rodzina 800+'."
]:
    print(input)
    print("->", questions.estimate(input))
