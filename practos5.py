import os
import multiprocessing
from math import ceil

def encrypt(text, shift):
    encrypted_text = ""
    for char in text:
        if char.isalpha():
            offset = 65 if char.isupper() else 97
            encrypted_text += chr((ord(char) - offset + shift) % 26 + offset)
        else:
            encrypted_text += char
    return encrypted_text

def decrypt(text, shift):
    decrypted_text = ""
    for char in text:
        if char.isalpha():
            offset = 65 if char.isupper() else 97
            decrypted_text += chr((ord(char) - offset - shift) % 26 + offset)
        else:
            decrypted_text += char
    return decrypted_text

def process_chunk(chunk, operation, shift):
    if operation == "encrypt":
        return encrypt(chunk, shift)
    elif operation == "decrypt":
        return decrypt(chunk, shift)

def save_to_file(filename, data):
    print(f"Сохранение данных в файл: {filename}")
    with open(filename, 'w', encoding='utf-8') as file:
        file.write(data)

def process_file(input_file, output_file, operation, num_processes, shift=3):
    if not os.path.exists(input_file):
        print(f"Ошибка: Файл '{input_file}' не найден.")
        return

    try:
        with open(input_file, 'r', encoding='utf-8') as file:
            text = file.read()
    except UnicodeDecodeError:
        print("Ошибка: Не удалось декодировать файл. Возможно, неправильная кодировка.")
        return

    if len(text) == 0:
        print("Ошибка: Входной файл пуст.")
        return

    num_processes = min(num_processes, len(text))

    chunk_size = ceil(len(text) / num_processes)
    chunks = [text[i:i + chunk_size] for i in range(0, len(text), chunk_size)]

    pool = multiprocessing.Pool(processes=num_processes)
    results = []

    for chunk in chunks:
        result = pool.apply_async(process_chunk, args=(chunk, operation, shift))
        results.append(result)

    processed_chunks = []
    for result in results:
        processed_chunk = result.get()
        processed_chunks.append(processed_chunk)

    pool.close()
    pool.join()

    final_text = ''.join(processed_chunks)

    save_process = multiprocessing.Process(target=save_to_file, args=(output_file, final_text))
    save_process.start()
    save_process.join()

def main():
    print("Выберите операцию:")
    print("1. Шифрование")
    print("2. Дешифрование")
    choice = input("Введите номер операции: ")

    input_file = input("Введите путь к входному файлу: ")
    output_file = input("Введите путь к выходному файлу: ")
    shift = int(input("Введите значение сдвига для шифра Цезаря: "))

    max_processes = multiprocessing.cpu_count()
    print(f"Максимальное количество процессов: {max_processes}")
    num_processes = int(input(f"Введите количество процессов (1-{max_processes}): "))
    num_processes = min(num_processes, max_processes)

    if choice == "1":
        process_file(input_file, output_file, "encrypt", num_processes, shift)
        print("Файл успешно зашифрован.")
    elif choice == "2":
        process_file(input_file, output_file, "decrypt", num_processes, shift)
        print("Файл успешно дешифрован.")
    else:
        print("Неверный выбор операции.")

if __name__ == "__main__":
    main()