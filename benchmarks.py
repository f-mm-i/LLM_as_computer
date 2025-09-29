
import time
import random
from agents import RAMAgent, SSDAgent

class Benchmark:
    def __init__(self, agent_name: str, model: str = "gpt-5-nano"):
        self.agent_name = agent_name
        self.model = model

    def run_benchmark(self):
        raise NotImplementedError("Метод run_benchmark должен быть реализован в дочерних классах")

class RAMAgentBenchmark(Benchmark):
    def __init__(self, agent_name: str = "RAMAgent", model: str = "gpt-5-nano"):
        super().__init__(agent_name, model)
        self.agent = RAMAgent(name=agent_name, model=model)
        # Учитываем, что ram_storage может быть пустым, если это происходит, то длина 0.
        storage_len = len(self.agent.ram_storage) if self.agent.ram_storage else 0
        if storage_len > 0:
            self.test_indices = [i % storage_len for i in range(100)] # Фиксированные индексы для 100 чтений (0-based)
            self.write_test_data = [(i % storage_len, i * 10 % 1000) for i in range(100)] # Фиксированные индексы и значения для 100 записей
        else:
            self.test_indices = []
            self.write_test_data = []

    def run_benchmark(self):
        results = {}

        # Бенчмарк операций чтения
        if not self.test_indices:
            print(f"Хранилище RAMAgent {self.agent_name} пусто, бенчмарк чтения не запущен.")
            results["read_total_time"] = 0
            results["read_successful_reads"] = 0
            results["read_avg_time"] = 0
        else:
            read_total_time = 0
            read_successful_reads = 0
            print(f"Запуск бенчмарка для RAMAgent.read ({self.agent_name})...")
            for index in self.test_indices:
                start_time = time.time()
                result = self.agent.read(index + 1)
                end_time = time.time()
                read_total_time += (end_time - start_time)
                if result != -1:
                    read_successful_reads += 1

            read_avg_time = read_total_time / len(self.test_indices)
            print(f"Бенчмарк RAMAgent.read ({self.agent_name}) завершен.")
            print(f"Всего операций чтения: {len(self.test_indices)}")
            print(f"Успешных операций чтения: {read_successful_reads}")
            print(f"Среднее время чтения: {read_avg_time:.6f} секунд")
            results["read_total_time"] = read_total_time
            results["read_successful_reads"] = read_successful_reads
            results["read_avg_time"] = read_avg_time

        print("\n")

        # Бенчмарк операций записи
        if not self.write_test_data:
            print(f"Хранилище RAMAgent {self.agent_name} пусто, бенчмарк записи не запущен.")
            results["write_total_time"] = 0
            results["write_successful_writes"] = 0
            results["write_avg_time"] = 0
        else:
            write_total_time = 0
            write_successful_writes = 0
            print(f"Запуск бенчмарка для RAMAgent.write ({self.agent_name})...")
            for index, value in self.write_test_data:
                start_time = time.time()
                result = self.agent.write(index + 1, value)
                end_time = time.time()
                write_total_time += (end_time - start_time)
                if result != -1:
                    write_successful_writes += 1

            write_avg_time = write_total_time / len(self.write_test_data)
            print(f"Бенчмарк RAMAgent.write ({self.agent_name}) завершен.")
            print(f"Всего операций записи: {len(self.write_test_data)}")
            print(f"Успешных операций записи: {write_successful_writes}")
            print(f"Среднее время записи: {write_avg_time:.6f} секунд")
            results["write_total_time"] = write_total_time
            results["write_successful_writes"] = write_successful_writes
            results["write_avg_time"] = write_avg_time

        return results

class SSDAgentBenchmark(Benchmark):
    def __init__(self, agent_name: str = "SSDAgent", model: str = "gpt-5-nano"):
        super().__init__(agent_name, model)
        self.agent = SSDAgent(name=agent_name, model=model)
        self.num_operations = 100
        # Фиксированные LBA для 100 операций
        self.test_lbas = [i % self.agent.pages_count for i in range(self.num_operations)]
        # Фиксированные данные для записи для 100 операций
        self.test_data = [f"fixed_data_{i % self.agent.pages_count}" for i in range(self.num_operations)]

    def run_benchmark(self):
        print(f"Запуск бенчмарка для SSDAgent ({self.agent_name})...")

        # Бенчмарк операций чтения
        read_total_time = 0
        read_successful = 0
        for lba in self.test_lbas:
            start_time = time.time()
            result = self.agent.read(lba)
            end_time = time.time()
            read_total_time += (end_time - start_time)
            if result: 
                read_successful += 1
        read_avg_time = read_total_time / self.num_operations
        print(f"SSDAgent.read: {read_successful} успешных из {self.num_operations} операций.")
        print(f"Среднее время чтения SSDAgent: {read_avg_time:.6f} секунд.")

        # Бенчмарк операций записи
        write_total_time = 0
        write_successful = 0
        for i in range(self.num_operations):
            lba = self.test_lbas[i]
            data = self.test_data[i]
            start_time = time.time()
            status = self.agent.write(lba, data)
            end_time = time.time()
            write_total_time += (end_time - start_time)
            if "Error" not in status:
                write_successful += 1
        write_avg_time = write_total_time / self.num_operations
        print(f"SSDAgent.write: {write_successful} успешных из {self.num_operations} операций.")
        print(f"Среднее время записи SSDAgent: {write_avg_time:.6f} секунд.")

        print(f"Бенчмарк SSDAgent ({self.agent_name}) завершен.")
        return {
            "read_total_time": read_total_time,
            "read_successful": read_successful,
            "read_avg_time": read_avg_time,
            "write_total_time": write_total_time,
            "write_successful": write_successful,
            "write_avg_time": write_avg_time,
        }

if __name__ == "__main__":
    print("Запуск бенчмарков...")

    # Бенчмарк RAMAgent
    ram_benchmark = RAMAgentBenchmark()
    ram_benchmark.run_benchmark()

    print("\n" + "="*50 + "\n")

    # Бенчмарк SSDAgent
    ssd_benchmark = SSDAgentBenchmark()
    ssd_benchmark.run_benchmark()
