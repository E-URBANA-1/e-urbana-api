import './database.js';            // 1) Conexión a MongoDB
import app from './app.js';        // 2) Express + rutas REST
import http from 'http';
import { Server as IOServer } from 'socket.io';
import luminariaDAO from './dao/luminariaDao.js';

const PORT = process.env.SERVER_PORT || 3200;

// 3) Crear servidor HTTP
const server = http.createServer(app);

// 4) Levantar Socket.IO con CORS para tu front en Vite (5173)
export const io = new IOServer(server, {
  cors: {
    origin: 'http://localhost:5173',
    methods: ['GET','POST','PUT','DELETE']
  }
});

io.on('connection', async socket => {
  console.log('WS conectado:', socket.id);
  try {
    // Emite sólo los resúmenes (totales, por colonia y comparativo)
    const totals      = await luminariaDAO.getTotals();
    const byColony    = await luminariaDAO.getConsumptionByColony();
    const comparative = await luminariaDAO.getMonthlyComparative();
    socket.emit('initialData', { totals, byColony, comparative });
  } catch (err) {
    console.error('Error enviando initialData:', err);
    socket.emit('initialDataError', { message: err.message });
  }
});

// 5) Arrancar servidor en el puerto configurado
server.listen(PORT, () => {
  console.log(`API + WS escuchando en http://localhost:${PORT}`);
});
