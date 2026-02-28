import json
import random
from faker import Faker
from datetime import datetime, timedelta

fake = Faker('es_ES')

# 3 Hoteles
hotels = [
    {"id": "hotel_01", "name": "Hotel Caribe Plaza", "city": "Cartagena"},
    {"id": "hotel_02", "name": "Hotel Santo Domingo", "city": "Santo Domingo"},
    {"id": "hotel_03", "name": "Hotel Punta Cana Resort", "city": "Punta Cana"},
]

# Tipos de habitación
room_types = ["Simple", "Doble", "Suite", "Familiar"]

# Canales de reserva
channels = ["Booking.com", "Expedia", "Directo", "Agencia", "Airbnb"]

# Estados de reserva
statuses = ["confirmed", "cancelled", "checked_in", "checked_out"]

def generate_reservations(hotel, num_records=5000):
    reservations = []
    start_date = datetime(2019, 1, 1)

    for i in range(num_records):
        check_in = start_date + timedelta(days=random.randint(0, 365*5))
        check_out = check_in + timedelta(days=random.randint(1, 14))
        rate = round(random.uniform(50, 500), 2)
        nights = (check_out - check_in).days

        reservation = {
            "reservation_id": f"{hotel['id']}_RES_{i+1:05d}",
            "hotel_id": hotel["id"],
            "hotel_name": hotel["name"],
            "city": hotel["city"],
            "guest_name": fake.name(),
            "guest_email": fake.email(),
            "guest_nationality": fake.country(),
            "room_type": random.choice(room_types),
            "channel": random.choice(channels),
            "status": random.choice(statuses),
            "check_in": check_in.strftime("%Y-%m-%d"),
            "check_out": check_out.strftime("%Y-%m-%d"),
            "nights": nights,
            "rate_per_night": rate,
            "total_amount": round(rate * nights, 2),
            "created_at": fake.date_time_between(start_date="-5y", end_date="now").strftime("%Y-%m-%d %H:%M:%S")
        }
        reservations.append(reservation)
    return reservations

# Generar datos para los 3 hoteles
all_reservations = []
for hotel in hotels:
    all_reservations.extend(generate_reservations(hotel, num_records=5000))

# Guardar en JSON
output_path = "../data/reservations_raw.json"
with open(output_path, "w", encoding="utf-8") as f:
    json.dump(all_reservations, f, ensure_ascii=False, indent=2)

print(f"✅ {len(all_reservations)} reservaciones generadas y guardadas en {output_path}")