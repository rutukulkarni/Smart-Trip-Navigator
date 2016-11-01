from scipy.spatial import distance

source = "Bloomington,_Indiana"

routeFound = 0
route = []
visited = []
city_list = {}


# class for location data
class Location:
    def _init_(self):
        self.city = ''
        self.latitude = 0.0
        self.longitude = 0.0

# class for city data - parent to city
class City:
    def __init__(self):
        self.city = ""
        self.distance = 0
        self.speed = 0
        self.highway = ""
        self.parent = None


# constructs graph in the form of ajacency list
def draw_edge(city_dict,city, city_data):
    if city not in city_dict:
        city_dict[city] = [city_data]
    else:
        city_dict[city].append(city_data)

    city_data1 = City()
    city_data1.city = city
    city = city_data.city
    city_data1.distance = city_data.distance
    city_data1.speed = city_data.speed
    city_data1.highway = city_data.highway

    if city_data.city not in city_dict:
        city_dict[city] = [city_data1]
    else:
        city_dict[city].append(city_data1)
    city_list[city_data.city] = city_data
    city_list[city_data1.city] = city_data1

# load data from data files - road-segments, city-gps
def load_data(path1, path2):
    dataFile1 = open(path1, 'r')

    for dataLine in dataFile1:
        ele = dataLine.split(' ')
        ele[len(ele) - 1] = ele[len(ele) - 1].split('\n', 2)[0]
        city_data = City()
        city_data.city = ele[1]
        city_data.distance = ele[2]
        city_data.speed = ele[3]
        city_data.highway = ele[4]

        draw_edge(city_dict,ele[0],city_data)
    dataFile1.close()

    dataFile2 = open(path2, 'r')
    for dataLine in dataFile2:
        ele = dataLine.split(' ')
        city_location = Location()
        city_location.city = ele[0]
        city_location.latitude = ele[1]
        city_location.longitude = ele[2]

        location_dict[city_location.city] = city_location

def find_path(city_dict):
    routeFound = 0
    visited = {}
    for city in city_dict.keys():
        if city == source:
            dijkstra()
            break

def track_route(d, city_list):
    route = [d]
    count = 0
    total_distance = 0
    city_to_track = city_list[d]
    total_distance = int(city_to_track.distance)

    while city_to_track != None:
        count += 1
        route.append(city_to_track.parent)
        if city_to_track.parent != source:
            city_to_track = city_list[city_to_track.parent]
        else:
            city_to_track = None
    print 'Farthest City = ', d
    print 'Total distance = ', str(total_distance) +' miles'
    return

def dijkstra():
    fringe = {}
    visited_astar = [source]
    fringe[source]= 0
    current_city = source

    while len(fringe) > 0:
        current_city = min(fringe, key=fringe.get)
        current_city_dist = fringe[current_city]
        del fringe[current_city]

        for neighbour in city_dict[current_city]:
            distance = current_city_dist + int(neighbour.distance)
            if neighbour.city not in fringe or distance < fringe[neighbour.city]:
                if neighbour.city not in visited_astar:
                    visited_astar.append(neighbour.city)
                    city_list[neighbour.city].parent = current_city
                    city_list[neighbour.city].distance = distance
                    fringe[neighbour.city] = distance
    track_route(current_city,city_list)
    return


####################################################################
city_dict = {}
location_dict = {}
load_data('../data/road-segments.txt','../data/city-gps.txt')
find_path(city_dict)