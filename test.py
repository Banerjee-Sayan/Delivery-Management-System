import math
from heapq import heappop, heappush

def haversine_distance(coord1, coord2):
    """Calculates the distance between two coordinates using the Haversine formula."""
    lon1, lat1 = coord1
    lon2, lat2 = coord2

    R = 6371  # Earth radius in kilometers
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)

    a = math.sin(dlat / 2) ** 2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon / 2) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    distance = R * c
    return distance

def heuristic(coord1, coord2):
    """Estimates the remaining distance from coord1 to coord2 using Euclidean distance."""
    lon1, lat1 = coord1
    lon2, lat2 = coord2

    x_diff = lon2 - lon1
    y_diff = lat2 - lat1
    return math.sqrt(x_diff**2 + y_diff**2)

def astar(graph, start, goal):
    """Finds the shortest path between start and goal using the A* algorithm."""
    open_set = [(0, start)]  # Priority queue using heap
    came_from = {}
    g_scores = {node: float('inf') for node in graph}
    g_scores[start] = 0
    f_scores = {node: float('inf') for node in graph}
    f_scores[start] = heuristic(start, goal)

    while open_set:
        current_f, current_node = heappop(open_set)

        if current_node == goal:
            return reconstruct_path(came_from, start, goal)

        for neighbor, cost in graph[current_node]:
            tentative_g_score = g_scores[current_node] + cost
            if tentative_g_score < g_scores[neighbor]:
                came_from[neighbor] = current_node
                g_scores[neighbor] = tentative_g_score
                f_scores[neighbor] = tentative_g_score + heuristic(neighbor, goal)
                heappush(open_set, (f_scores[neighbor], neighbor))

    return []  # No path found

def reconstruct_path(came_from, start, goal):
    """Reconstructs the path from goal to start using the came_from dictionary."""
    path = []
    while goal in came_from:
        path.append(goal)
        goal = came_from[goal]
    path.append(start)
    path.reverse()
    return path

# Example usage:
graph = {
    (10.0, 20.0): [((5.0, 15.0), 5), ((15.0, 25.0), 10), ((4, 4), 25)],  # Add connections
    
}
start = (10.0, 20.0)  # Example start coordinates
goal = (30.0, 40.0)  # Example goal coordinates

path = astar(graph, start, goal)

if path:
    print("Shortest path:", path)
    total_distance = sum(haversine_distance(graph[path[i]][0], graph[path[i + 1]][0]) for i in range(len(path) - 1))
    print("Total distance:", total_distance, "km")
else:
    print("No path found")
