import { config } from 'dotenv';
config();  // carga las vars de .env

import mongoose from 'mongoose';

const uri = process.env.CONECTION_DB;
if (!uri) {
  console.error('❌ Falta CONECTION_DB en .env');
  process.exit(1);
}

console.log('Intentando conectar a la base de datos...');
mongoose
  .connect(uri)  // sin opciones deprecadas
  .then(() => console.log('✅ Database connected'))
  .catch(err => console.error('❌ Error conectando a la base de datos:', err));
