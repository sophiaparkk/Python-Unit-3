import csv
from pprint import pprint

class Melon:
    def __init__(self, melon_id, common_name, price, image_url, color, seedless):
        self.melon_id = melon_id
        self.common_name = str(common_name)
        self.price = float(price)
        self.image_url = image_url
        self.color = color
        self.seedless = seedless

    def __repr__(self): #a method to show information in the terminal
        return f'<Melon: {self.melon_id}, {self.common_name}'
    
    def price_str(self):
        return f'${self.price:.2f}'

melon_dict = {}


with open('melons.csv') as csvfile:
    rows = csv.DictReader(csvfile)

    for row in rows:
        # print(row)
        melon_id = row['melon_id']
        #each melon is a dictionary of key value pairs that are melon attributes
        melon = Melon(
            melon_id,
            row['common_name'],
            float(row['price']),
            row['image_url'],
            row['color'],
            eval(row['seedless'])
        )
        #this is a new dictionary of melons where key value pairs are the ID and the melon object (a dictionary of dictionaries)
        melon_dict[melon_id] = melon
    
# print(melon_dict)


def get_by_id(melon_id):
    return melon_dict[melon_id]

# print(get_by_id('cren'))

def get_all():
    return list(melon_dict.values())

# print(get_all())