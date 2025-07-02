// src/dao/luminariaDao.js
import Luminaria from '../models/luminariaModel.js';

const luminariaDAO = {};

/**
 * Devuelve todas las luminarias sin paginar.
 * Usar con precaución si hay millones de documentos.
 */
luminariaDAO.getAll = async () => {
  return await Luminaria.find().lean();
};

/**
 * Devuelve un bloque de luminarias paginadas.
 * @param {number} skip – cuántos documentos omitir
 * @param {number} limit – cuántos documentos traer
 */
luminariaDAO.getPaginated = async (skip = 0, limit = 1000) => {
  return await Luminaria.find()
    .skip(skip)
    .limit(limit)
    .lean();
};

/**
 * Cuenta el total de luminarias en la colección.
 */
luminariaDAO.countAll = async () => {
  return await Luminaria.countDocuments();
};

/**
 * Devuelve una luminaria por su identificador único.
 * @param {string} identificador
 */
luminariaDAO.getOne = async (identificador) => {
  return await Luminaria.findOne({ identificador }).lean();
};

/**
 * Inserta una nueva luminaria.
 * @param {Object} data – objeto con la estructura de luminaria
 * @returns {Object} – el documento insertado
 */
luminariaDAO.insertLuminaria = async (data) => {
  const doc = new Luminaria(data);
  const saved = await doc.save();
  return saved.toObject();
};

/**
 * Actualiza una luminaria por su identificador.
 * @param {string} identificador
 * @param {Object} data – campos a actualizar
 * @returns {boolean} – true si se encontró y actualizó
 */
luminariaDAO.updateLuminaria = async (identificador, data) => {
  const updated = await Luminaria.findOneAndUpdate(
    { identificador },
    data,
    { new: true }
  ).lean();
  return updated !== null;
};

/**
 * Elimina una luminaria por su identificador.
 * @param {string} identificador
 * @returns {boolean} – true si se eliminó
 */
luminariaDAO.deleteLuminaria = async (identificador) => {
  const deleted = await Luminaria.findOneAndDelete({ identificador });
  return deleted !== null;
};

/**
 * Inserta varias luminarias en lote.
 * @param {Array<Object>} docs – array de objetos luminaria
 * @returns {Array<Object>} – documentos insertados
 */
luminariaDAO.insertManyLuminarias = async (docs) => {
  return await Luminaria.insertMany(docs);
};

/**
 * Suma total de kWh del mes y horas de funcionamiento.
 */
luminariaDAO.getTotals = async () => {
  const [result = {}] = await Luminaria.aggregate([
    {
      $group: {
        _id: null,
        totalConsumo: { $sum: '$consumo.acumulado_kwh.mes' },
        totalHoras: { $sum: '$eficiencia.horas_funcionamiento_total' }
      }
    }
  ])
    .option({ allowDiskUse: true });
  return {
    totalConsumo: result.totalConsumo || 0,
    totalHoras: result.totalHoras || 0
  };
};

/**
 * Agrupa consumo por colonia (primera línea de la dirección).
 */
luminariaDAO.getConsumptionByColony = async () => {
  return await Luminaria.aggregate([
    {
      $project: {
        colonia: {
          $arrayElemAt: [
            { $split: ['$ubicacion.direccion', '\n'] },
            0
          ]
        },
        consumo: '$consumo.acumulado_kwh.mes'
      }
    },
    {
      $group: {
        _id: '$colonia',
        value: { $sum: '$consumo' }
      }
    },
    {
      $project: { _id: 0, name: '$_id', value: 1 }
    }
  ])
    .option({ allowDiskUse: true });
};

/**
 * Obtiene comparativo de consumo/gasto por mes
 * basado en el historial de cada luminaria.
 */
luminariaDAO.getMonthlyComparative = async () => {
  return await Luminaria.aggregate([
    { $unwind: '$consumo.historial' },
    {
      $group: {
        _id: {
          $dateToString: { format: '%b', date: '$consumo.historial.fecha' }
        },
        consumo: { $sum: '$consumo.historial.kwh' }
      }
    },
    {
      $project: {
        name: '$_id',
        consumo: 1,
        gasto: { $multiply: ['$consumo', 2.85] }
      }
    },
    {
      $sort: { name: -1 }  // Orden desc. de meses (Nov, Oct, Sep...)
    }
  ])
    .option({ allowDiskUse: true });
};

export default luminariaDAO;
