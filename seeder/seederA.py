import random
import requests
from datetime import datetime
from faker import Faker

fake = Faker()

API_URL = "http://localhost:3200/api/luminarias"

# Distribuciones con pesos realistas
TIPOS = ['LED', 'Halógena', 'Incandescente']
PESOS_TIPOS = [0.7, 0.2, 0.1]

ESTADOS = ['encendida', 'apagada', 'fallando']
PESOS_ESTADOS = [0.6, 0.3, 0.1]

FIRMWARES = ['v1.0.0', 'v1.2.3', 'v2.0.1']
PESOS_FIRMWARES = [0.5, 0.3, 0.2]

ESTADOS_RED = ['estable', 'inestable', 'sin conexión']
PESOS_RED = [0.8, 0.15, 0.05]

RESPONSABLES = [
    "Juan Pérez", "María González", "José Hernández", "Ana Martínez", "Luis López",
    "Laura Rodríguez", "Carlos Sánchez", "Sofía Ramírez", "Miguel Torres", "Lucía Flores"
]

def pick_weighted(choices, weights):
    return random.choices(choices, weights)[0]

def maybe_include(p=0.8):
    return random.random() < p

def generar_identificador(estado, ciudad, fecha, lat, lng, seq):
    return (
        f"{estado}{ciudad}"
        f"{fecha.day:02d}{fecha.month:02d}"
        f"{str(int(abs(lat)*100))[:2]}{str(int(abs(lng)*100))[:2]}"
        f"{seq:03d}"
    )

def generar_luminaria(idx, estado="pu", ciudad="pb"):
    lat = round(6.24 + random.uniform(-0.01, 0.01), 6)
    lng = round(-75.57 + random.uniform(-0.01, 0.01), 6)
    fecha = fake.date_between(start_date='-2y', end_date='today')
    ident = generar_identificador(estado, ciudad, fecha, lat, lng, idx)

    lum = {
        "identificador": ident,
        "ubicacion": {
            "direccion": fake.address(),
            "coordenadas": {"lat": lat, "lng": lng}
        },
        "tipo": pick_weighted(TIPOS, PESOS_TIPOS),
        "potencia_watts": random.choice([50, 75, 100, 150]),
        "altura_metros": round(random.uniform(6.0, 10.0), 2),
        "estado": pick_weighted(ESTADOS, PESOS_ESTADOS),
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
            # historial a veces vacío o incompleto
            "historial": (
                [{
                    "fecha": fake.date_time_between(start_date='-5d', end_date='now').isoformat(),
                    "kwh": round(random.uniform(0.8, 1.6), 2)
                } for _ in range(random.randint(0,5))]
                if maybe_include(0.8)
                else []
            )
        },
        "sensores": {
            "luminosidad_lux": random.randint(50, 300),
            "movimiento": random.choice([True, False]),
            "temperatura_c": round(random.uniform(20.0, 35.0), 1),
            "humedad_pct": round(random.uniform(40.0, 80.0), 1)
        },
        "mantenimiento": {},
        "conectividad": {},
        "eficiencia": {},
        "registro": {}
    }

    # mantenimiento: a veces falta entero, a veces responsable vacío
    if maybe_include(0.9):
        lum["mantenimiento"]["ultima_revision"] = fake.date_between(start_date='-6mo', end_date='today').isoformat()
    if maybe_include(0.7):
        lum["mantenimiento"]["ultima_reparacion"] = fake.date_between(start_date='-1y', end_date='-1mo').isoformat()
    if maybe_include(0.95):
        lum["mantenimiento"]["estado_lampara"] = pick_weighted(["bueno","regular","malo"], [0.7,0.2,0.1])
    if maybe_include(0.5):
        lum["mantenimiento"]["notas"] = fake.sentence()
    # responsable poco frecuente
    if maybe_include(0.4):
        lum["mantenimiento"]["responsable"] = random.choice(RESPONSABLES)

    # conectividad
    if maybe_include(0.95):
        lum["conectividad"]["estado_red"] = pick_weighted(ESTADOS_RED, PESOS_RED)
    if maybe_include(0.8):
        lum["conectividad"]["latencia_ms"] = round(random.uniform(20, 100), 1)
    if maybe_include(0.7):
        lum["conectividad"]["firmware"] = pick_weighted(FIRMWARES, PESOS_FIRMWARES)

    # eficiencia: siempre algo
    lum["eficiencia"] = {
        "lumens_por_watt": round(random.uniform(90, 130), 2),
        "horas_funcionamiento_total": random.randint(500, 10000),
        "vida_util_restante_pct": round(random.uniform(30.0, 90.0), 1)
    }

    # registro: fecha siempre, creado_por a veces omitido
    lum["registro"]["fecha_instalacion"] = fecha.isoformat()
    if maybe_include(0.75):
        lum["registro"]["creado_por"] = "admin_sistema"

    return lum

def seed_luminarias_api(cantidad, estado="pu", ciudad="pb"):
    for i in range(1, cantidad + 1):
        data = generar_luminaria(i, estado.lower(), ciudad.lower())
        resp = requests.post(API_URL, json=data)
        if resp.status_code in (200, 201):
            print(f"Insertada {data['identificador']}")
        else:
            print(f"Error {data['identificador']}: {resp.status_code} – {resp.text}")

if __name__ == "__main__":
    n = int(input("¿Cuántas luminarias deseas insertar? "))
    e = input("Código de estado (2 letras, ej: pu): ")
    c = input("Código de ciudad (2 letras, ej: pb): ")
    seed_luminarias_api(n, e, c)
    print("¡Completado!")
