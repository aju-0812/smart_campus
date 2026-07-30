"""Transport Information Agent — Route planning + delay prediction."""
from typing import List, Dict, Optional
from sqlalchemy.orm import Session
from app.models.models import Bus, BusStop, BusSchedule, BusDelay, BusTicketBooking
from loguru import logger
from datetime import date, datetime
import heapq
import statistics
import random
import time

def get_all_buses(db: Session, city: Optional[str] = None) -> List[Dict]:
    logger.info(f"Transport Agent: get_all_buses city={city}")
    try:
        query = db.query(Bus).filter(Bus.is_active == True)
        if city and city.lower() != "all":
            query = query.filter(Bus.city == city)
        buses = query.all()
        
        now = datetime.now()
        progress_pct = int((now.second * 100) / 60)
        
        res = []
        for b in buses:
            # Deterministic pseudo-random speed & occupancy based on bus id
            random.seed(b.id + 42)
            speed = random.randint(25, 45)
            occupancy = random.randint(28, 48)
            random.seed() # reset seed
            
            res.append({
                "id": b.id,
                "bus_number": b.bus_number,
                "city": b.city or "Coimbatore",
                "route_name": b.route_name,
                "capacity": b.capacity,
                "driver_name": b.driver_name,
                "driver_phone": b.driver_phone,
                "stop_count": len(b.stops),
                "speed_kmh": speed,
                "occupancy": occupancy,
                "live_status": "En Route",
                "progress_pct": progress_pct
            })
        return res
    except Exception as e:
        logger.exception(f"Transport Agent error in get_all_buses: {e}")
        return []

def get_bus_stops(db: Session, bus_number: str) -> Dict:
    logger.info(f"Transport Agent: get_bus_stops for bus_number={bus_number}")
    try:
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
                    "is_spot": stop.is_spot,
                    "latitude": stop.latitude,
                    "longitude": stop.longitude,
                }
                for stop in sorted(bus.stops, key=lambda s: s.stop_order)
            ]
        }
    except Exception as e:
        logger.exception(f"Transport Agent error in get_bus_stops: {e}")
        return {"error": f"Failed to fetch stops: {str(e)}", "stops": []}


def get_bus_schedule(db: Session, bus_number: str) -> Dict:
    logger.info(f"Transport Agent: get_bus_schedule for bus_number={bus_number}")
    try:
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
    except Exception as e:
        logger.exception(f"Transport Agent error in get_bus_schedule: {e}")
        return {"error": f"Failed to fetch schedules: {str(e)}", "schedules": []}


def predict_delay(db: Session, bus_number: str) -> Dict:
    """Exponential smoothing on historical delay data to predict today's delay."""
    logger.info(f"Transport Agent: predict_delay for bus_number={bus_number}")
    try:
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
    except Exception as e:
        logger.exception(f"Transport Agent error in predict_delay: {e}")
        return {
            "bus_number": bus_number,
            "predicted_delay_minutes": 0,
            "confidence": "Error",
            "message": f"Error in delay prediction: {str(e)}"
        }


def get_optimal_bus_route(db: Session, from_stop: str, to_stop: str) -> Dict:
    """Find optimal bus route between two stops using Dijkstra on stop graph."""
    logger.info(f"Transport Agent: get_optimal_bus_route from={from_stop} to={to_stop}")
    try:
        all_buses = db.query(Bus).filter(Bus.is_active == True).all()

        # Build graph: stop_name → [(cost, next_stop, bus_number)]
        graph: Dict[str, List] = {}
        for bus in all_buses:
            stops = sorted(bus.stops, key=lambda s: s.stop_order)
            for i in range(len(stops) - 1):
                src = stops[i].stop_name
                dst = stops[i + 1].stop_name
                cost = 15
                if src not in graph:
                    graph[src] = []
                if dst not in graph:
                    graph[dst] = []
                graph[src].append((cost, dst, bus.bus_number))
                graph[dst].append((cost, src, bus.bus_number))  # bidirectional

        if from_stop not in graph:
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
        pq = [(0, from_stop, [])]

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
    except Exception as e:
        logger.exception(f"Transport Agent error in get_optimal_bus_route: {e}")
        return {"error": f"Error finding route: {str(e)}"}


def get_seats_layout(db: Session, bus_id: int, travel_date: str) -> List[Dict]:
    logger.info(f"Transport Agent: get_seats_layout bus_id={bus_id} date={travel_date}")
    try:
        # Fetch confirmed bookings for this bus & date
        bookings = db.query(BusTicketBooking).filter(
            BusTicketBooking.bus_id == bus_id,
            BusTicketBooking.travel_date == travel_date,
            BusTicketBooking.status == "CONFIRMED"
        ).all()
        booked_seats = {b.seat_number for b in bookings}
        
        # Generate 50 seats layout (Rows 1-12: A,B,C,D; Row 13: A,B)
        layout = []
        for r in range(1, 13):
            for col in ["A", "B", "C", "D"]:
                seat_id = f"{r}{col}"
                layout.append({
                    "seat_number": seat_id,
                    "row": r,
                    "column": col,
                    "is_booked": seat_id in booked_seats
                })
        for col in ["A", "B"]:
            seat_id = f"13{col}"
            layout.append({
                "seat_number": seat_id,
                "row": 13,
                "column": col,
                "is_booked": seat_id in booked_seats
            })
        return layout
    except Exception as e:
        logger.exception(f"Transport Agent error in get_seats_layout: {e}")
        return []

def book_ticket(db: Session, student_id: str, student_name: str, hostel_block_room: str, 
                bus_id: int, seat_number: str, travel_date: str, destination_city: str, 
                boarding_point: str, drop_point: str, departure_time: str, contact_phone: str) -> Dict:
    logger.info(f"Transport Agent: book_ticket student_id={student_id} bus_id={bus_id} seat={seat_number} date={travel_date}")
    try:
        # Check availability
        existing = db.query(BusTicketBooking).filter(
            BusTicketBooking.bus_id == bus_id,
            BusTicketBooking.travel_date == travel_date,
            BusTicketBooking.seat_number == seat_number,
            BusTicketBooking.status == "CONFIRMED"
        ).first()
        if existing:
            return {"error": "Seat is already reserved by another passenger."}
            
        tkt_num = f"TKT-{datetime.now().strftime('%Y%m%d')}-{random.randint(1000, 9999)}"
        qr_data = f"TICKET:{tkt_num}:{student_id}:{seat_number}:{travel_date}"
        
        booking = BusTicketBooking(
            ticket_number=tkt_num,
            student_id=student_id,
            student_name=student_name,
            hostel_block_room=hostel_block_room,
            bus_id=bus_id,
            seat_number=seat_number,
            travel_date=travel_date,
            destination_city=destination_city,
            boarding_point=boarding_point,
            drop_point=drop_point,
            departure_time=departure_time,
            contact_phone=contact_phone,
            status="CONFIRMED",
            qr_code_data=qr_data
        )
        db.add(booking)
        db.commit()
        db.refresh(booking)
        
        return {
            "status": "Success",
            "ticket_number": tkt_num,
            "message": f"Seat {seat_number} reserved successfully! Ticket ID: {tkt_num}.",
            "booking": {
                "id": booking.id,
                "ticket_number": booking.ticket_number,
                "student_id": booking.student_id,
                "seat_number": booking.seat_number,
                "travel_date": booking.travel_date,
                "qr_code_data": booking.qr_code_data
            }
        }
    except Exception as e:
        logger.exception(f"Transport Agent error in book_ticket: {e}")
        return {"error": f"Failed to book ticket: {str(e)}"}

def get_student_tickets(db: Session, student_id: str) -> List[Dict]:
    logger.info(f"Transport Agent: get_student_tickets student_id={student_id}")
    try:
        bookings = db.query(BusTicketBooking).filter(
            BusTicketBooking.student_id == student_id
        ).order_by(BusTicketBooking.id.desc()).all()
        
        res = []
        for b in bookings:
            bus = db.query(Bus).filter(Bus.id == b.bus_id).first()
            bus_number = bus.bus_number if bus else "N/A"
            res.append({
                "id": b.id,
                "ticket_number": b.ticket_number,
                "student_id": b.student_id,
                "student_name": b.student_name,
                "hostel_block_room": b.hostel_block_room,
                "bus_id": b.bus_id,
                "bus_number": bus_number,
                "seat_number": b.seat_number,
                "travel_date": b.travel_date,
                "destination_city": b.destination_city,
                "boarding_point": b.boarding_point,
                "drop_point": b.drop_point,
                "departure_time": b.departure_time,
                "contact_phone": b.contact_phone,
                "status": b.status,
                "qr_code_data": b.qr_code_data
            })
        return res
    except Exception as e:
        logger.exception(f"Transport Agent error in get_student_tickets: {e}")
        return []

def cancel_ticket(db: Session, ticket_id: int) -> Dict:
    logger.info(f"Transport Agent: cancel_ticket ticket_id={ticket_id}")
    try:
        booking = db.query(BusTicketBooking).filter(BusTicketBooking.id == ticket_id).first()
        if not booking:
            return {"error": "Ticket reservation not found."}
        booking.status = "CANCELLED"
        db.commit()
        return {"status": "Success", "message": "Ticket reservation cancelled successfully."}
    except Exception as e:
        logger.exception(f"Transport Agent error in cancel_ticket: {e}")
        return {"error": f"Failed to cancel reservation: {str(e)}"}
