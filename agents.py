import os
from openai import OpenAI
import json 

def load_openai_api_key(file_path="config.txt"):
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


    def write(self, addres: int, value: int):
        client = OpenAI()
        functions = [
                {
                    "name": "ram_write",
                    "description": "Реализация метода WRITE в RAM",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "storage": {
                                "type": "array",
                                "items": {"type": "integer"},
                                "description": "Массив чисел"
                            }
                        },
                        "required": ["storage"]
                    }
                }
            ]

        response = client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": "Ты модуль в ОЗУ компьютера, который отвечает за операцию WRITE. "
                                    "Ты получаешь на вход хранилище ОЗУ(массив чисел), индекс и значение. Ты должен вставить значение в хранилище по указанному индексу(нумерация в хранилище начинается с единицы)."
                                    "Пример входных данных: (storage: [0, 0, 0, 0, 0, 0], index: 3, value: 25) -> ожидаемый вывод: [0, 0, 25, 0, 0, 0] "
                                    "Если данный индекс не входит в хранилище, или произошла другая проблема тебе необходимо вернуть значение -1" # потом нужно будет сменить логику ошибки
                    },
                    {
                        "role": "user",
                        "content": f"Хранилище: {self.ram_storage}, индекс: {addres}, значение: {value}"
                    },
                ],
                functions=functions,
                function_call={"name": "ram_write"},
            )
        arguments = response.choices[0].message.function_call.arguments
        read_output = json.loads(arguments)
        return read_output.get('storage')
        pass


class SSDAgent(Agent):
    def __init__(self, name: str = "SSDAgent", model: str = "gpt-5-nano", pages=1024, block_size=16, cache_size=64):
        super().__init__(name, model)
        # Эмуляция SSD
        self.pages_count = pages
        self.block_size = block_size
        self.cache_size = cache_size
        self.pages = [None] * pages       # физические страницы
        self.ftl = {}                     # LBA -> физическая страница
        self.cache = {}                   # DRAM-кэш
        self.next_free = 0

    def read(self, lba: int) -> bytes:
        client = OpenAI()
        functions = [
            {
                "name": "ssd_read",
                "description": "Реализация метода READ в SSD",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "data": {
                            "type": "string",
                            "description": "Данные из запрошенного логического блока"
                        }
                    },
                    "required": ["data"]
                }
            }
        ]

        response = client.chat.completions.create(
            model=self.model,
            messages=[
                {
                    "role": "system",
                    "content":
                        "Ты модуль SSD. Ты работаешь с логическими блоками (LBA), кэшем DRAM и FTL. "
                        "При получении LBA ты должен вернуть данные, находящиеся в этом логическом блоке. "
                        "Если LBA находится в кэше, возвращай данные из кэша, иначе используй FTL для поиска физической страницы. "
                        "Если данных нет или произошла ошибка, возвращай пустую строку. "
                        "Пример: (cache: {1: 'abc'}, ftl: {2: 5}, pages: [None, 'data1', 'data2'], LBA: 1) -> 'abc'."
                },
                {
                    "role": "user",
                    "content":
                        f"LBA для чтения: {lba}\n"
                        f"Кэш: {self.cache}\n"
                        f"FTL: {self.ftl}\n"
                        f"Физические страницы: {self.pages}"
                }
            ],
            functions=functions,
            function_call={"name": "ssd_read"}
        )

        arguments = response.choices[0].message.function_call.arguments
        read_output = json.loads(arguments)
        data = read_output.get('data', '')  # возвращаем данные в виде строки
        return data

    def write(self, lba: int, data: str) -> str:
        client = OpenAI()
        functions = [
            {
                "name": "ssd_write",
                "description": "Реализация метода WRITE в SSD",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "status": {
                            "type": "string",
                            "description": "Результат операции записи"
                        }
                    },
                    "required": ["status"]
                }
            }
        ]

        response = client.chat.completions.create(
            model=self.model,
            messages=[
                {
                    "role": "system",
                    "content":
                        "Ты модуль SSD. Ты работаешь с кэшем DRAM и FTL. "
                        "При записи LBA необходимо сохранить данные в кэш, "
                        "затем записать их в свободную физическую страницу. "
                        "Если свободных страниц мало, вызови perform_gc(). "
                        "Возвращай статус операции записи."
                },
                {
                    "role": "user",
                    "content":
                        f"LBA для записи: {lba}\n"
                        f"Данные: {data}\n"
                        f"Кэш: {self.cache}\n"
                        f"FTL: {self.ftl}\n"
                        f"Физические страницы: {self.pages}"
                }
            ],
            functions=functions,
            function_call={"name": "ssd_write"}
        )

        arguments = response.choices[0].message.function_call.arguments
        write_output = json.loads(arguments)
        status = write_output.get('status', '')

        # Эмуляция записи на уровне Python (исполнение LLM-команды)
        if lba < 0 or lba >= self.pages_count:
            return "Error: LBA out of range"

        # Кэшируем данные
        if len(self.cache) >= self.cache_size:
            self.perform_gc()

        self.cache[lba] = data

        # Записываем в свободную физическую страницу
        if self.next_free >= self.pages_count:
            self.perform_gc()

        phys_page = self.next_free
        self.pages[phys_page] = self.cache.pop(lba)
        self.ftl[lba] = phys_page
        self.next_free += 1

        return status or f"LBA {lba} written to page {phys_page}"
'''
ssd1 = SSDAgent()
ssd1.cache = {1: "данные_кэша_LBA1".encode('utf-8'), 5: "данные_кэша_LBA5".encode('utf-8')}
ssd1.ftl = {2: 0, 3: 1} # LBA 2 -> phys_page 0, LBA 3 -> phys_page 1
ssd1.pages[0] = "физические_данные_страница0".encode('utf-8')
ssd1.pages[1] = "физические_данные_страница1".encode('utf-8')
#print(ssd1.write(1, "data1"))
#print(ssd1.read(1))
read_data_1 = ssd1.read(1) # Ожидаемое значение: "данные_кэша_LBA1"
print(f"Чтение SSD LBA 1 (из кэша): {read_data_1}")
read_data_2 = ssd1.read(2) # Ожидаемое значение: "физические_данные_страница0"
print(f"Чтение SSD LBA 2 (из FTL): {read_data_2}")
read_data_3 = ssd1.read(99) # Ожидаемое значение: "" (пустая строка)
print(f"Чтение SSD LBA 99 (не найдено): {read_data_3}")
'''


