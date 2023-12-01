import sys
import file_handling

dict_users = {
    "user1": [0, "pass1", "1@example.com"],
    "user2": [0, "pass2", "2@example.com"],
    "user3": [0, "pass3", "3@example.com"],
    "user4": [0, "pass4", "4@example.com"],
    "user5": [0, "pass5", "5@example.com"],
    "admin1": [1, "admin1", "a1@example.com"],
    "admin2": [1, "admin2", "a2@example.com"],
    "admin3": [1, "admin3", "a3@example.com"],
}


class Error(Exception):
    pass


class AnswerOptionError(Error):
    pass


def edit_data_users(user, login):
    try:
        answer_option = 3
        action = int(input(f"\n{'-' * 30}\n --Изменение данных пользователя--\n1. Логин\n2. Пароль\n3. Email\n--> "))
        if answer_option < action > answer_option:
            raise AnswerOptionError
    except (ValueError, AnswerOptionError):
        print("Введите число из предложенного вам варианта")
        return edit_data_users(user, login)

    match action:
        case 1:
            while True:
                new_login = input("Введите новый логин: ")
                if new_login in dict_users.keys():
                    print("Пользователь с таким логином уже существует")
                    continue
                dict_users[new_login] = dict_users.pop(login)
                break
        case 2:
            new_password = input("Новый пароль: ")
            dict_users[login][1] = new_password
        case 3:
            new_email = input("Новый Email: ")
            dict_users[login][2] = new_email

    return session(user)


def edit_dict_users(user: dict):
    try:
        answer_option = 3
        action = int(
            input(f"\n{'-' * 30}\n --Изменение списка пользователей--\n1. Добавить\n2. Изменить\n3. Удалить\n--> "))
        if answer_option < action > answer_option:
            raise AnswerOptionError
    except (ValueError, AnswerOptionError):
        print("Введите число из предложенного вам варианта")
        return edit_dict_users(user)

    while True:
        login = input("Введите логин пользователя: ")
        if login not in dict_users.keys():
            print("Пользователь с таким логином не существует")
            continue

        if action == 2:
            edit_data_users(user, login)
            break
        elif action == 3:
            del dict_users[login]
            break

    if action == 1:
        while True:
            login = input("Логин: ")
            if login in dict_users.keys():
                print("Пользователь с таким логином уже существует")
                continue

            password = input("Пароль: ")
            email = input("Email: ")

            dict_users[login] = [0, password, email]
            break

    return session(user)


def session(user: dict):
    print(f"Добро пожаловать, ", *user.keys())
    level = user[list(user.keys())[0]][0]
    if level:
        try:
            answer_option = 1
            action = int(
                input(f"\n{'-' * 30}\n --Доступные действия администратора--\n1. Изменение списка пользователей\n--> "))
            if action < answer_option < action:
                raise AnswerOptionError
        except (ValueError, AnswerOptionError):
            print("Введите число из предложенного вам варианта")
            return session(user)

        match action:
            case 1:
                edit_dict_users(user)


def edit_password():
    print(f"\n{'-' * 10}\n --Смена пароля-- ")
    data = file_handling.read_data_from_file()
    while True:
        email = input("Email: ")
        name = input("Имя: ")

        for user in data:
            if user["email"] == email and user["name"] == name:
                new_password = input("Введите новый пароль: ")
                user["password"] = new_password
                print("Пароль успешно изменён")
                main()
            else:
                print("Неверный email или имя пользователя. Введите email и имя, которые указывали при регистрации")
                edit_password()
        else:
            print("Пользователя с таким логином не существует")
            main()
            break


def authorization():
    try:
        action = int(input(f"\n{'-' * 30}\n --Авторизация--\n1. Войти\n2. Забыл пароль\n3. назад\n--> "))
    except (ValueError, AnswerOptionError):
        print("Введите число из предложенного вам варианта")
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
                        session(user)
                else:
                    print("Неверный логин или пароль")
                    attempts += 1
            else:
                print("Слишком много попыток. Попробуйте авторизоваться позже")
                sys.exit(3)
        case 2:
            edit_password()
        case 3:
            main()


def registration():
    print(f"\n{'-' * 30}\n --Регистрация--\n")
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
    print('Вы успешно зарегистрировались')
    return session(user)


def main():
    try:
        action = int(input(f"\n{'-' * 30}\nВойдите в систему\n1. Авторизоваться\n2. Зарегистрироваться\n--> "))
    except (ValueError, AnswerOptionError):
        print("Введите число из предложенного вам варианта")
        return main()

    match action:
        case 1:
            authorization()
        case 2:
            registration()


if __name__ == '__main__':
    main()
