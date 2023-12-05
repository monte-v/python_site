import sys
import file_handling
from tabulate import tabulate


def edit_data_users(user_session, user):
    try:
        print(f"\n{'-' * 30}\n --Изменение данных пользователя--\n")
        print(tabulate
              ({"Ключ": list(user.keys())[1:],
                "Значение": list(user.values())[1:]}, headers="keys", tablefmt="presto"))
        key = input("Ключ --> ")
        if key not in list(user.keys()):
            raise ValueError
    except ValueError:
        print("Введите ключ из предложенного вам варианта")
        return edit_data_users(user_session, user)
    data = file_handling.read_data_from_file()
    new_entry = input("Введите новое значение\n--> ")
    for us in data:
        if us["email"] == user["email"]:
            us[key] = new_entry
            file_handling.write_data_to_file(data)
            user = us
            print("Данные пользователя успешно обновлены\n")
            break

    while True:
        confirmation = input("Желаете еще что-нибудь изменить (д/н)?\n--> ").lower()
        if confirmation != 'д' or confirmation != 'н':
            print("Попробуйте еще раз\n")
            continue
        elif confirmation == 'д':
            edit_data_users(user_session, user)
        break

    return session(user_session)


def edit_list_users(user_session: dict):
    try:
        answer_option = ["1. Добавить\n", "2. Изменить\n", "3. Удалить\n"]
        print(f"\n{'-' * 30}\n --Изменение списка пользователей--\n", *answer_option)
        action = int(input("--> "))
        if len(answer_option) < action > len(answer_option):
            raise ValueError
    except ValueError:
        print("Введите число из предложенного вам варианта")
        return edit_list_users(user_session)
    data = file_handling.read_data_from_file()
    existing_emails = [user["email"] for user in data]

    if action == 1:
        new_user = registration()
        print(data_users for data_users in new_user)
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
                        confirmation = input("Вы уверены (д/н)?\n--> ").lower()
                        if confirmation != 'д' or confirmation != 'н':
                            print("Попробуйте еще раз\n")
                            continue
                        elif confirmation == 'д':
                            data.remove(user)
                            file_handling.write_data_to_file(data)
                        break
            break


def session(user_session: dict):
    print(f"Добро пожаловать, {user_session['name']}")
    level = user_session["admin"]
    if level:
        try:
            answer_option = ["1. Изменение списка пользователей"]
            print(f"\n{'-' * 30}\n --Доступные действия администратора--\n", *answer_option)
            action = int(input("--> "))
            if len(answer_option) < action > len(answer_option):
                raise ValueError
        except ValueError:
            print("Введите число из предложенного вам варианта")
            return session(user_session)

        match action:
            case 1:
                edit_list_users(user_session)


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
                continue
        else:
            print("Пользователя с таким логином не существует")
            main()
            break


def authorization():
    try:
        answer_option = ["1. Войти\n", "2. Забыл пароль\n", "3. назад\n"]
        print(f"\n{'-' * 30}\n --Авторизация--\n", *answer_option)
        action = int(input("--> "))
        if len(answer_option) < action > len(answer_option):
            raise ValueError
    except ValueError:
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
    return user


def main():
    try:
        answer_option = ["1. Авторизоваться\n", "2. Зарегистрироваться\n"]
        print(f"\n{'-' * 30}\nВойдите в систему\n", *answer_option)
        action = int(input("--> "))
        if len(answer_option) < action > len(answer_option):
            raise ValueError
    except ValueError:
        print("Введите число из предложенного вам варианта")
        return main()

    match action:
        case 1:
            authorization()
        case 2:
            user = registration()
            session(user)


if __name__ == '__main__':
    main()
