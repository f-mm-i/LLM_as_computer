import os
from openai import OpenAI
import json 

def load_openai_api_key(file_path="LLM_as_computer/config.txt"):
    with open(file_path, "r") as f:
        for line in f:
            if line.startswith("OPENAI_API_KEY ="):
                return line.split("=", 1)[1].strip().strip("'").strip('"')
    return None

OPENAI_API_KEY = load_openai_api_key()

os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY
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
    def __init__(self, name: str = "RAMAgent", model: str = "gpt-5-nano"):
        super().__init__(name, model)
        self.ram_storage = [9, 3, 4, 5, 6, 0, 10, 25, 678]

    def read(self, need_index: int) -> int:
        client = OpenAI()
        functions = [
                {
                    "name": "ram_read",
                    "description": "Реализация метода READ в RAM",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "value": {
                                "type": "integer",
                                "description": "Числовое значение"
                            }
                        },
                        "required": ["value"]
                    }
                }
            ]

        response = client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": "Ты модуль в ОЗУ компьютера, который отвечает за операцию READ. "
                                    "Ты получаешь хранилище ОЗУ(массив чисел) и числовой индекс. Ты должен вернуть число из хранилища которое соответсвует данному индексу(нумерация в хранилище начинается с единицы)."
                                    "Пример входных данных: (storage: [0, 9, 5, 9, 0, 3], index: 3) -> ожидаемый вывод: 5 "
                                    "Если запрошенный индекс не входит в хранилище, или произошла другая проблема тебе необходимо вернуть значение -1" # потом нужно будет сменить логику ошибки
                    },
                    {
                        "role": "user",
                        "content": f"Хранилище: {self.ram_storage}, Запрошенный индекс: {need_index}"
                    },
                ],
                functions=functions,
                function_call={"name": "ram_read"},
            )
        arguments = response.choices[0].message.function_call.arguments
        read_output = json.loads(arguments)
        return read_output.get('value')


    def write(self, need_index: int) -> str:
        pass


ram1 = RAMAgent()
print(ram1.read(8))