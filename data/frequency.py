import sys, json, math
from multiprocessing import Pool
from os import listdir

def frequency(clusters, data, output):
    result = []
    with open(clusters) as f:
        values = f.readlines()
        for value in values:
            longitude, latitude = value.strip('\n').split(',')
            result.append({
                'longitude': float(longitude),
                'latitude': float(latitude),
                'dropoff_times': dict((time, 0) for time in range(24))})

    with open(data, 'r') as infile:
        for line in infile:
            values = line.split(',')
            longitude = float(values[9])
            latitude = float(values[10])

            minDistance = float('inf')
            belongsTo = None

            for cluster in result:
                distance = math.sqrt((longitude-cluster['longitude'])**2 + (latitude-cluster['latitude'])**2)
                if distance < minDistance:
                    minDistance = distance
                    belongsTo = cluster

            dropoffHours = int(values[1].split(' ')[-1].split(':')[0])
            belongsTo['dropoff_times'][dropoffHours] += 1

    with open(output, 'w') as outfile:
        json.dump(result, outfile)

    print 'Finished processing file %s' % data

def wrapper(args):
    return frequency(*args)

def merge_results(base_path):
    result = []
    for name in listdir(base_path):
        if name.startswith('freq'):
            f = open(base_path + '/' + name, 'r')
            data = json.loads(''.join(f.readlines()))
            for point in data:
                added = False
                for r in result:
                    if r['latitude'] == point['latitude'] and r['longitude'] == point['longitude']:
                        for time in r['dropoff_times']:
                            r['dropoff_times'][time] += point['dropoff_times'][time]
                        added = True
                        break
                if not added:
                    result.append(point)
    return result

if __name__ == '__main__':
    pool = Pool()
    args = []
    for name in listdir('.'):
        if name.startswith('trip_data'):
            index = name.split('_')[-1]
            args.append((sys.argv[1], name, 'result/frequency_%s.json' % index))
    pool.map(wrapper, args)


