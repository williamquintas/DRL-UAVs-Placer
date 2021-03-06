import csv


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


def convert_to_dict(row_data):
    if len(row_data) == len(headers.keys()):
        date, time, uuid, line, latitude, longitude, speed = row_data
        buses_ids.add(uuid)
        return {
            'date': date,
            'time': time,
            'id': uuid,
            'line': line,
            'longitude': longitude,
            'latitude': latitude,
            'speed': speed
        }

    return {}


def filter_by_bus_id(row_data, searched_id):
    return 'id' in row_data.keys() and row_data['id'] == searched_id


with open('/content/data/all_buses_2014_10_03.csv', 'r', encoding="utf-8") as csv_file:
    data = csv.reader(csv_file)
    rows = [convert_to_dict(row) for row in data]

for bus_id in buses_ids:
    mobility_trace = list(
        filter(
            filter_by_bus_id(row, bus_id),
            rows))
    print(bus_id, len(mobility_trace))

    mobility_trace.sort(key=lambda row: row['latitude'])
    max_latitude = float(mobility_trace[0]['latitude'])
    min_latitude = float(mobility_trace[-1]['latitude'])

    mobility_trace.sort(key=lambda row: row['longitude'])
    max_longitude = float(mobility_trace[0]['longitude'])
    min_longitude = float(mobility_trace[-1]['longitude'])

    def normalize(min_value, max_value, value):
        return (float(value) - min_value) / (max_value - min_value) * 100.0

    def normalize_latitude_and_longitude(row_data):
        updated_data = row_data
        if (min_latitude != max_latitude and min_longitude != max_longitude):
            updated_data.update({
                'latitude': normalize(min_latitude, max_latitude, row_data['latitude']),
                'longitude': normalize(min_longitude, max_longitude, row_data['longitude']),
            })
        return updated_data

    mobility_trace = sorted(list(map(
        normalize_latitude_and_longitude, mobility_trace)), key=lambda row: row['time'])

    with open(f'/content/data/{bus_id}_20141003.csv', 'w', encoding='utf-8') as csv_file:
        csv_file.write(','.join(headers.keys()))
        csv_file.write('\n')

        for row in mobility_trace:
            csv_file.write(','.join(map(str, row.values())))
            csv_file.write('\n')
