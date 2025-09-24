
# пример функции openai
"""
client = OpenAI()
            functions = [
                {
                    "name": "keyphrase_extractor",
                    "description": "Вернуть ключевые слова из текста",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "keyphrases": {
                                "type": "array",
                                "items": {"type": "string"},
                                "description": "Ключевые слова"
                            }
                        },
                        "required": ["keyphrases"]
                    }
                }
            ]

            response = client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": "Извлеки краткие содержательные ключевые фразы из научной аннотации."
                                    f"Верни не более {top_k} фраз на русском языке, без нумерации."
                                    "Ключевая фраза модет содержать от 1 до 3 слов без учёта союзов и предлогов"
                                    "Так как это научные аннотации, то фразы содержащие слова: 'статья', 'автор','сущность', 'рассматривается' и их производные, а так же близкие к ним по смыслу слова и выражения не являются ключевыми фразами"
                    },
                    {
                        "role": "user",
                        "content": 'Пример входных и выходных данных. Входные данные: "Вводятся в научный оборот результаты палеокарпологического анализа керамики поселения черкаскульской культуры бронзового века Ольховка, расположенного в долине Исети. Обнаружение на черепках отпечатков семян пшеницы и ячменя практически первое прямое свидетельство знакомства черкаскульского населения Приисетья с земледелием, хотя вопрос о его роли в хозяйстве указанной группировки остается открытым.". Выходные данные: "черкаскульское население, керамика, палеокарпологический анализ".'
                                    'Ещё один пример входных и выходных данных. Входные данные: "Проведен анализ костюмных комплексов могильников Киняминских I, II (XIII первая половина XIV в.), реконструированы накосные украшения из женских погребений.". Выходные данные: "киняминский могильник, накосные украшения, костюмный комплекс".'
                                    f"Аннотация для извлечения ключевых слов: {query}"
                    },
                ],
                functions=functions,
                function_call={"name": "keyphrase_extractor"},
            )
            arguments = response.choices[0].message.function_call.arguments
            res = json.loads(arguments)
            return res.get('keyphrases')
"""




class Agent:
    def __init__(self, name: str, model: str):
        self.name = name
        self.model = model

    def run(self, *args, **kwargs):
        raise NotImplementedError("Метод run должен быть реализован в дочерних классах")


class SimpleAgent(Agent):
    def __init__(self, name: str = "SimpleAgent"):
        super().__init__(name, model)

    def run(self, input_text: str) -> str:
        return input_text


class RAMAgent(Agent):
    def __init__(self, name: str = "RAMAgent", model: str = "default_model"):
        super().__init__(name, model)

    def run(self, input_text: str) -> str:
        if input_text == 'READ':
            data_bus.value = self.memory[addr]
        elif input_text == 'WRITE'
        return