import express from "express";
import {
  getAllLuminarias,
  getOneLuminaria,
  insertLuminaria,
  updateLuminaria,
  deleteLuminaria
} from "../controllers/luminariaController.js";

const router = express.Router();

// Rutas para luminarias
router.get("/", getAllLuminarias); // Obtener todas
router.get("/:identificador", getOneLuminaria); // Obtener una por identificador
router.post("/", insertLuminaria); // Crear nueva
router.put("/:identificador", updateLuminaria); // Actualizar por identificador
router.delete("/:identificador", deleteLuminaria); // Eliminar por identificador

export default router;
