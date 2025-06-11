import express from 'express';
import morgan from 'morgan';
import { config } from "dotenv";
config();
import luminariaRoutes from './routes/luminariaRoutes.js';

const app = express();

// configuración
app.set('view engine', 'ejs');

// middlewares
app.use(express.json());
app.use(express.urlencoded({ extended: false }));
app.use(morgan('dev'));
app.use('', luminariaRoutes); // Cambiado a utilizar las rutas de luminarias
export default app;

