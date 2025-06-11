# 🌃 E. Urbana - API de Gestión de Luminarias Inteligentes

Esta API permite gestionar luminarias públicas para su monitoreo, mantenimiento y análisis inteligente en entornos urbanos. Desarrollada con Node.js, Express y MongoDB.

---

## 📦 Tecnologías

- Node.js
- Express.js
- MongoDB + Mongoose
- JavaScript ES Modules (ESM)

---

## 📂 Estructura del Proyecto

```
/models           → Esquemas de Mongoose
/dao              → Lógica de acceso a datos (Data Access Object)
/controllers      → Controladores para las rutas
/routes           → Definición de endpoints
index.js          → Configuración principal del servidor
```

---

## ⚙️ Instalación

1. Clona el repositorio:


2. Instala las dependencias:
   ```bash
   npm install
   ```

3. Configura la base de datos:
   - Crea un archivo `.env` y agrega tu URI de MongoDB:
     ```
     MONGODB_URI=mongodb://localhost:3200
     ```

4. Inicia el servidor:
   ```bash
   npm run dev
   ```

---

## 📡 Endpoints

### Base URL: `/`

| Método | Ruta                            | Descripción                               |
|--------|----------------------------------|-------------------------------------------|
| GET    | `/`                   | Obtiene todas las luminarias              |
| GET    | `/:identificador`    | Obtiene una luminaria por su identificador |
| POST   | `/`                   | Crea una nueva luminaria                  |
| PUT    | `/:identificador`    | Actualiza una luminaria                   |
| DELETE | `/:identificador`    | Elimina una luminaria                     |

---

## 🧾 Ejemplo de Documento (Modelo Luminaria)

```json
[
    {
        "ubicacion": {
            "coordenadas": {
                "lat": 19.0433,
                "lng": -98.1982
            },
            "direccion": "Av. Reforma 123, Puebla, México"
        },
        "horarios": {
            "encendido": "18:30",
            "apagado": "06:00"
        },
        "consumo": {
            "acumulado_kwh": {
                "dia": 1.8,
                "semana": 12.6,
                "mes": 55.2
            },
            "actual_watts": 95,
            "historial": [
                {
                    "fecha": "2025-06-10T23:00:00.000Z",
                    "kwh": 1.7,
                    "_id": "68499b906623c7f3c3bbaf1d"
                },
                {
                    "fecha": "2025-06-09T23:00:00.000Z",
                    "kwh": 1.9,
                    "_id": "68499b906623c7f3c3bbaf1e"
                }
            ]
        },
        "sensores": {
            "luminosidad_lux": 150,
            "movimiento": true,
            "temperatura_c": 28.5,
            "humedad_pct": 62
        },
        "mantenimiento": {
            "ultima_revision": "2025-06-01",
            "ultima_reparacion": "2025-05-15",
            "estado_lampara": "óptimo",
            "notas": "Sin observaciones",
            "responsable": "Juan Pérez"
        },
        "conectividad": {
            "estado_red": "estable",
            "latencia_ms": 25,
            "firmware": "v1.3.5"
        },
        "eficiencia": {
            "lumens_por_watt": 120,
            "horas_funcionamiento_total": 3200,
            "vida_util_restante_pct": 85
        },
        "registro": {
            "fecha_instalacion": "2023-10-15",
            "creado_por": "admin_system"
        },
        "_id": "68499b906623c7f3c3bbaf1c",
        "identificador": "LUM-001-AZ",
        "tipo": "LED",
        "potencia_watts": 100,
        "altura_metros": 8,
        "estado": "encendida",
        "createdAt": "2025-06-10T21:30:00.000Z",
        "updatedAt": "2025-06-10T21:30:00.000Z"
    }
]

```

---

## 🔧 Funcionalidades Futuras

- 🤖 Integración de IA para predicción de mantenimiento
- 🔔 Notificaciones automáticas por sobreconsumo

---

## 👤 Autor

Desarrollado por [Luis Marquez](https://github.com/luisivmaraz)
