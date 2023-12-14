import sys
import file_handling
from tabulate import tabulate

OUTLINE_HEADERS = 34  # qty simbols


def print_header(header: str, answer_option=None):
    """
    Функция выводит заголовок и варианты действий пользователя

    :param header: Заголовок
    :param answer_option: Варианты действий пользователя list
    """

    if answer_option:
        print("-" * OUTLINE_HEADERS, " " * int((OUTLINE_HEADERS - len(header)) / 2) + header, "-" * OUTLINE_HEADERS,
              *answer_option, sep="\n", end="\n\n")
    else:
        print("-" * OUTLINE_HEADERS, " " * int((OUTLINE_HEADERS - len(header)) / 2) + header, "-" * OUTLINE_HEADERS,
              sep="\n")


def request_user_actions(header="", answer_option=None):
    """
    Функция запрашивает действия пользователя

    :param header: Заголовок
    :param answer_option: Варианты действий пользователя list
    :return: Выбранный пользователем вариант
    """
    try:
        if header:
            print_header(header, answer_option)
            action = int(input("--> "))
            if len(answer_option) < action > len(answer_option):
                raise ValueError
        else:
            action = int(input("--> "))
        return action
    except ValueError:
        print("ERROR: Неверный ввод данных")
        return 0


def edit_data_users(user_session, user):
    """
    Функция изменения данных пользователя, админом.

    :param user_session: Данные, вошедшего в систему, пользователя (админа)
    :param user: Данные пользователя, которые будут изменяться
    """

    print_header("Изменение данных пользователя")
    print(tabulate
          ({"Ключ": list(user.keys())[1:],
            "Значение": list(user.values())[1:]}, headers="keys", tablefmt="presto"), end="\n\n")
    while True:
        key = input("Ключ --> ")
        if key not in list(user.keys()):
            print("Введите ключ из предложенного вам варианта")
            continue
        break

    data = file_handling.read_data_from_file()
    new_entry = input("Введите новое значение --> ")

    for us in data:
        if us["email"] == user["email"]:
            us[key] = new_entry
            file_handling.write_data_to_file(data)
            user = us
            print("\nДанные пользователя успешно обновлены\n")
            break

    while True:
        confirmation = input("Желаете еще что-нибудь изменить (д/н)? --> ").lower()
        if confirmation == 'д':
            return edit_data_users(user_session, user)
        elif confirmation == 'н':
            return session(user_session)
        else:
            print("Попробуйте еще раз\n")
            continue


def edit_list_users(user_session: dict):
    """
    Функция, изменяющая database.json, в связи, с выбранным пользователем (админом), действием.

    :param user_session: Данные, вошедшего в систему, пользователя (админа)
    """

    action = request_user_actions("Изменение списка пользователей", ["1. Добавить", "2. Изменить", "3. Удалить"])
    if not action:
        return edit_list_users(user_session)

    data = file_handling.read_data_from_file()
    existing_emails = [user["email"] for user in data]

    if action == 1:
        new_user = registration()
        print(f"{new_user['name']} успешно зарегистрирован")
        return session(user_session)
    else:
        while True:
            email = input("Введите email пользователя: ")
            if email not in existing_emails:
                print("Пользователь с таким адресом электронной почты не существует")
                continue
            break
        for user in data:
            if email == user["email"]:
                if action == 2:
                    edit_data_users(user_session, user)
                elif action == 3:
                    while True:
                        confirmation = input("Вы уверены (д/н)? --> ").lower()
                        if confirmation == 'д':
                            data.pop(data.index(user))
                            file_handling.write_data_to_file(data)
                            print("\nПользователь удален")
                            return session(user_session)
                        elif confirmation == 'н':
                            return session(user_session)
                        else:
                            print("Неверный ввод данных\n")
                            continue


def session(user_session: dict):
    """
    Текущая сессия пользователя.

    :param user_session: Данные, вошедшего в систему, пользователя
    """

    level = user_session["admin"]

    if level:
        action = request_user_actions("Доступные действия администратора",
                                      ["1. Изменение списка пользователей", "2. Выход из аккаунта",
                                       "3. Завершить сессию"])
        if not action:
            return session(user_session)

        match action:
            case 1:
                edit_list_users(user_session)
            case 2:
                main()
            case 3:
                sys.exit(3)


def edit_password():
    """
    Функция изменения пароля, в случае его утери.
    """

    print_header("Смена пароля")

    data = file_handling.read_data_from_file()

    while True:
        email = input("Email: ")
        name = input("Имя пользователя: ")

        for user in data:
            if user["email"] == email and user["name"] == name:
                new_password = input("Введите новый пароль: ")
                user["password"] = new_password
                file_handling.write_data_to_file(data)
                print("\nПароль успешно изменён")
                return main()
        else:
            print("\nНеверный email или имя пользователя")
            main()


def authorization():
    """
    Функция реализации входа пользователя в свой аккаунт.

    Пользователь входит если верно введёт email и пароль, который указывал при регистрации (данный в database.json).
    Если было совершено 8 попыток входа, то система завершает. У пользователя есть возможность восстановить свой
    аккаунт, выбрав соответствующее действие.
    """

    action = request_user_actions("Авторизация", ["1. Войти", "2. Забыл пароль", "3. Назад"])
    if not action:
        return authorization()

    data = file_handling.read_data_from_file()
    attempts = 0

    match action:
        case 1:
            while attempts != 8:
                email = input("Email: ")
                password = input("Пароль: ")

                for user in data:
                    if user["email"] == email and user["password"] == password:
                        print(f"\nДобро пожаловать, {user['name']}")
                        return session(user)
                else:
                    print("Неверный email или пароль\n")
                    attempts += 1
            else:
                print("Слишком много попыток. Попробуйте авторизоваться позже")
                sys.exit(3)
        case 2:
            edit_password()
        case 3:
            main()


def registration():
    """
    Функция добавляет нового пользователя в database.json

    :return: данные добавленного пользователя
    """

    data = file_handling.read_data_from_file()
    existing_emails = [user["email"] for user in data]

    while True:
        email = input("Email: ")
        if email in existing_emails:
            print("Пользователь с таким адресом электронной почты уже существует.")
            continue
        break
    name = input("Имя: ")
    password = input("Пароль: ")

    user = {"admin": 0, "email": email, "name": name, "password": password}
    data.append(user)
    file_handling.write_data_to_file(data)

    return user


def main():
    action = request_user_actions("SHOP", ["1. Войти", "2. Зарегистрироваться"])
    if not action:
        return main()

    match action:
        case 1:
            authorization()
        case 2:
            header = "Регистрация"
            print_header(header)
            user = registration()
            print('Вы успешно зарегистрировались')
            print(f"\nДобро пожаловать, {user['name']}\n")
            session(user)


if __name__ == '__main__':
    main()
