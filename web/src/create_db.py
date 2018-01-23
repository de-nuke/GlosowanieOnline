# create_db.py


from app import db
from models import  User, Candidate
import random, string

USERS_NUM = 10
CANDIDATES_NUM = 10

first_names_m = ['Jan', 'Andrzej', 'Piotr', 'Krzysztof', 'Stanisław', 'Tomasz', 'Paweł', 'Józef', 'Marcin', 'Marek',
               'Michał', 'Grzegorz', 'Jerzy', 'Tadeusz', 'Adam', 'Łukasz', 'Zbigniew', 'Ryszard', 'Dariusz', 'Henryk',
               'Mariusz', 'Kazimierz', 'Wojciech', 'Robert', 'Mateusz', 'Marian', 'Rafał', 'Jacek', 'Janusz',
               'Mirosław', 'Maciej', 'Sławomir', 'Jarosław', 'Kamil', 'Wiesław', 'Roman', 'Władysław', 'Jakub',
               'Artur', 'Zdzisław', 'Edward', 'Mieczysław', 'Damian', 'Dawid', 'Przemysław', 'Sebastian', 'Czesław',
               'Leszek', 'Daniel', 'Waldemar']

first_names_f = ['Anna', 'Maria', 'Katarzyna', 'Małgorzata', 'Agnieszka', 'Krystyna', 'Barbara', 'Ewa', 'Elżbieta',
                 'Zofia', 'Janina', 'Teresa', 'Joanna', 'Magdalena', 'Monika', 'Jadwiga', 'Danuta', 'Irena', 'Halina',
                 'Helena', 'Beata', 'Aleksandra', 'Marta', 'Dorota', 'Marianna', 'Grażyna', 'Jolanta', 'Stanisława',
                 'Iwona', 'Karolina', 'Bożena', 'Urszula', 'Justyna', 'Renata', 'Alicja', 'Paulina', 'Sylwia',
                 'Natalia', 'Wanda', 'Agata', 'Aneta', 'Izabela', 'Ewelina', 'Marzena', 'Wiesława', 'Genowefa',
                 'Patrycja', 'Kazimiera', 'Edyta', 'Stefania']

last_names = ['Nowak', 'Wiśniewski', 'Lewandowski', 'Kamiński', 'Zieliński', 'Woźniak', 'Jankowski', 'Kwiatkowski',
              'Mazur', 'Piotrowski', 'Nowakowski', 'Michalski', 'Adamczyk', 'Zając', 'Jabłoński', 'Majewski',
              'Jaworski', 'Malinowski', 'Witkowski', 'Stępień', 'Rutkowski', 'Sikora', 'Baran', 'Szewczyk', 'Pietrzak',
              'Wróblewski', 'Jakubowski', 'Zawadzki', 'Bąk', 'Włodarczyk', 'Czarnecki', 'Sokołowski', 'Kubiak',
              'Szczepański', 'Wilk', 'Lis', 'Wysocki', 'Kaźmierczak', 'Sobczak', 'Andrzejewski', 'Głowacki',
              'Kołodziej', 'Krajewski', 'Szymczak', 'Baranowski', 'Brzeziński', 'Ziółkowski']

parties = ['PO', 'PSL', 'PIS', 'SLD', 'KORWIN', 'NOWOCZESNA', 'KUKIZ15', 'RAZEM', 'KNP']

descriptions = [
    'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nunc ullamcorper fringilla turpis, eu iaculis tortor dignissim vel. In imperdiet vulputate ex, at luctus mauris sollicitudin faucibus.',
    'Nam lorem mi, volutpat nec elit ac, viverra tincidunt ex. Donec sit amet dignissim justo. Donec lorem urna, suscipit in convallis vel, euismod vitae elit. Ut luctus iaculis neque at sagittis. Nam fermentum sed urna sed convallis. Pellentesque habitant morbi tristique senectus et netus et malesuada fames ac turpis egestas.',
    'Pellentesque habitant morbi tristique senectus et netus et malesuada fames ac turpis egestas. Proin suscipit velit ut tortor imperdiet auctor. Lorem ipsum dolor sit amet, consectetur adipiscing elit.',
    'uspendisse facilisis varius massa id finibus. Suspendisse aliquet tempor arcu. Aliquam interdum tristique vulputate. Integer euismod lectus erat, a imperdiet quam facilisis quis.',
]


db.create_all()

for i in range(int(USERS_NUM/2)):
    db.session.add(User(
        first_name=random.choice(first_names_m),
        last_name=random.choice(last_names),
        father_name=random.choice(first_names_m),
        mother_name=random.choice(first_names_f),
        id_series_number=''.join(random.choice(string.ascii_uppercase) for _ in range(3)) + ''.join(random.choice(string.digits) for _ in range(6)),
        pesel=''.join(random.choice(string.digits) for _ in range(10)),
    ))
    db.session.add(User(
        first_name=random.choice(first_names_f),
        last_name=random.choice(last_names),
        father_name=random.choice(first_names_m),
        mother_name=random.choice(first_names_f),
        id_series_number=''.join(random.choice(string.ascii_uppercase) for _ in range(3)) + ''.join(
            random.choice(string.digits) for _ in range(6)),
        pesel=''.join(random.choice(string.digits) for _ in range(10)),
    ))

db.session.add(User(
    first_name='test',
    last_name='test',
    father_name='test',
    mother_name='test',
    id_series_number='test',
    pesel='test'
))    

for i in range(int(CANDIDATES_NUM/2)):
    db.session.add(Candidate(
        first_name=random.choice(first_names_m),
        last_name=random.choice(last_names),
        age=random.randrange(18, 60),
        party=random.choice(parties),
        description=random.choice(descriptions)
    ))
    db.session.add(Candidate(
        first_name=random.choice(first_names_f),
        last_name=random.choice(last_names),
        age=random.randrange(18, 60),
        party=random.choice(parties),
        description=random.choice(descriptions)
    ))
db.session.commit()
