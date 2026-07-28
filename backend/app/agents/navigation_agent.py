"""Navigation Agent — Dijkstra + A* pathfinding on campus graph."""
import heapq
from typing import List, Dict, Optional, Tuple
from sqlalchemy.orm import Session
from app.models.models import Building, CampusRoute
from loguru import logger
import math


def _build_graph(db: Session) -> Tuple[Dict, Dict]:
    """Build adjacency list from DB routes. Returns (graph, building_map)."""
    buildings = db.query(Building).all()
    routes = db.query(CampusRoute).all()

    building_map = {b.id: b for b in buildings}
    graph: Dict[int, List[Tuple[float, int]]] = {b.id: [] for b in buildings}

    for route in routes:
        graph[route.source_id].append((route.walk_time_minutes, route.destination_id))
        graph[route.destination_id].append((route.walk_time_minutes, route.source_id))  # undirected

    return graph, building_map


def _heuristic(b1: Building, b2: Building) -> float:
    """Euclidean heuristic using lat/lon (degrees ≈ km scale)."""
    dlat = b1.latitude - b2.latitude
    dlon = b1.longitude - b2.longitude
    return math.sqrt(dlat**2 + dlon**2) * 111  # rough km conversion → walk minutes


def dijkstra(graph: Dict, start_id: int, end_id: int) -> Tuple[float, List[int]]:
    """Standard Dijkstra shortest path. Returns (cost, path_ids)."""
    dist = {node: float('inf') for node in graph}
    dist[start_id] = 0
    prev = {node: None for node in graph}
    pq = [(0, start_id)]

    while pq:
        cost, node = heapq.heappop(pq)
        if cost > dist[node]:
            continue
        if node == end_id:
            break
        for weight, neighbor in graph.get(node, []):
            new_cost = cost + weight
            if new_cost < dist[neighbor]:
                dist[neighbor] = new_cost
                prev[neighbor] = node
                heapq.heappush(pq, (new_cost, neighbor))

    path, cur = [], end_id
    while cur is not None:
        path.append(cur)
        cur = prev[cur]
    path.reverse()

    return dist[end_id], path


def a_star(graph: Dict, building_map: Dict, start_id: int, end_id: int) -> Tuple[float, List[int]]:
    """A* pathfinding using lat/lon heuristic."""
    open_set = [(0, start_id)]
    g_score = {node: float('inf') for node in graph}
    g_score[start_id] = 0
    f_score = {node: float('inf') for node in graph}
    if start_id in building_map and end_id in building_map:
        f_score[start_id] = _heuristic(building_map[start_id], building_map[end_id])
    came_from = {}

    while open_set:
        _, current = heapq.heappop(open_set)
        if current == end_id:
            path, cur = [], current
            while cur in came_from:
                path.append(cur)
                cur = came_from[cur]
            path.append(start_id)
            path.reverse()
            return g_score[end_id], path

        for weight, neighbor in graph.get(current, []):
            tentative_g = g_score[current] + weight
            if tentative_g < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = tentative_g
                h_val = _heuristic(building_map[neighbor], building_map[end_id]) if neighbor in building_map and end_id in building_map else 0.0
                f_score[neighbor] = tentative_g + h_val
                heapq.heappush(open_set, (f_score[neighbor], neighbor))

    return float('inf'), []


def get_route(db: Session, from_name: str, to_name: str) -> Dict:
    """Find shortest route between two buildings by name."""
    logger.info(f"Navigation Agent: get_route from={from_name} to={to_name}")
    try:
        from_b = db.query(Building).filter(Building.name.ilike(f"%{from_name}%")).first()
        to_b = db.query(Building).filter(Building.name.ilike(f"%{to_name}%")).first()

        if not from_b:
            return {"error": f"Building '{from_name}' not found"}
        if not to_b:
            return {"error": f"Building '{to_name}' not found"}
        if from_b.id == to_b.id:
            return {"error": "Source and destination are the same building"}

        graph, building_map = _build_graph(db)

        # Use A* for pathfinding
        cost, path_ids = a_star(graph, building_map, from_b.id, to_b.id)

        if cost == float('inf'):
            logger.warning(f"Navigation Agent: No route found between {from_b.name} and {to_b.name}")
            return {"error": "No route found between these buildings"}

        path_names = [building_map[pid].name for pid in path_ids if pid in building_map]

        return {
            "from": from_b.name,
            "to": to_b.name,
            "walk_time_minutes": round(cost, 1),
            "distance_estimate_meters": round(cost * 80),  # avg walking 80m/min
            "path": path_names,
            "path_ids": path_ids,
            "hops": len(path_ids) - 1,
            "algorithm": "A*"
        }
    except Exception as e:
        logger.exception(f"Navigation Agent error in get_route: {e}")
        return {"error": f"Error calculating route: {str(e)}"}


def get_all_buildings(db: Session) -> List[Dict]:
    logger.info("Navigation Agent: get_all_buildings")
    try:
        buildings = db.query(Building).all()
        return [
            {
                "id": b.id,
                "code": b.building_code,
                "name": b.name,
                "type": b.building_type,
                "floors": b.floors,
                "latitude": b.latitude,
                "longitude": b.longitude,
                "description": b.description,
            }
            for b in buildings
        ]
    except Exception as e:
        logger.exception(f"Navigation Agent error in get_all_buildings: {e}")
        return []


def get_campus_graph(db: Session) -> Dict:
    """Return full campus graph as adjacency list for frontend map rendering."""
    logger.info("Navigation Agent: get_campus_graph")
    try:
        buildings = get_all_buildings(db)
        routes = db.query(CampusRoute).all()
        edges = [
            {
                "source_id": r.source_id,
                "destination_id": r.destination_id,
                "distance_meters": r.distance_meters,
                "walk_time_minutes": r.walk_time_minutes,
            }
            for r in routes
        ]
        return {"buildings": buildings, "edges": edges}
    except Exception as e:
        logger.exception(f"Navigation Agent error in get_campus_graph: {e}")
        return {"buildings": [], "edges": []}
