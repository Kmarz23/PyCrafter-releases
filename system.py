import datetime
import socket
import webbrowser
import requests
import json
import re
import os
import time
from cryptography.fernet import Fernet
from colorama import init, Fore, Style

if not os.path.exists("System"):
    os.mkdir("System")
os.chdir("System")
if not os.path.exists("Gry"):
    os.mkdir("Gry")
if not os.path.exists("Programy"):
    os.mkdir("Programy")

# Inicjalizacja colorama
init(autoreset=True)
current_version = '0.0.1'  # Aktualna wersja Twojej aplikacji

# Reszta kodu (jak wcześniej)

def is_internet_available():
    try:
        # Próbujemy nawiązać połączenie z serwerem Google na porcie 80 (HTTP).
        socket.create_connection(("www.google.com", 80))
        return True
    except OSError:
        pass
    return False

def check_for_update():
    if is_internet_available():
        repo_owner = 'Kmarz23'
        repo_name = 'PyCrafter'
        
        response = requests.get(f'https://api.github.com/repos/{repo_owner}/{repo_name}/releases')

        if response.status_code == 200:
            releases = json.loads(response.text)
            if releases:
                latest_release = releases[0]  # Zakładamy, że najnowszy release znajduje się na początku listy
                latest_version = latest_release.get('tag_name')
                if latest_version:
                    if latest_version > current_version:
                        print(f"Dostępna jest nowa wersja systemu: {latest_version}.")
                        t_n = input("Naciśnij dowolny klawisz aby przejść do strony: ")
                        url = "https://github.com/Kmarz23/Moj_OS/releases"  # Zastąp to adresem URL, na który chcesz przekierować użytkownika
                        webbrowser.open(url)
                    else:
                        print("Masz już najnowszą wersję systemu.")
                else:
                    print("Nie znaleziono informacji o wersji w odpowiedzi z GitHuba.")
            else:
                print("Brak dostępnych wydań w repozytorium.")
        else:
            print("Błąd podczas pobierania danych z GitHuba.")
    else:
        print("Brak dostępu do internetu. Sprawdź swoje połączenie.")

current_version = '1.0.0'  # Aktualna wersja Twojej aplikacji

# Wywołaj funkcję check_for_update() w odpowiednim miejscu w aplikacji
check_for_update()

def print_loading_animation():
    total_steps = 100
    for i in range(total_steps + 1):
        loading_text = f"Ładowanie systemu... {i}%"
        colorized_loading_text = f"{Fore.RED}{loading_text}{Style.RESET_ALL}"
        print(colorized_loading_text, end="\r")
        time.sleep(0.03)
    time.sleep(0.5)
    print(f"{Fore.GREEN}System załadowany!{Style.RESET_ALL}        ")

def set_password():
    password = input("Ustaw hasło: ")
    key = Fernet.generate_key()
    cipher_suite = Fernet(key)
    encrypted_password = cipher_suite.encrypt(password.encode())
    with open("password.txt", "wb") as file:
        file.write(key)
        file.write(b'\n')
        file.write(encrypted_password)

def get_password():
    try:
        with open("password.txt", "rb") as file:
            lines = file.read().splitlines()
            key = lines[0]
            encrypted_password = lines[1]
            cipher_suite = Fernet(key)
            decrypted_password = cipher_suite.decrypt(encrypted_password)
            return decrypted_password.decode()
    except FileNotFoundError:
        return None

def authenticate():
    password = get_password()
    if password is None:
        print("Brak hasła. Ustaw hasło przy pierwszym uruchomieniu.")
        set_password()
    entered_password = input("Podaj hasło: ")
    return entered_password == password

def print_banner():
    os.system("clear")
    print_loading_animation()  # Wywołanie animacji ładowania
    now = datetime.datetime.now()
    print(f"{now.strftime('%Y-%m-%d %H:%M:%S')}    -------------------")
    print("                       |#################|")
    print(f"                       |#################|")
    print(f"                       |#################|")
    print(f"                       |####{Fore.YELLOW}PyCrafter{Style.RESET_ALL}####|")
    print(f"                       |#################|")
    print(f"                       |#################|")
    print("                       |#################|")
    print("                       -------------------")
    print("                           By Kmarz")

current_directory = "System"

def dzienik_zmian():
	print("Wersja: 1.0.0\n")
	print("Wydano: 3.09.2023r.")
	print("Zmiany:\n")
	print("Stworzono system.\n")
	input("Naciśnij enter aby powrucić do menu głównego ")

def list_files():
    files = os.listdir('.')
    for file in files:
        if os.path.isdir(file):
            print(f"{Fore.RED}{file}{Style.RESET_ALL}")  # Katalog w ciemnym czerwonym kolorze
        else:
            print(file)

def create_directory(directory_name):
    try:
        os.mkdir(directory_name)
        print("Katalog", directory_name, "został utworzony.")
    except FileExistsError:
        print("Katalog", directory_name, "już istnieje.")

def delete_file(file_name):
    if file_name == "password.txt":
        print("Nie można usunąć pliku 'password.txt'.")
    else:
        try:
            os.remove(file_name)
            print("Plik", file_name, "został usunięty.")
        except FileNotFoundError:
            print("Plik", file_name, "nie istnieje.")

def change_directory(directory_name):
    global current_directory
    try:
        if directory_name == "..":
            if current_directory == "System":
                print("Nie możesz opuścić katalogu 'System'.")
            else:
                current_directory = os.path.dirname(current_directory)
                os.chdir(directory_name)
                print("Zmieniono bieżący katalog na", current_directory)
        else:
            new_directory = os.path.join(current_directory, directory_name)
            current_directory = new_directory
            os.chdir(directory_name)
            print("Zmieniono bieżący katalog na", current_directory)
    except FileNotFoundError:
        print("Katalog", directory_name, "nie istnieje.")

def create_file(file_name):
    try:
        with open(file_name, 'w') as file:
            print("Plik", file_name, "został utworzony.")
    except FileExistsError:
        print("Plik", file_name, "już istnieje.")

def edit_file(file_name):
    try:
        with open(file_name, 'a') as file:
            while True:
                line = input("Wprowadź tekst (lub wpisz 'exit' aby zakończyć edycję): ")
                if line == 'exit':
                    break
                file.write(line + '\n')
            print("Edycja pliku", file_name, "zakończona.")
    except FileNotFoundError:
        print("Plik", file_name, "nie istnieje.")

def show_menu():
    print("Menu\n")
    print("1. Menedżer plików")
    print("2. Kalkulator")
    print("3. Gry")
    print("4. Programy")
    print("5. Dzienik zmian")
    print("6. Wyjdź\n")

def main():
    while True:
        now = datetime.datetime.now()
        if authenticate():
            print_banner()
            show_menu()
            choice = input("Twój wybór: ")

            if choice == "1":
                file_manager_menu()
            elif choice == "2":
                calculator_menu()
            elif choice == "3":
                games_menu()
            elif choice == "4":
            	programy_menu()
            elif choice == "5":
            	dzienik_zmian()
            elif choice == "6":
                print("Do widzenia!")
                break
            else:
                print("Nieprawidłowy wybór. Wybierz opcję 1, 2, 3, 4 lub 5.")
        else:
            print("Nieprawidłowe hasło. Dostęp zabroniony.")

def programy_menu():
    selected_file = 0
    os.chdir("Programy")
    while True:
        print("\nProgramy")
        files = [file for file in os.listdir('.') if file.endswith(".py")]
        for idx, file in enumerate(files, start=1):
            print(f"{idx}. {file}")

        print(f"{len(files) + 1}. Wróć do głównego menu\n")  # Zmiana: korzystamy z len(files) zamiast idx
        choice = input("Twój wybór: ")

        if choice == str(len(files) + 1):  # Zmiana: porównujemy z len(files) + 1
            os.chdir("..")
            break
        elif choice.isdigit() and 1 <= int(choice) <= len(files):
            selected_file = files[int(choice) - 1]
            os.system(f"python {selected_file}")
        else:
            print("Nieprawidłowy wybór")

def games_menu():
    selected_file = 0
    os.chdir("Gry")
    while True:
        print("\nGry")
        files = [file for file in os.listdir('.') if file.endswith(".py")]
        for idx, file in enumerate(files, start=1):
            print(f"{idx}. {file}")

        print(f"{idx + 1}. Wróć do głównego menu\n")
        choice = input("Twój wybór: ")

        if choice == str(idx + 1):
            os.chdir("..")
            break
        elif choice.isdigit() and 1 <= int(choice) <= len(files):
            selected_file = files[int(choice) - 1]
            os.system(f"python {selected_file}")
        else:
            print("Nieprawidłowy wybór")

def file_manager_menu():
    global current_directory
    while True:
        print("\nMenedżer plików - Aktualna lokalizacja:", current_directory, "\n")
        print("1. Wyświetl pliki w katalogu")
        print("2. Utwórz nowy katalog")
        print("3. Usuń plik")
        print("4. Zmień katalog")
        print("5. Utwórz plik")
        print("6. Edytuj plik")
        print("7. Wróć do głównego menu\n")

        choice = input("Twój wybór: ")

        if choice == "1":
            list_files()
        elif choice == "2":
            directory_name = input("Podaj nazwę nowego katalogu: ")
            create_directory(directory_name)
        elif choice == "3":
            file_name = input("Podaj nazwę pliku do usunięcia: ")
            delete_file(file_name)
        elif choice == "4":
            print("Podaj nazwę katalogu do zmiany")
            directory_name = input("lub napisz .. aby powrucić do poprzedniego: ")
            change_directory(directory_name)
        elif choice == "5":
            file_name = input("Podaj nazwę nowego pliku: ")
            create_file(file_name)
        elif choice == "6":
            file_name = input("Podaj nazwę pliku do edycji: ")
            edit_file(file_name)
        elif choice == "7":
            break
        else:
            print("Nieprawidłowy wybór. Wybierz opcję od 1 do 7.")

def calculator_menu():
    while True:
        print("\nKalkulator\n")
        print("1. Dodawanie")
        print("2. Odejmowanie")
        print("3. Mnożenie")
        print("4. Dzielenie")
        print("5. Wróć do głównego menu\n")

        choice = input("Twój wybór: ")

        if choice in ["1", "2", "3", "4"]:
            num1 = float(input("Podaj pierwszą liczbę: "))
            num2 = float(input("Podaj drugą liczbę: "))
            
            if choice == "1":
                print("Wynik:", num1 + num2)
            elif choice == "2":
                print("Wynik:", num1 - num2)
            elif choice == "3":
                print("Wynik:", num1 * num2)
            elif choice == "4":
                if num2 != 0:
                    print("Wynik:", num1 / num2)
                else:
                    print("Nie można dzielić przez zero!")
        elif choice == "5":
            break
        else:
            print("Nieprawidłowy wybór. Wybierz opcję od 1 do 5.")

if __name__ == "__main__":
    main()
