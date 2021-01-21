import csv, itertools

def get_preview_data(path, limit = 5):
    items = []
    with open(path) as file:
        rows = csv.reader(file, delimiter=',')
        for row in itertools.islice(rows, limit):
            items.append(row)
    return items
