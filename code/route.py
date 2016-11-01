'''
Q1.     Which search algorithm seems to work best for each routing options?
ANS:    In case of BFS, DFS and IDS, same route will be returned irrespective of the routing option.
        This route will provide optimal number of segments in case of BFS and IDS.
        Routing option      Best Algorithm
        Distance            A-Star (0.0311 sec)
        Time                A-Star (0.0304 sec)
        Scenic              A-Star (0.0121 sec)
        Segments            A-Star (0.0475  sec)

Q2.     Which algorithm is fastest in terms of the amount of computation time required by your program, and by how much,
        according to your experiments?
ANS:    A-star algorithm is the fastest in case of computation time(excluding the time for computing geographical location co-ordinates for unknown cities)
        as the search space is reduced using the heuristic function.
        function. When compared with BFS, A-star is about 8-10 times faster when considering the amount of computation.
        As the distance between source and destination increases, A-star proves to be much faster.

Q3.     Which algorithm requires the least memory, and by how much, according to your experiments?
ANS:    A-star requires least memory as it considers most probable next node into consideration and does not unnecessarily
        traverse incorrect cities. When checked the maximum fringe size for a route from Bloomington, Indiana to Chicago,Illinois, max fringe size using
        BFS = 85 and A-Star = 60.  The memory saved in case of A-star is approximately 30% over BFS.

Q4.     Which heuristic function did you use, how good is it, and how might you make it better?
ANS:    In case of routing option Distance, I have used Euclidean distance from current city to destination. There is
        no location information for about 1500 cities or junctions, they were needed to be calculated. I have calculated the median of the
        latitudes and longitudes of the neighbouring cities to estimate the location of the unknown cities or junctions.
        To adjust this estimated location co-ordinates, using Euclidean distance provided the best estimate.
        Route option = Distance, Euclidean Distance is the heuristic function
        Route option = Speed, Euclidean distance is used a heuristic function along with the formula of time.
                        Time = Distance / Speed
        Route option = Segments, heuristic value of distance using Euclidean distance is multiplied with the factor of edges/mile.
                        The multiplication factor of edges/mile is calculated by calculating entire distance of the graph and total
                        number of edges in the graph.
        Route option = Scenic, The concept of adding penalty is used far highways. Whenever a highway is encountered(speed > 55),
                        a factor of modulus(55-speed) is multiplied as a penalty to the highway route. This would reduce the
                        probablity of selecting highway route over scenic route.

        Alternatively, I can use Haversine's distance formula which uses the great circle distance. This would work well if the location co-ordinates are
        correctly predicted.

Q5.     Supposing you start in Bloomington, which city should you travel to if you want to take the longest possible drive (in miles) that is still the shortest path to that city?
ANS:    Skagway,_Alaska is the farthest city from Bloomington,_Indiana. It is about 4814 miles away from Bloomington,_IN.
        This is calculated using Dijkstra's algorithm which will find out shortest route to the farthest city.
'''


from scipy.spatial import distance
import City as C, Location as L
import sys
import time

route = []
visited = []
city_list = {}
highway_list = {}
missing_locations = []
graph_edges = 0.0
graph_distance = 0.0

# Constructs graph in the form of ajacency list: City Name --> [List of adjacent cities]
def draw_edge(city_dict,city, city_data):
    global graph_edges, graph_distance

    if city not in city_dict:
        city_dict[city] = [city_data]
    else:
        city_dict[city].append(city_data)
        graph_edges = graph_edges + 1
        graph_distance = graph_distance + int(city_data.distance)

    city_data1 = C.City()
    city_data1.city = city
    city = city_data.city
    city_data1.distance = city_data.distance
    city_data1.speed = city_data.speed
    city_data1.highway = city_data.highway

    if city_data.city not in city_dict:
        city_dict[city] = [city_data1]
    else:
        city_dict[city].append(city_data1)
        graph_edges = graph_edges + 1
        graph_distance = graph_distance + int(city_data.distance)

    city_list[city_data.city] = city_data
    city_list[city_data1.city] = city_data1


# Load data 3 from data files - road-segments, city-gps, no_gps_cities
def load_data(path1, path2, path3):

    dataFile1 = open(path1, 'r')
    count = 0
    for dataLine in dataFile1:
        ele = dataLine.split()
        ele[len(ele) - 1] = ele[len(ele) - 1].split('\n', 2)[0]
        city_data = C.City()
        city_data.city = ele[1]
        city_data.distance = ele[2]
        if ele[3] == '0' or len(ele)<5:
            city_data.speed = 50
            city_data.highway = ele[3]
        else:
            city_data.speed = ele[3]
            city_data.highway = ele[4]
        city_data.time = float(eval(str(city_data.distance))) / float(eval(str(city_data.speed)))
        draw_edge(city_dict,ele[0],city_data)
    dataFile1.close()

    dataFile2 = open(path2, 'r')
    for dataLine2 in dataFile2:
        ele = dataLine2.split()
        if len(ele) == 3:
            city_location = L.Location()
            city_location.city = ele[0]
            city_location.latitude = ele[1]
            city_location.longitude = ele[2]
            location_dict[city_location.city] = city_location

    dataFile3 = open(path3, 'r')
    for dataLine2 in dataFile3:
        ele = dataLine2.split()
        missing_locations.append(ele)

    calc_missing_loc_coordinates(missing_locations)
    dataFile2.close()


# Start finding path using BFS, DFS, IDS and ASTAR
def find_path():
    visited = {}
    if source not in city_dict.keys() or destination not in city_dict.keys():
        print 'Invalid Source-Destination'
        print 'Please input correct source and destination'
        return

    for city in city_dict.keys():
        if city == source:
            if routing_algorithm == "bfs" and len(route_option) > 0:
                bfs(source,None, destination)
            elif routing_algorithm == "dfs" and len(route_option) > 0:
                dfs(source,None, destination)
            elif routing_algorithm == "ids" and len(route_option) > 0:
                ids(source,destination)
            elif routing_algorithm == "astar":
                astar()
            else:
                print 'Invalid input\n'
                print 'Please input in the following format:\n'
                print '[filename] [source] [destination] [routing option] [routing algorithm]'
            break

# Track back from destination to source
def track_route(d, city_list):
    route = [d]
    segment_count = 0
    city_to_track = city_list[d]
    total_distance = int(city_to_track.distance)
    total_time = 0
    while city_to_track != None:
        segment_count += 1
        route.append(city_to_track.city)
        if city_to_track.parent != source:
            total_time = total_time + city_to_track.time
            total_distance = total_distance + int(city_to_track.distance)
            city_to_track = city_list[city_to_track.parent]
        else:
            city_to_track = None

    route.append(source)
    route.reverse()

    print '\n\nSource' + '\t\t\t' + 'Destination' + '\t\t' + 'Distance' + '    ' + 'Time' + '\n'
    print '---------------------------------------------------------------'
    for i in range(len(route)-2):
        print str(city_list[route[i]].city) + '\t' + str(city_list[route[i+1]].city) + '\t' + str(city_list[route[i+1]].distance) + ' mi \t' + str(round(city_list[route[i+1]].time,2)) + ' hrs\n'

    printable_route = ''
    printable_route = str(total_distance) + ' ' + str(round(total_time,2)) + ' '
    for route_city in route:
        printable_route = printable_route + route_city+' '
    print printable_route
    return


#  Breadth First Search
def bfs(city_name, city, destination):
    visited.append(city_name)
    fringe = [city_name]
    current_city = city_name

    while len(fringe) > 0:
        current_city = fringe.pop(0)
        if current_city == destination:
            track_route(current_city, city_list)
            return
        for neighbour in city_dict[current_city]:
            if neighbour.city not in visited:
                visited.append(neighbour.city)
                fringe.append(neighbour.city)
                fringe_size.append(len(fringe))

                city_list[neighbour.city].parent = current_city
                city_list[neighbour.city].time = float(city_list[neighbour.city].distance)/float(city_list[neighbour.city].speed)

def dfs(city_name, city, destination):
    visited.append(city_name)
    fringe = [city_name]
    current_city = city_name

    while len(fringe) > 0:
        current_city = fringe.pop()
        if current_city == destination:
            track_route(current_city, city_list)
        for neighbour in city_dict[current_city]:
            if neighbour.city not in visited:
                visited.append(neighbour.city)
                fringe.append(neighbour.city)
                city_list[neighbour.city].parent = current_city
                city_list[neighbour.city].time = float(city_list[neighbour.city].distance)/float(city_list[neighbour.city].speed)


def ids(source,destination, max_depth=5000):
    for limit in range(1,max_depth+1):
        found=iddfs(source,destination,limit,path=[])
        if found :
            track_route(destination, city_list)
            return
    if found ==None: print("Not found")

def iddfs(start,end,limit,path=None):
    if start not in path: path.append(start)
    if start == end: return True
    if limit <=0: return False

    for nextVertex in city_dict[start]:
        if nextVertex.city not in path:
            city_list[nextVertex.city].parent = start
            found=iddfs(nextVertex.city,end,limit-1,path)
            if found: return found

# Calculate value for h(n) when routing option = distance
def calc_heuristic_distance(city):
    city_a = (float(location_dict[city].longitude), float(location_dict[city].latitude))
    city_b = (float(location_dict[destination].longitude), float(location_dict[destination].latitude))
    #geographic_dist = great_circle(city_a, city_b).miles
    geographic_dist = distance.euclidean(city_a,city_b)
    return geographic_dist

# Calculate value for h(n) when routing option = time
def calc_heuristic_time(city):
    dist = calc_heuristic_distance(city)
    speed = 60
    time = int(dist) / float(speed)
    return time

# Calculate value for h(n) when routing option = scenic
def calc_heuristic_scenic(city):
    dist = calc_heuristic_distance(city)
    new_dist = int(dist) * (abs(int(city_list[city].speed)- 55))
    return new_dist

# Calculate value for h(n) when routing option = segments
def calc_heuristic_segments(city):
    dist = calc_heuristic_distance(city)
    estimated_segments = int(dist) * (graph_edges/graph_distance)
    return estimated_segments


# Calculate missing city geo locations (latitude, longitude)
def calc_missing_loc_coordinates(missing_locations):
    if len(missing_locations) ==0:
        return

    extra_location_list = []
    cnt = 0
    for junction in missing_locations:
        cities_on_junction = city_dict[junction[0]]
        cnt = cnt + 1
        temp1 = []
        for c in cities_on_junction:
            if c.city in location_dict and location_dict[c.city] != None:
                temp1.append(c.city)

        if len(temp1) == 0:
            extra_location_list.append([junction[0]])
        else:
            cities_on_junction = temp1
            highway_loc = L.Location()
            lat_junction = 0.0
            long_junction = 0.0

            if len(cities_on_junction) >= 1:
                for city in cities_on_junction:
                    if location_dict[city]!=None or location_dict[city].latitude != None:
                        lat_junction = lat_junction + float(location_dict[city].latitude)
                        long_junction = long_junction + float(location_dict[city].longitude)

                highway_loc.city = junction
                highway_loc.latitude = lat_junction/len(cities_on_junction)
                highway_loc.longitude = long_junction/len(cities_on_junction)
                location_dict[junction[0]] = highway_loc
    calc_missing_loc_coordinates(extra_location_list)

# Astar algorithm for routing options -
#   1. distance
#   2. time
#   3. segments
#   4. scenic

def astar():
    fringe = {}
    visited_astar = [source]
    fringe[source]= 0
    current_city = source
    heuristic_dist = 0

    while len(fringe) > 0:
        current_city = min(fringe, key=fringe.get)
        current_city_val = fringe[current_city]
        del fringe[current_city]

        if current_city == destination:
            track_route(current_city,city_list)
            return

        for neighbour in city_dict[current_city]:
            if route_option == "distance":
                heuristic_dist = calc_heuristic_distance(neighbour.city)
                distance = current_city_val + int(neighbour.distance) + heuristic_dist
                if neighbour.city not in fringe or distance < fringe[neighbour.city]:
                    if neighbour.city not in visited_astar:
                        visited_astar.append(neighbour.city)
                        city_list[neighbour.city].parent = current_city
                        city_list[neighbour.city].distance = distance
                        fringe[neighbour.city] = distance
                        fringe_size.append(len(fringe))

            elif route_option == "time":
                heuristic_time = calc_heuristic_time(neighbour.city)

                time = current_city_val + float(neighbour.distance)/float(neighbour.speed) + heuristic_time
                if neighbour.city not in fringe or time < fringe[neighbour.city]:
                    if neighbour.city not in visited_astar:
                        visited_astar.append(neighbour.city)
                        city_list[neighbour.city].time = float(neighbour.distance)/float(neighbour.speed)
                        city_list[neighbour.city].parent = current_city
                        fringe[neighbour.city] = time
                        fringe_size.append(len(fringe))

            elif route_option == "segments":
                predicted_segs = calc_heuristic_segments(neighbour.city)
                segments = current_city_val + predicted_segs +1
                if neighbour.city not in fringe or predicted_segs < fringe[neighbour.city]:
                    if neighbour.city not in visited_astar:
                        visited_astar.append(neighbour.city)
                        city_list[neighbour.city].segments = segments
                        city_list[neighbour.city].parent = current_city
                        fringe[neighbour.city] = segments
                        fringe_size.append(len(fringe))

            elif route_option == "scenic":
                heuristic_scenic_path = calc_heuristic_scenic(neighbour.city)
                dist = current_city_val + heuristic_scenic_path
                if neighbour.city not in fringe:
                    if neighbour.city not in visited_astar:
                        visited_astar.append(neighbour.city)
                        city_list[neighbour.city].time = float(neighbour.distance)/float(neighbour.speed)
                        city_list[neighbour.city].parent = current_city
                        city_list[neighbour.city].distance = dist
                        fringe[neighbour.city] = dist
                        fringe_size.append(len(fringe))

    return


# command line arguments
source, destination, route_option, routing_algorithm = sys.argv[1:5]
avg_time = []
city_dict = {}
location_dict = {}
fringe_size = []

load_data('../data/road-segments.txt','../data/city-gps.txt','../data/no_gps_cities.txt')
start = time.time()
find_path()
end = time.time()
