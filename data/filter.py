import sys, json
from shapely.geometry import shape, Point
from multiprocessing import Pool
from os import listdir

def filter(geojson, data, result):
    with open(geojson) as f:
        js = json.load(f)

    polygon = shape(js['geometry'])

    with open(data, 'r') as infile, open(result, 'w') as outfile:
	lineNum = 0
        for line in infile:
	    if lineNum % 10000 == 0:
		print 'Processing line %s from %s' % (lineNum, data)
	    lineNum += 1

            try:
                values = line.split(',')
                point = Point(float(values[9]), float(values[10]))
                if polygon.contains(point):
                    outfile.write(line)
            except ValueError:
                pass
    print 'Finished processing file %s' % data

def wrapper(args):
    return filter(*args)

if __name__ == '__main__':
    pool = Pool(processes=30)
    args = []
    for name in listdir('.'):
        if name.startswith('trip_data'):
            index = name.split('_')[-1]
            args.append((sys.argv[1], name, 'result/filtered_data_%s.csv' % index))
    pool.map(wrapper, args)


