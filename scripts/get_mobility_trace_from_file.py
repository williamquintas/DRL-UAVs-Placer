import csv
import pickle

headers = {
    'date': 0,
    'time': 1,
    'id': 2,
    'line': 3,
    'latitude': 4,
    'longitude': 5,
    'speed': 6,
}

buses_ids = set()


def convert_to_dict(row):
    if len(row) == len(headers.keys()):
        date, time, id, line, latitude, longitude, speed = row
        buses_ids.add(id)
        return {
            'date': date,
            'time': time,
            'id': id,
            'line': line,
            'longitude': longitude,
            'latitude': latitude,
            'speed': speed
        }

    return {}


with open('/content/data/all_buses_2014_10_03.csv', 'r') as csv_file:
    data = csv.reader(csv_file)
    rows = [convert_to_dict(row) for row in data]

for id in buses_ids:
    mobility_trace = list(
        filter(
            lambda row: 'id' in row.keys() and row['id'] == id,
            rows))
    print(id, len(mobility_trace))

    mobility_trace.sort(key=lambda row: row['latitude'])
    max_latitude = float(mobility_trace[0]['latitude'])
    min_latitude = float(mobility_trace[-1]['latitude'])

    mobility_trace.sort(key=lambda row: row['longitude'])
    max_longitude = float(mobility_trace[0]['longitude'])
    min_longitude = float(mobility_trace[-1]['longitude'])

    def normalize(min, max, value):
        return (float(value) - min) / (max - min) * 100.0

    def normalize_latitude_and_longitude(row):
        data = row
        if (min_latitude != max_latitude and min_longitude != max_longitude):
            data.update({
                'latitude': normalize(min_latitude, max_latitude, row['latitude']),
                'longitude': normalize(min_longitude, max_longitude, row['longitude']),
            })
        return data

    mobility_trace = sorted(list(map(
        normalize_latitude_and_longitude, mobility_trace)), key=lambda row: row['time'])

    with open(f'/content/data/{id}_20141003.csv', 'w') as csv_file:
        csv_file.write(','.join(headers.keys()))
        csv_file.write('\n')

        for row in mobility_trace:
            csv_file.write(','.join(map(str, row.values())))
            csv_file.write('\n')
