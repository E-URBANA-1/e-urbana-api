import express from "express";
import {
  getAllLuminarias,
  getOneLuminaria,
  insertLuminaria,
  insertLuminariasBatch,
  updateLuminaria,
  deleteLuminaria
} from "../controllers/luminariaController.js";

const router = express.Router();

/**
 * @swagger
 * tags:
 *   name: Luminarias
 *   description: Endpoints para gestión de luminarias
 */

/**
 * @swagger
 * /api/luminarias:
 *   get:
 *     summary: Obtener todas las luminarias (paginadas)
 *     tags: [Luminarias]
 *     parameters:
 *       - in: query
 *         name: page
 *         schema:
 *           type: integer
 *         description: Número de página (por defecto 1)
 *       - in: query
 *         name: limit
 *         schema:
 *           type: integer
 *         description: Cantidad de resultados por página (por defecto 1000)
 *     responses:
 *       200:
 *         description: Lista de luminarias paginadas
 */
router.get("/", getAllLuminarias);

/**
 * @swagger
 * /api/luminarias/{identificador}:
 *   get:
 *     summary: Obtener una luminaria por identificador
 *     tags: [Luminarias]
 *     parameters:
 *       - in: path
 *         name: identificador
 *         required: true
 *         schema:
 *           type: string
 *         description: Identificador de la luminaria
 *     responses:
 *       200:
 *         description: Datos de la luminaria
 *       404:
 *         description: Luminaria no encontrada
 */
router.get("/:identificador", getOneLuminaria);

/**
 * @swagger
 * /api/luminarias:
 *   post:
 *     summary: Insertar una nueva luminaria
 *     tags: [Luminarias]
 *     requestBody:
 *       required: true
 *       content:
 *         application/json:
 *           schema:
 *             type: object
 *             description: Datos de la luminaria a insertar
 *     responses:
 *       201:
 *         description: Luminaria guardada exitosamente
 *       500:
 *         description: Error del servidor
 */
router.post("/", insertLuminaria);

/**
 * @swagger
 * /api/luminarias/batch:
 *   post:
 *     summary: Insertar múltiples luminarias en lote
 *     tags: [Luminarias]
 *     requestBody:
 *       required: true
 *       content:
 *         application/json:
 *           schema:
 *             type: array
 *             items:
 *               type: object
 *               description: Datos de una luminaria
 *     responses:
 *       201:
 *         description: Luminarias insertadas exitosamente
 *       400:
 *         description: Solicitud inválida
 *       500:
 *         description: Error del servidor
 */
router.post("/batch", insertLuminariasBatch);

/**
 * @swagger
 * /api/luminarias/{identificador}:
 *   put:
 *     summary: Actualizar una luminaria por identificador
 *     tags: [Luminarias]
 *     parameters:
 *       - in: path
 *         name: identificador
 *         required: true
 *         schema:
 *           type: string
 *         description: Identificador de la luminaria
 *     requestBody:
 *       required: true
 *       content:
 *         application/json:
 *           schema:
 *             type: object
 *             description: Datos a actualizar
 *     responses:
 *       200:
 *         description: Luminaria actualizada
 *       404:
 *         description: Luminaria no encontrada
 *       500:
 *         description: Error del servidor
 */
router.put("/:identificador", updateLuminaria);

/**
 * @swagger
 * /api/luminarias/{identificador}:
 *   delete:
 *     summary: Eliminar una luminaria por identificador
 *     tags: [Luminarias]
 *     parameters:
 *       - in: path
 *         name: identificador
 *         required: true
 *         schema:
 *           type: string
 *         description: Identificador de la luminaria
 *     responses:
 *       200:
 *         description: Luminaria eliminada
 *       404:
 *         description: Luminaria no encontrada
 *       500:
 *         description: Error del servidor
 */
router.delete("/:identificador", deleteLuminaria);

export default router;
