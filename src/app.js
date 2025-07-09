import express from 'express';
import morgan from 'morgan';
import cors from 'cors';
import { config } from 'dotenv';
config();

import luminariaRoutes from './routes/luminariaRoutes.js';

import swaggerJsdoc from 'swagger-jsdoc';
import swaggerUi from 'swagger-ui-express';
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

const swaggerOptions = {
  definition: {
    openapi: '3.0.0',
    info: {
      title: 'API E-Urbana',
      version: '1.0.0',
      description: 'API para la gestión de luminarias inteligentes',
    },
    servers: [
      { url: 'http://localhost:3200' }
    ],
  },
  apis: ['./src/routes/*.js'], 
};

const swaggerSpec = swaggerJsdoc(swaggerOptions);
app.use('/api-docs', swaggerUi.serve, swaggerUi.setup(swaggerSpec));

// rutas de API REST
app.use('/api/luminarias', luminariaRoutes);

export default app;
