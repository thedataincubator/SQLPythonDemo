import artist_search
from tabulate import tabulate

connect_string = 'postgresql://rich:testpass@localhost:5432/art'

artist = input("Please enter an artist:\n")

loop = True
page = 0

while loop:
    objects = artist_search.artist_objects(connect_string, artist, 5, page)
    bounds = artist_search.artist_count(connect_string, artist, 5, page)
    
    print(tabulate(objects[['title', 'dated']], headers=['title', 'date'], tablefmt='fancy_grid', showindex=False))
    print(f"Showing objects {bounds['low']} to {bounds['high']} out of {bounds['total']}")
    
    print("\nEnter n for next page, p for previous, anything else to exit")
    
    command = input()
    
    if command.lower() == "n":
        if 5*(page + 1) < bounds['total']:
            page += 1
    elif command.lower() == "p":
        if page > 0:
            page -= 1
    else:
        loop = False