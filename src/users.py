import re
import os
import base64
import datetime


class User:
    
    def __init__(
            self,
            is_admin,
            surname,
            name='',
            birth_year=2000,
            address='',
            email='',
            phone=''):
        self.is_admin = is_admin
        self.surname = surname
        self.name = name
        self.birth_year = birth_year
        self.address = address
        self.email = email
        self.phone = phone
        self.photo = None
        self.__created = datetime.datetime.utcnow()

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        if not value:
            return
        if not value.isalpha():
            print('A name must contain only alphabetic symbols.')
        self._name = value

    @property
    def birth_year(self):
        return self._birth_year

    @birth_year.setter
    def birth_year(self, value):
        if isinstance(value, int) and value > 0:
            self._birth_year = value
        else:
            self._birth_year = 2000

    @property
    def email(self):
        return self._email

    @email.setter
    def email(self, value):
        if '@' in value:
            self._email = value
        else:
            self._email = value + '@gmail.com'

    @property
    def phone(self):
        return self._phone

    @phone.setter
    def phone(self, value):
        self._phone = ''.join([_char for _char in value if _char.isnumeric()])
    
    @property
    def created(self):
        return self.__created

    def create_recipient(self):
        full_name = ' '.join([_name for _name in [self.name, self.surname] if _name])
        recipient = f'<{full_name}>'
        if self.email:
            recipient += self.email
        return recipient

    def add_user_photo(self, path):
        if not path.endswith('.jpg'):
            raise ValueError('Only .jpg images are supported.')
        with open(path, 'rb') as image:
            self.photo = base64.b64encode(image.read())

    def write_user_photo(self, path):
        image_path = os.path.join(path, 'foto.jpg')
        with open(image_path, 'wb') as image:
            image.write(base64.decodebytes(self.photo))


class Administrator(User):
    pass


class Volunteer(User):
    
    def __init__(
            self,
            is_admin,
            surname,
            name='',
            birth_year=2000,
            address='',
            email='',
            phone=''):
        super().__init__(is_admin, surname, name, birth_year, address, email, phone)
        self.collection_data = {}

    def __natural_sort(self, seq): 
        convert = lambda text: int(text) if text.isdigit() else text.lower()
        alphanum_key = lambda key: [convert(c) for c in re.split('([0-9]+)', key)]
        return sorted(seq, key=alphanum_key)

    def add_collection_data(self, garbage_type, weight, volume, date=None):
        if garbage_type not in {'glass', 'plastic', 'paper'}:
            raise ValueError('Only these garbage types are supported: glass, plastic, paper.')
        if not date:
            date = datetime.date.today()
        if not date in self.collection_data:
            self.collection_data[date] = []
        self.collection_data[date].append({'garbage_type': garbage_type,'weight': weight, 'volume': volume, 'density': weight/volume})

    def print_collection_data(self):
        if not self.collection_data:
            print(f"{self.name} hasn't collected any garbage yet!")
        sorted_data = {key: self.collection_data[key] for key in self.__natural_sort(self.collection_data.keys())}
        for date, records in sorted_data.items():
            line = f"{date} {self.name} has collected:"
            for record in records:
                line += f" {record['weight']}kg of {record['garbage_type']} [volume: {record['volume']}, density: {record['density']}]"
            print(line)

    def garbage_sum(self, garbage_type, metric, date_start, date_end):
        if metric not in {'weight', 'volume'}:
            raise ValueError('The only supported metrics are weight and volume.')
        total = 0
        for date, records in self.collection_data.items():
            if date >= date_start and date <= date_end:
                for record in records:
                    if record['garbage_type'] == garbage_type:
                        total += record[metric]
        return total

    def print_sum_stats(self):
        weight_totals = {'glass': 0, 'paper': 0, 'plastic': 0}
        volume_totals = {'glass': 0, 'paper': 0, 'plastic': 0}
        density_totals = {'glass': 0, 'paper': 0, 'plastic': 0}
        for _date, records in self.collection_data.items():
            for record in records:
                weight_totals[record['garbage_type']] += record['weight']
                volume_totals[record['garbage_type']] += record['volume']
                density_totals[record['garbage_type']] += record['density']
        for garbage_type, weight in weight_totals.items():
            print(f"Total {garbage_type} weight: {weight}")
        print(f"Total garbage weight: {sum(weight_totals.values())}\n")
        for garbage_type, volume in volume_totals.items():
            print(f"Total {garbage_type} volume: {volume}")
        print(f"Total garbage volume: {sum(volume_totals.values())}\n")
        for garbage_type, density in density_totals.items():
            print(f"Total {garbage_type} density: {density}")
        print(f"Total garbage density: {sum(density_totals.values())}\n")
