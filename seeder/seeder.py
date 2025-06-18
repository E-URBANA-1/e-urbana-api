import random
import requests
from datetime import datetime
from faker import Faker

fake = Faker()

API_URL = "http://localhost:3200"  
TIPOS = ['LED', 'Halógena', 'Incandescente','NULL']
ESTADOS = ['encendida', 'apagada', 'fallando','NULL']
FIRMWARES = ['v1.0.0', 'v1.2.3', 'v2.0.1','NULL']
ESTADOS_RED = ['estable', 'inestable', 'sin conexión','NULL']
RESPONSABLES = ['Carlos Rodríguez', 'Ana Gómez', 'Luis Pérez','NULL']


def generar_identificador(estado, ciudad, fecha, lat, lng, secuencial):
    dia = f"{fecha.day:02d}"
    mes = f"{fecha.month:02d}"
    lat_dos = str(int(abs(lat) * 100))[:2]
    lng_dos = str(int(abs(lng) * 100))[:2]
    return f"{estado.lower()}{ciudad.lower()}{dia}{mes}{lat_dos}{lng_dos}{secuencial:03d}"


def generar_luminaria(index, estado="pu", ciudad="pb"):
    lat = round(6.24 + random.uniform(-0.01, 0.01), 6)
    lng = round(-75.57 + random.uniform(-0.01, 0.01), 6)
    fecha_instalacion = fake.date_between(start_date='-2y', end_date='today')
    identificador = generar_identificador(estado, ciudad, fecha_instalacion, lat, lng, index)

    return {
        "identificador": identificador,
        "ubicacion": {
            "direccion": fake.address(),
            "coordenadas": {
                "lat": lat,
                "lng": lng
            }
        },
        "tipo": random.choice(TIPOS),
        "potencia_watts": random.choice([50, 75, 100, 150]),
        "altura_metros": round(random.uniform(6.0, 10.0), 2),
        "estado": random.choice(ESTADOS),
        "horarios": {
            "encendido": "18:00",
            "apagado": "06:00"
        },
        "consumo": {
            "actual_watts": round(random.uniform(40.0, 110.0), 2),
            "acumulado_kwh": {
                "dia": round(random.uniform(0.5, 2.0), 2),
                "semana": round(random.uniform(4.0, 14.0), 2),
                "mes": round(random.uniform(20.0, 60.0), 2)
            },
            "historial": [
                {
                    "fecha": fake.date_time_between(start_date='-5d', end_date='now').isoformat(),
                    "kwh": round(random.uniform(0.8, 1.6), 2)
                } for _ in range(5)
            ]
        },
        "sensores": {
            "luminosidad_lux": random.randint(50, 300),
            "movimiento": random.choice([True, False]),
            "temperatura_c": round(random.uniform(20.0, 35.0), 1),
            "humedad_pct": round(random.uniform(40.0, 80.0), 1)
        },
        "mantenimiento": {
            "ultima_revision": fake.date_between(start_date='-6mo', end_date='today').isoformat(),
            "ultima_reparacion": fake.date_between(start_date='-1y', end_date='-1mo').isoformat(),
            "estado_lampara": random.choice(["bueno", "regular", "malo"]),
            "notas": fake.sentence(),
            "responsable": random.choice(RESPONSABLES)
        },
        "conectividad": {
            "estado_red": random.choice(ESTADOS_RED),
            "latencia_ms": round(random.uniform(20, 100), 1),
            "firmware": random.choice(FIRMWARES)
        },
        "eficiencia": {
            "lumens_por_watt": round(random.uniform(90, 130), 2),
            "horas_funcionamiento_total": random.randint(500, 10000),
            "vida_util_restante_pct": round(random.uniform(30.0, 90.0), 1)
        },
        "registro": {
            "fecha_instalacion": fecha_instalacion.isoformat(),
            "creado_por": "admin_sistema"
        }
    }


def seed_luminarias_api(cantidad, estado="pu", ciudad="pb"):
    for i in range(1, cantidad + 1):
        luminaria = generar_luminaria(i, estado, ciudad)
        response = requests.post(API_URL, json=luminaria)
        if response.status_code in [200, 201]:
            print(f"Insertada  {luminaria['identificador']}")
        else:
            print(f"Error  {luminaria['identificador']}: {response.status_code} - {response.text}")


if __name__ == "__main__":
    cantidad = int(input("¿Cuántas luminarias deseas insertar? "))
    estado = input("Código de estado (2 letras, ej: pu): ").strip().lower()
    ciudad = input("Código de ciudad (2 letras, ej: pb): ").strip().lower()
    seed_luminarias_api(cantidad, estado, ciudad)
    print("completado")
