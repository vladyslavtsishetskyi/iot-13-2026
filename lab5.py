from datetime import date, datetime
from enum import Enum


class MovieType(Enum):
    ACTION = "Бойовик"
    COMEDY = "Комедія"
    DRAMA = "Драма"
    FANTASY = "Фентезі"
    HORROR = "Жахи"
    THRILLER = "Трилер"


class Movie:
    def __init__(self, id, title, ranking, release_date, character_number, ticket_price, comment, type):
        self._id = id
        self._title = title
        self._ranking = ranking
        self.set_release_date(release_date)
        self.set_character_number(character_number)
        self.set_ticket_price(ticket_price)
        self._comment = comment
        self._type = type

    def __del__(self):
        print(f"Деструктор: фільм «{self._title}» видалено")

    def get_id(self):
        return self._id

    def get_title(self):
        return self._title

    def set_title(self, title):
        self._title = title

    def get_ranking(self):
        return self._ranking

    def set_ranking(self, ranking):
        self._ranking = ranking

    def get_release_date(self):
        return self._release_date

    def set_release_date(self, release_date):
        if not isinstance(release_date, date) or isinstance(release_date, datetime):
            raise TypeError("Дата виходу має бути об'єктом date")
        self._release_date = release_date

    def get_character_number(self):
        return self._character_number

    def set_character_number(self, character_number):
        if character_number < 0:
            raise ValueError("Кількість персонажів не може бути від'ємною")
        self._character_number = character_number

    def get_ticket_price(self):
        return self._ticket_price

    def set_ticket_price(self, ticket_price):
        if ticket_price < 0:
            raise ValueError("Ціна квитка не може бути від'ємною")
        self._ticket_price = ticket_price

    def get_comment(self):
        return self._comment

    def set_comment(self, comment):
        self._comment = comment

    def get_type(self):
        return self._type

    def set_type(self, type):
        self._type = type

    def display(self):
        print(f"[{self._id}] {self._title} | жанр: {self._type.value} | "
              f"рейтинг: {self._ranking} | дата виходу: {self._release_date} | "
              f"персонажів: {self._character_number} | "
              f"ціна квитка: {self._ticket_price} грн | коментар: {self._comment}")


class Cinema:
    def __init__(self, name, location):
        self._name = name
        self._location = location
        self._movies = []     
        self._tickets_sold = {}

    def __del__(self):
        print(f"Деструктор: кінотеатр «{self._name}» видалено")

    def get_name(self):
        return self._name

    def set_name(self, name):
        self._name = name

    def get_location(self):
        return self._location

    def set_location(self, location):
        self._location = location

    def get_movies(self):
        return self._movies

    def add_movie(self, movie):
        self._movies.append(movie)

    def remove_movie(self, movie_id):
        if not any(movie.get_id() == movie_id for movie in self._movies):
            raise ValueError(f"Фільм з ID {movie_id} не знайдено")
        self._movies = [m for m in self._movies if m.get_id() != movie_id]

    def sell_tickets(self, movie, day, count):
        if movie not in self._movies:
            raise ValueError("Фільм не належить цьому кінотеатру")
        if not isinstance(day, date) or isinstance(day, datetime):
            raise TypeError("Дата продажу має бути об'єктом date")
        if not isinstance(count, int) or isinstance(count, bool):
            raise TypeError("Кількість квитків має бути цілим числом")
        if count < 0:
            raise ValueError("Кількість квитків не може бути від'ємною")
        if movie.get_release_date() > day:
            raise ValueError("Не можна продавати квитки до дати виходу фільму")

        key = (movie.get_id(), day)
        self._tickets_sold[key] = self._tickets_sold.get(key, 0) + count

    def calculate_profit(self, movie, day):
        sold = self._tickets_sold.get((movie.get_id(), day), 0)
        return sold * movie.get_ticket_price()

    def select_movie(self, genre=None, max_price=None, min_ranking=None):
        suitable = [
            m for m in self._movies
            if (genre is None or m.get_type() == genre)
            and (max_price is None or m.get_ticket_price() <= max_price)
            and (min_ranking is None or m.get_ranking() >= min_ranking)
        ]
        if not suitable:
            return None
        return max(suitable, key=lambda m: m.get_ranking())

    def sort_by_release_date(self, reverse=False):
        self._movies.sort(key=lambda m: m.get_release_date(), reverse=reverse)

    def display(self):
        print(f"\nКінотеатр «{self._name}», адреса: {self._location}")
        print("Фільми у прокаті:")
        for m in self._movies:
            m.display()


def main():
    m1 = Movie(1, "Месники", 8.4, date(2012, 4, 25), 12, 150,
               "Супергеройський блокбастер", MovieType.ACTION)
    m2 = Movie(2, "Маска", 7.0, date(1994, 7, 29), 8, 100,
               "Класична комедія", MovieType.COMEDY)
    m3 = Movie(3, "Втеча з Шоушенка", 9.3, date(1994, 9, 23), 15, 120,
               "Драма про надію", MovieType.DRAMA)
    m4 = Movie(4, "Володар перснів", 8.9, date(2001, 12, 19), 20, 180,
               "Епічне фентезі", MovieType.FANTASY)

    cinema = Cinema("Multiplex", "м. Київ, вул. Хрещатик, 1")
    for m in (m1, m2, m3, m4):
        cinema.add_movie(m)

    cinema.display()

    print("\n--- Сортування за датою виходу ---")
    cinema.sort_by_release_date()
    cinema.display()

    print("\n--- Прибуток за день ---")
    day = date(2025, 5, 10)
    cinema.sell_tickets(m1, day, 50)
    cinema.sell_tickets(m4, day, 30)
    for m in (m1, m4):
        print(f"«{m.get_title()}»: {cinema.calculate_profit(m, day)} грн")

    print("\n--- Вибір фільму (жанр FANTASY, ціна до 200 грн) ---")
    chosen = cinema.select_movie(genre=MovieType.FANTASY, max_price=200)
    if chosen:
        chosen.display()
    else:
        print("Фільм не знайдено")

    print("\n--- Вибір фільму (рейтинг від 9, ціна до 130 грн) ---")
    chosen = cinema.select_movie(max_price=130, min_ranking=9)
    if chosen:
        chosen.display()
    else:
        print("Фільм не знайдено")

    cinema = Cinema("Multiplex", "м. Київ, вул. Хрещатик, 1")

    movies = [
        Movie(1, "Месники", 8.4, date(2012, 4, 25),
              12, 150, "Супергеройський блокбастер", MovieType.ACTION),
        Movie(2, "Маска", 7.0, date(1994, 7, 29),
              8, 100, "Класична комедія", MovieType.COMEDY),
        Movie(3, "Втеча з Шоушенка", 9.3, date(1994, 9, 23),
              15, 120, "Драма про надію", MovieType.DRAMA),
        Movie(4, "Володар перснів", 8.9, date(2001, 12, 19),
              20, 180, "Епічне фентезі", MovieType.FANTASY),
    ]
    for movie in movies:
        cinema.add_movie(movie)

    print("Назва і коментар для кожного фільму:")
    for movie in movies:
        print(f"{movie.get_title()}: {movie.get_comment()}")
    print()


if __name__ == "__main__":
    main()
