from datetime import datetime, timedelta
from directions_and_durations import directions
from db_and_forecast import read_and_fill, sort_landmarks

CATEGORIES_DB_NAMES = {
    '1': 'waterfalls',
    '2': 'lakes',
    '3': 'trails',
    '4': 'peaks'
}

CATEGORIES = {
    '1': 'водопади',
    '2': 'езера',
    '3': 'екопътеки',
    '4': 'върхове'
}


def enter_date():
    """
    Ask the user to enter a date and return how many days are there
    between the entered date and the current one. If it is more than 16 or
    the entered date has passed, the user is asked to enter again.
    """
    isValid = False
    while not isValid:
        user_date = input(
            "Моля, въведете дата от следващите 16 дни(дд/мм/гг): ")
        try:
            date = datetime.strptime(user_date, "%d/%m/%y")
            current_day = datetime.now()
            delta = date - current_day
            if delta.days >= 0 and delta.days <= 16:
                isValid = True
        except:
            print("Невалиден формат на датата или твърде далечна.")

    return delta.days


def enter_address():
    """
    Asks the user to enter an address and returns a string with it.
    """
    address = None
    current_or_not = '0'
    while current_or_not != '1' and current_or_not != '2':
        print('''Изчисленията да са спрямо:
                1 - сегашната ми позиция
                2 - избран от мен адрес''')
        current_or_not = input()

        if current_or_not == '2':
            address = input("Моля, въведете адрес: ")
            address = address.replace(" ", "+")

    return address

if __name__ == "__main__":
    while True:
        print('''Моля, въведете цифра от 1 до 4:
        1: Водопади
        2: Езера
        3: Екопътеки
        4: Върхове''')

        while True:
            choice = input()
            if choice == '1' or choice == '2' or\
                    choice == '3' or choice == '4':
                print("Вие избрахте: {}".format(CATEGORIES[choice]))
                break
            else:
                print("Невалиден избор. Моля, въведете цифра между 1 и 4.")
                continue

        date = enter_date()

        address = enter_address()

        landmarks = read_and_fill(
            CATEGORIES_DB_NAMES[choice], address, date)

        print_flag = True

        if len(landmarks) != 0:
            landmarks_sorted = sort_landmarks(landmarks)
            for landmark in landmarks_sorted:
                print(("{} - {} градуса - {} % облачност - {} "
                       "време за път").format(
                    landmark.get_name(),
                    str(landmark.get_average_temp()),
                    str(landmark.get_cloud_percentage()),
                    str(timedelta(
                        seconds=landmark.get_travel_duration()))))

                print("Искате ли инструкции за пътуването? (1 - Да, 2 - Не)")
                instructions = '0'
                while instructions != '1' and instructions != '2':
                    instructions = input()
                    if instructions != '1' and instructions != '2':
                        print("Невалиден избор. Моля, въведете 1 или 2.")

                if instructions == '1':
                    directions(
                        landmark.get_coordinates()[0],
                        landmark.get_coordinates()[1],
                        address)

                print("Искате ли друго предложение? (1 - Да, 2 - Не)")
                is_it_okay = '0'
                while is_it_okay != '1' and is_it_okay != '2':
                    is_it_okay = input()
                    if is_it_okay != '1' and is_it_okay != '2':
                        print("Невалиден избор. Моля, въведете 1 или 2.")
                if is_it_okay == '1':
                    continue
                elif is_it_okay == '2':
                    print_flag = False
                    break
            if print_flag:
                print(
                    "Няма други места с хубаво време от избраната категория.")

        else:
            print("Няма места с хубаво време от избраната категория :(")

        print("Желаете ли да видите друга категория? (1 - Да, 2 - Не)")
        another_category = '0'
        while another_category != '1' and another_category != '2':
            another_category = input()
            if another_category != '1' and another_category != '2':
                print("Невалиден избор. Моля, въведете 1 или 2.")
        if another_category == '1':
            continue
        else:
            break
