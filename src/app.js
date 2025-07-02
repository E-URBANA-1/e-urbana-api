import express from 'express';
import morgan from 'morgan';
import cors from 'cors';
import { config } from 'dotenv';
config();

import luminariaRoutes from './routes/luminariaRoutes.js';

const app = express();

// — Habilita CORS para tu front en Vite (puerto 5173)
app.use(cors({
  origin: 'http://localhost:5173',
  methods: ['GET','POST','PUT','DELETE']
}));

// configuración
app.set('view engine', 'ejs');

// middlewares
app.use(express.json({ limit: '100mb' }));
app.use(express.urlencoded({ extended: false }));
app.use(morgan('dev'));

// rutas de API REST
app.use('/api/luminarias', luminariaRoutes);

export default app;
