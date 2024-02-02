import tkinter as tk
from tkinter import ttk
import time


class SortingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Sorting App")

        self.create_widgets()

    def create_widgets(self):
        # Поле для ввода чисел
        self.label_input = tk.Label(self.root, text="Введите числа через запятую:")
        self.label_input.grid(row=0, column=0, columnspan=2)

        self.entry_numbers = tk.Entry(self.root, width=40)
        self.entry_numbers.grid(row=0, column=2, columnspan=2)

        # Кнопка для вставки из буфера
        self.btn_paste_from_clipboard = tk.Button(
            self.root, text="Вставить из буфера обмена", command=self.paste_from_clipboard
        )
        self.btn_paste_from_clipboard.grid(row=0, column=4, columnspan=2)

        # Выпадающий список сортировок
        self.label_sort_type = tk.Label(self.root, text="Выберите тип сортировки:")
        self.label_sort_type.grid(row=1, column=0, columnspan=2)

        self.sort_type_var = tk.StringVar(value="Пузырьковая")
        self.sort_type_combobox = ttk.Combobox(
            self.root,
            textvariable=self.sort_type_var,
            values=["Пузырьковая", "Быстрая", "Слиянием", "По возрастанию", "По убыванию"],
        )
        self.sort_type_combobox.grid(row=1, column=2, columnspan=2)

        # Кнопка для сортировки
        self.btn_start_sort = tk.Button(self.root, text="Отсортировать", command=self.start_sorting)
        self.btn_start_sort.grid(row=1, column=4, columnspan=2)

        # Метка для времени сортировки
        self.label_time = tk.Label(self.root, text="Время сортировки:")
        self.label_time.grid(row=2, column=0, columnspan=4)

        # Поле вывода
        self.text_result = tk.Text(self.root, height=10, width=40, state=tk.NORMAL)
        self.text_result.grid(row=3, column=0, columnspan=6)

        # Скролл-бар для текстового поля
        self.scrollbar = tk.Scrollbar(self.root, command=self.text_result.yview)
        self.scrollbar.grid(row=3, column=4, sticky="ns")
        self.text_result.config(yscrollcommand=self.scrollbar.set)

    def start_sorting(self):
        input_sequence = self.entry_numbers.get().strip()
        sort_type = self.sort_type_var.get()

        try:
            numbers = [float(num) for num in input_sequence.split(",")]
        except ValueError:
            self.text_result.delete(1.0, tk.END)
            self.text_result.insert(tk.END, "Ошибка: Введите числа через запятую.\n")
            return

        self.text_result.delete(1.0, tk.END)
        self.text_result.insert(tk.END, "Отсортированная последовательность:")

        start_time = time.time()

        if sort_type in ["Пузырьковая", "Быстрая", "Слиянием"]:
            sorted_sequence = self.sort_numbers(numbers, sort_type)
        else:
            sorted_sequence = self.sort_numbers_v2(numbers, sort_type)

        end_time = time.time()

        for num in sorted_sequence:
            self.text_result.insert(tk.END, f" {num},")

        elapsed_time = end_time - start_time
        self.label_time.config(text=f"Время сортировки: {elapsed_time:.6f} секунд")


    def sort_numbers(self, numbers, sort_type):
        ascending = sort_type == "По возрастанию"

        if sort_type == "Пузырьковая":
            return self.bubble_sort(numbers, ascending)
        elif sort_type == "Быстрая":
            return self.quick_sort(numbers, ascending)
        elif sort_type == "Слиянием":
            return self.merge_sort(numbers, ascending)

    def sort_numbers_v2(self, numbers, sort_type):
        ascending = sort_type == "По возрастанию"
        return sorted(numbers, reverse=not ascending)

    @staticmethod
    def bubble_sort(numbers, ascending):
        n = len(numbers)
        for i in range(n - 1):
            for j in range(0, n - i - 1):
                if ascending:
                    if numbers[j] > numbers[j + 1]:
                        numbers[j], numbers[j + 1] = numbers[j + 1], numbers[j]
                else:
                    if numbers[j] < numbers[j + 1]:
                        numbers[j], numbers[j + 1] = numbers[j + 1], numbers[j]
        return numbers

    @staticmethod
    def quick_sort(numbers, ascending):
        if len(numbers) <= 1:
            return numbers
        pivot = numbers[len(numbers) // 2]
        left = [x for x in numbers if x < pivot]
        middle = [x for x in numbers if x == pivot]
        right = [x for x in numbers if x > pivot]
        if ascending:
            return SortingApp.quick_sort(left, ascending) + middle + SortingApp.quick_sort(right, ascending)
        else:
            return SortingApp.quick_sort(right, ascending) + middle + SortingApp.quick_sort(left, ascending)

    @staticmethod
    def merge_sort(numbers, ascending):
        if len(numbers) > 1:
            mid = len(numbers) // 2
            left_half = numbers[:mid]
            right_half = numbers[mid:]

            SortingApp.merge_sort(left_half, ascending)
            SortingApp.merge_sort(right_half, ascending)

            i, j, k = 0, 0, 0

            while i < len(left_half) and j < len(right_half):
                if ascending:
                    if left_half[i] < right_half[j]:
                        numbers[k] = left_half[i]
                        i += 1
                    else:
                        numbers[k] = right_half[j]
                        j += 1
                else:
                    if left_half[i] > right_half[j]:
                        numbers[k] = left_half[i]
                        i += 1
                    else:
                        numbers[k] = right_half[j]
                        j += 1
                k += 1

            while i < len(left_half):
                numbers[k] = left_half[i]
                i += 1
                k += 1

            while j < len(right_half):
                numbers[k] = right_half[j]
                j += 1
                k += 1

        return numbers

    def paste_from_clipboard(self):
        clipboard_content = self.root.clipboard_get()
        self.entry_numbers.delete(0, tk.END)
        self.entry_numbers.insert(tk.END, clipboard_content)


if __name__ == "__main__":
    root = tk.Tk()
    app = SortingApp(root)
    root.mainloop()