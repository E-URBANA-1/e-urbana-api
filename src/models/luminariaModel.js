import { Schema, model } from "mongoose";

const luminariaSchema = new Schema({
  identificador: {
    type: String,
    unique: true,
    required: true
  },
  ubicacion: {
    direccion: String,
    coordenadas: {
      lat: Number,
      lng: Number
    }
  },
  tipo: String, 
  potencia_watts: Number,
  altura_metros: Number,
  estado: {
    type: String,
    enum: ['encendida', 'apagada', 'fallando'],
    default: 'apagada'
  },
  horarios: {
    encendido: String, 
    apagado: String    
  },
  consumo: {
    actual_watts: Number,
    acumulado_kwh: {
      dia: Number,
      semana: Number,
      mes: Number
    },
    historial: [
      {
        fecha: Date,  
        kwh: Number
      }
    ]
  },
  sensores: {
    luminosidad_lux: Number,
    movimiento: Boolean,
    temperatura_c: Number,
    humedad_pct: Number
  },
  mantenimiento: {
    ultima_revision: String,
    ultima_reparacion: String,
    estado_lampara: String,
    notas: String,
    responsable: String
  },
  conectividad: {
    estado_red: String,
    latencia_ms: Number,
    firmware: String
  },
  eficiencia: {
    lumens_por_watt: Number,
    horas_funcionamiento_total: Number,
    vida_util_restante_pct: Number
  },
  registro: {
    fecha_instalacion: String,
    creado_por: String
  }
}, {
  timestamps: true,
  versionKey: false
});

export default model('luminarias', luminariaSchema);
