import random
import requests
from datetime import datetime
from faker import Faker
from tqdm import tqdm
from concurrent.futures import ThreadPoolExecutor

fake = Faker()

API_URL = "http://localhost:3200/batch"
TOTAL = 100000   
BATCH_SIZE = 10000
NUM_THREADS = 12


ESTADOS_MX = {
    'Ags': ['ags'], 'BC': ['tj', 'mc'], 'BCS': ['lpz'], 'Camp': ['cam'],
    'Coah': ['slc', 'tor'], 'Col': ['col'], 'Chis': ['tuxt'], 'Chih': ['chih', 'ju'],
    'CDMX': ['cx'], 'Dgo': ['dgo'], 'Gto': ['leo', 'ira'], 'Gro': ['aca', 'chil'],
    'Hgo': ['pach'], 'Jal': ['gd', 'zap'], 'Méx': ['tol', 'nez'], 'Mich': ['morelia'],
    'Mor': ['cuernavaca'], 'Nay': ['tep'], 'NL': ['mty'], 'Oax': ['oax'],
    'Qro': ['qro'], 'QR': ['cancun', 'chetumal'], 'SLP': ['slp'], 'Sin': ['cul', 'mochi'],
    'Son': ['herm', 'nog'], 'Tab': ['villah'], 'Tamps': ['tampico', 'reynosa'],
    'Tlax': ['tlax'], 'Ver': ['ver', 'coatza'], 'Yuc': ['mda'], 'Zac': ['zac']
}

TIPOS = ['LED', 'Halógena', 'Incandescente']
ESTADOS = ['encendida', 'apagada', 'fallando']
FIRMWARES = ['v1.0.0', 'v1.2.3', 'v2.0.1']
ESTADOS_RED = ['estable', 'inestable', 'sin conexión']
RESPONSABLES = [
  "Juan Pérez", "María González", "José Hernández", "Ana Martínez", "Luis López",
  "Laura Rodríguez", "Carlos Sánchez", "Sofía Ramírez", "Miguel Torres", "Lucía Flores",
  "Diego Morales", "Camila Reyes", "Fernando Cruz", "Valeria Ortiz", "Javier Castillo",
  "Paola Mendoza", "Andrés Romero", "Fernanda Vargas", "Emilio Herrera", "Daniela Ríos",
  "Alejandro Navarro", "Isabel Guzmán", "Ricardo Domínguez", "Gabriela Aguilar", "Eduardo Salinas",
  "Diana Cordero", "Manuel Pacheco", "Andrea Cabrera", "Raúl Jiménez", "Patricia Soto",
  "Héctor Carrillo", "Monserrat Peña", "Francisco Vázquez", "Mariana Lozano", "Marco Camacho",
  "Daniela Padilla", "Iván Pineda", "Fátima Gallardo", "Óscar Arias", "Regina Escobar",
  "Ramón Cortés", "Brenda Palma", "Ernesto León", "Jimena Treviño", "Víctor Fuentes",
  "Ariadna Meza", "Roberto Chávez", "Renata Luna", "Ángel Olvera", "Karina Godínez",
  "Alonso Becerra", "Itzel Quiroz", "Sebastián Tapia", "Vanessa Benítez", "Tomás Rangel",
  "Natalia Valdez", "Mauricio Bravo", "Ximena Serrano", "Cristian Calderón", "Leticia Mena",
  "Elías Acosta", "Zaira Medina", "Gustavo Barrera", "Tania Duarte", "Armando Villegas",
  "Jessica Rueda", "Leonardo Beltrán", "Rocío Solís", "Abel Márquez", "Lorena Espinosa",
  "Bruno Téllez", "Alejandra Cuevas", "Isaac Sepúlveda", "Daniela Figueroa", "Jonathan Lara",
  "Mónica Escamilla", "Adrián Arce", "Marisol Ledezma", "Matías Castañeda", "Perla Zamora",
  "Guillermo Barajas", "Estefanía Murillo", "Jorge Saucedo", "Cynthia Manríquez", "Kevin Castaño",
  "Aranza Bermúdez", "Rodrigo Villanueva", "Julia Tinoco", "Maximiliano Zúñiga", "Rebeca Lozoya",
  "Jaime Sandoval", "Dafne Castañón", "Ulises Mondragón", "Melina Rojo", "Saúl Valenzuela",
  "Claudia Puga", "Benjamín Galindo", "Lilia Bustos", "Mario Cárdenas", "Elena Llamas"
]

def generar_identificador(estado, ciudad, fecha, lat, lng, sec):
    lat_dos = str(int(abs(lat) * 100))[:2]
    lng_dos = str(int(abs(lng) * 100))[:2]
    return f"{estado.lower()}{ciudad.lower()}{fecha.day:02d}{fecha.month:02d}{lat_dos}{lng_dos}{sec:03d}"

def generar_luminaria(index):
    estado, ciudades = random.choice(list(ESTADOS_MX.items()))
    ciudad = random.choice(ciudades)
    lat = round(19 + random.uniform(-5, 5), 6)
    lng = round(-99 + random.uniform(-5, 5), 6)
    fecha = fake.date_between(start_date='-2y', end_date='today')

    return {
        "identificador": generar_identificador(estado, ciudad, fecha, lat, lng, index),
        "ubicacion": {
            "direccion": fake.address(),
            "coordenadas": {"lat": lat, "lng": lng}
        },
        "tipo": random.choice(TIPOS),
        "potencia_watts": random.choice([50, 75, 100, 150]),
        "altura_metros": round(random.uniform(6.0, 10.0), 2),
        "estado": random.choice(ESTADOS),
        "horarios": {"encendido": "18:00", "apagado": "06:00"},
        "consumo": {
            "actual_watts": round(random.uniform(40.0, 110.0), 2),
            "acumulado_kwh": {
                "dia": round(random.uniform(0.5, 2.0), 2),
                "semana": round(random.uniform(4.0, 14.0), 2),
                "mes": round(random.uniform(20.0, 60.0), 2)
            },
            "historial": [
                {"fecha": fake.date_time_between(start_date='-5d', end_date='now').isoformat(),
                 "kwh": round(random.uniform(0.8, 1.6), 2)}
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
            "fecha_instalacion": fecha.isoformat(),
            "creado_por": "admin_sistema"
        }
    }

def enviar_batch(batch):
    try:
        r = requests.post(API_URL, json=batch)
        if r.status_code not in [200, 201]:
            print(f"\n Error: {r.status_code} - {r.text}")
    except Exception as e:
        print(f"\n Error en envío: {e}")

def generar_y_enviar_lotes():
    with ThreadPoolExecutor(max_workers=NUM_THREADS) as executor:
        tasks = []
        idx = 1
        for _ in tqdm(range(TOTAL // BATCH_SIZE), desc="Enviando luminarias"):
            batch = [generar_luminaria(idx + i) for i in range(BATCH_SIZE)]
            idx += BATCH_SIZE
            tasks.append(executor.submit(enviar_batch, batch))
        for t in tasks:
            t.result()

if __name__ == "__main__":
    generar_y_enviar_lotes()
    print("\n Inserción completada")
