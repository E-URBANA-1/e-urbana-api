import random
import requests
from datetime import datetime
from faker import Faker
from tqdm import tqdm

fake = Faker()

API_URL = "http://localhost:3200"   
BATCH_SIZE = 1000

TIPOS = ['LED', 'Halógena', 'Incandescente', 'NULL']
ESTADOS = ['encendida', 'apagada', 'fallando', 'NULL']
FIRMWARES = ['v1.0.0', 'v1.2.3', 'v2.0.1', 'NULL']
ESTADOS_RED = ['estable', 'inestable', 'sin conexión', 'NULL']

ESTADOS_MX = {
    'Ags': ['ags'], 'BC': ['tj', 'mc'], 'BCS': ['lpz'], 'Camp': ['cam'],
    'Coah': ['slc', 'tor'], 'Col': ['col'], 'Chis': ['tuxt'], 'Chih': ['chih', 'ju'],
    'CDMX': ['cx'], 'Dgo': ['dgo'], 'Gto': ['leo', 'irapuato'], 'Gro': ['aca', 'chil'],
    'Hgo': ['pach'], 'Jal': ['gd', 'zap'], 'Méx': ['tol', 'nez'], 'Mich': ['morelia'],
    'Mor': ['cuernavaca'], 'Nay': ['tep'], 'NL': ['mty'], 'Oax': ['oax'],
    'Qro': ['qro'], 'QR': ['cancun', 'chetumal'], 'SLP': ['slp'], 'Sin': ['cul', 'mochi'],
    'Son': ['herm', 'nog'], 'Tab': ['villah'], 'Tamps': ['tampico', 'reynosa'],
    'Tlax': ['tlax'], 'Ver': ['ver', 'coatza'], 'Yuc': ['mda'], 'Zac': ['zac']
}

RESPONSABLES = [
    "NULL", "Juan Pérez", "María González", "José Hernández", "Ana Martínez", "Luis López",
    "Laura Rodríguez", "Carlos Sánchez", "Sofía Ramírez", "Miguel Torres", "Lucía Flores"
]

def generar_identificador(estado, ciudad, fecha, lat, lng, secuencial):
    dia = f"{fecha.day:02d}"
    mes = f"{fecha.month:02d}"
    lat_dos = str(int(abs(lat) * 100))[:2]
    lng_dos = str(int(abs(lng) * 100))[:2]
    return f"{estado.lower()}{ciudad.lower()}{dia}{mes}{lat_dos}{lng_dos}{secuencial:03d}"

def generar_luminaria(index, estado, ciudad):
    lat = round(19.0 + random.uniform(-5, 5), 6)
    lng = round(-99.0 + random.uniform(-5, 5), 6)
    fecha_instalacion = fake.date_between(start_date='-2y', end_date='today')
    identificador = generar_identificador(estado, ciudad, fecha_instalacion, lat, lng, index)

    return {
        "identificador": identificador,
        "ubicacion": {
            "direccion": fake.address(),
            "coordenadas": { "lat": lat, "lng": lng }
        },
        "tipo": random.choice(TIPOS),
        "potencia_watts": random.choice([50, 75, 100, 150]),
        "altura_metros": round(random.uniform(6.0, 10.0), 2),
        "estado": random.choice(ESTADOS),
        "horarios": { "encendido": "18:00", "apagado": "06:00" },
        "consumo": {
            "actual_watts": round(random.uniform(40.0, 110.0), 2),
            "acumulado_kwh": {
                "dia": round(random.uniform(0.5, 2.0), 2),
                "semana": round(random.uniform(4.0, 14.0), 2),
                "mes": round(random.uniform(20.0, 60.0), 2)
            },
            "historial": [
                { "fecha": fake.date_time_between(start_date='-5d', end_date='now').isoformat(), "kwh": round(random.uniform(0.8, 1.6), 2) }
                for _ in range(5)
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

def seed_luminarias_api(cantidad_total):
    luminarias_batch = []
    index = 1

    for _ in tqdm(range(cantidad_total), desc="Insertando luminarias"):
        estado_abbr, ciudades = random.choice(list(ESTADOS_MX.items()))
        ciudad_abbr = random.choice(ciudades)
        luminaria = generar_luminaria(index, estado_abbr, ciudad_abbr)
        luminarias_batch.append(luminaria)
        index += 1

        if len(luminarias_batch) >= BATCH_SIZE or index > cantidad_total:
            try:
                response = requests.post(f"{API_URL}/batch", json=luminarias_batch)
                if response.status_code not in [200, 201]:
                    print(f"\n❌ Error en lote: {response.status_code} - {response.text}")
                luminarias_batch = []
            except Exception as e:
                print(f"\n🚨 Excepción en lote: {str(e)}")

if __name__ == "__main__":
    cantidad = int(input("¿Cuántas luminarias deseas insertar? "))
    seed_luminarias_api(cantidad)
    print("✅ Proceso completado")
