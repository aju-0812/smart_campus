"""Transport Information Agent — Route planning + delay prediction."""
from typing import List, Dict, Optional
from sqlalchemy.orm import Session
from app.models.models import Bus, BusStop, BusSchedule, BusDelay
from datetime import date, datetime
import heapq
import statistics


def get_all_buses(db: Session) -> List[Dict]:
    buses = db.query(Bus).filter(Bus.is_active == True).all()
    return [
        {
            "bus_number": b.bus_number,
            "route_name": b.route_name,
            "capacity": b.capacity,
            "driver_name": b.driver_name,
            "driver_phone": b.driver_phone,
            "stop_count": len(b.stops),
        }
        for b in buses
    ]


def get_bus_stops(db: Session, bus_number: str) -> Dict:
    bus = db.query(Bus).filter(Bus.bus_number == bus_number).first()
    if not bus:
        return {"error": f"Bus {bus_number} not found"}

    return {
        "bus_number": bus_number,
        "route_name": bus.route_name,
        "stops": [
            {
                "order": stop.stop_order,
                "name": stop.stop_name,
                "scheduled_arrival": stop.scheduled_arrival,
                "latitude": stop.latitude,
                "longitude": stop.longitude,
            }
            for stop in sorted(bus.stops, key=lambda s: s.stop_order)
        ]
    }


def get_bus_schedule(db: Session, bus_number: str) -> Dict:
    bus = db.query(Bus).filter(Bus.bus_number == bus_number).first()
    if not bus:
        return {"error": f"Bus {bus_number} not found"}

    return {
        "bus_number": bus_number,
        "route_name": bus.route_name,
        "schedules": [
            {
                "direction": s.direction,
                "departure_time": s.departure_time,
                "arrival_time": s.arrival_time,
                "days": s.days_of_operation,
            }
            for s in bus.schedules
        ]
    }


def predict_delay(db: Session, bus_number: str) -> Dict:
    """Exponential smoothing on historical delay data to predict today's delay."""
    bus = db.query(Bus).filter(Bus.bus_number == bus_number).first()
    if not bus:
        return {"error": f"Bus {bus_number} not found"}

    delays = db.query(BusDelay).filter(
        BusDelay.bus_id == bus.id
    ).order_by(BusDelay.delay_date.desc()).limit(30).all()

    if not delays:
        return {
            "bus_number": bus_number,
            "predicted_delay_minutes": 0,
            "confidence": "Low (no history)",
            "message": "No delay history available. Bus expected on time."
        }

    delay_values = [d.delay_minutes for d in reversed(delays)]

    # Simple exponential smoothing
    alpha = 0.3
    smoothed = delay_values[0]
    for v in delay_values[1:]:
        smoothed = alpha * v + (1 - alpha) * smoothed

    predicted = round(smoothed)
    avg = statistics.mean(delay_values)
    std = statistics.stdev(delay_values) if len(delay_values) > 1 else 0

    # Common delay reasons
    recent_reasons = [d.reason for d in delays[:5] if d.reason]
    common_reason = max(set(recent_reasons), key=recent_reasons.count) if recent_reasons else "Unknown"

    status = "On Time" if predicted <= 2 else "Slight Delay" if predicted <= 10 else "Significant Delay"

    return {
        "bus_number": bus_number,
        "route_name": bus.route_name,
        "predicted_delay_minutes": predicted,
        "historical_avg_delay": round(avg, 1),
        "status": status,
        "common_reason": common_reason,
        "confidence": "High" if len(delay_values) >= 20 else "Medium",
        "samples_used": len(delay_values),
        "message": f"Bus {bus_number} is predicted to be {predicted} min late. Status: {status}."
    }


def get_optimal_bus_route(db: Session, from_stop: str, to_stop: str) -> Dict:
    """Find optimal bus route between two stops using Dijkstra on stop graph."""
    all_buses = db.query(Bus).filter(Bus.is_active == True).all()

    # Build graph: stop_name → [(cost, next_stop, bus_number)]
    graph: Dict[str, List] = {}
    for bus in all_buses:
        stops = sorted(bus.stops, key=lambda s: s.stop_order)
        for i in range(len(stops) - 1):
            src = stops[i].stop_name
            dst = stops[i + 1].stop_name
            # Cost = approximate time between stops (15 min default)
            cost = 15
            if src not in graph:
                graph[src] = []
            if dst not in graph:
                graph[dst] = []
            graph[src].append((cost, dst, bus.bus_number))
            graph[dst].append((cost, src, bus.bus_number))  # bidirectional

    if from_stop not in graph:
        # Try partial match
        matches = [s for s in graph if from_stop.lower() in s.lower()]
        if matches:
            from_stop = matches[0]
        else:
            return {"error": f"Stop '{from_stop}' not found in any bus route"}

    if to_stop not in graph:
        matches = [s for s in graph if to_stop.lower() in s.lower()]
        if matches:
            to_stop = matches[0]
        else:
            return {"error": f"Stop '{to_stop}' not found in any bus route"}

    # Dijkstra
    dist = {stop: float('inf') for stop in graph}
    dist[from_stop] = 0
    prev = {}
    pq = [(0, from_stop, [])]  # (cost, stop, path)

    while pq:
        cost, stop, path = heapq.heappop(pq)
        if cost > dist[stop]:
            continue
        if stop == to_stop:
            return {
                "from": from_stop,
                "to": to_stop,
                "estimated_time_minutes": cost,
                "path": path + [stop],
                "message": f"Estimated travel time: {cost} minutes via {len(path)} stops."
            }
        for weight, neighbor, bus_num in graph.get(stop, []):
            new_cost = cost + weight
            if new_cost < dist[neighbor]:
                dist[neighbor] = new_cost
                heapq.heappush(pq, (new_cost, neighbor, path + [stop]))

    return {"error": "No route found between these stops"}
