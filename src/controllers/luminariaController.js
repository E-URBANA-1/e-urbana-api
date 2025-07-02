// src/controllers/luminariaController.js
import luminariaDAO from '../dao/luminariaDao.js';
import { io } from '../server.js';  // tu instancia de Socket.IO

// Obtener todas las luminarias (paginated)
export const getAllLuminarias = async (req, res) => {
  const page  = parseInt(req.query.page)  || 1;
  const limit = parseInt(req.query.limit) || 1000;
  const skip  = (page - 1) * limit;

  try {
    const [ data, total ] = await Promise.all([
      luminariaDAO.getPaginated(skip, limit),
      luminariaDAO.countAll()
    ]);

    res.json({
      total,
      page,
      limit,
      pages: Math.ceil(total / limit),
      data
    });
  } catch (err) {
    console.error('getAllLuminarias error:', err);
    res.status(500).json({ status: 'Server unavailable' });
  }
};

// Obtener una luminaria por identificador
export const getOneLuminaria = async (req, res) => {
  try {
    const luminaria = await luminariaDAO.getOne(req.params.identificador);
    if (!luminaria) {
      return res.status(404).json({ status: 'Luminaria not found' });
    }
    res.json(luminaria);
  } catch (err) {
    console.error('getOneLuminaria error:', err);
    res.status(500).json({ status: 'Server unavailable' });
  }
};

// Insertar una luminaria
export const insertLuminaria = async (req, res) => {
  try {
    await luminariaDAO.insertLuminaria(req.body);
    io.emit('luminariaAdded', req.body);
    res.status(201).json({ status: 'Luminaria saved' });
  } catch (err) {
    console.error('insertLuminaria error:', err);
    res.status(500).json({ status: 'Server unavailable' });
  }
};

// Insertar múltiples luminarias en lote (batch)
export const insertLuminariasBatch = async (req, res) => {
  const arr = req.body;
  if (!Array.isArray(arr)) {
    return res.status(400).json({ status: 'Bad request: se esperaba un array de luminarias' });
  }

  try {
    const inserted = await luminariaDAO.insertManyLuminarias(arr);
    io.emit('luminariasBatchAdded', inserted);
    res.status(201).json({ status: 'Luminarias insertadas', cantidad: inserted.length });
  } catch (err) {
    console.error('insertLuminariasBatch error:', err);
    res.status(500).json({ status: 'Error al insertar luminarias' });
  }
};

// Actualizar una luminaria por identificador
export const updateLuminaria = async (req, res) => {
  try {
    const ok = await luminariaDAO.updateLuminaria(req.params.identificador, req.body);
    if (!ok) {
      return res.status(404).json({ status: 'Luminaria not found' });
    }
    const updated = { identificador: req.params.identificador, ...req.body };
    io.emit('luminariaUpdated', updated);
    res.json({ status: 'Luminaria updated' });
  } catch (err) {
    console.error('updateLuminaria error:', err);
    res.status(500).json({ status: 'Server unavailable' });
  }
};

// Eliminar una luminaria por identificador
export const deleteLuminaria = async (req, res) => {
  try {
    const ok = await luminariaDAO.deleteLuminaria(req.params.identificador);
    if (!ok) {
      return res.status(404).json({ status: 'Luminaria not found' });
    }
    io.emit('luminariaDeleted', req.params.identificador);
    res.json({ status: 'Luminaria deleted' });
  } catch (err) {
    console.error('deleteLuminaria error:', err);
    res.status(500).json({ status: 'Server unavailable' });
  }
};
