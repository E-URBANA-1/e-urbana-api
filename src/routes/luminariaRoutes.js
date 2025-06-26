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

// Rutas para luminarias
router.get("/", getAllLuminarias);
router.get("/:identificador", getOneLuminaria);
router.post("/", insertLuminaria);
router.post("/batch", insertLuminariasBatch);  
router.put("/:identificador", updateLuminaria);
router.delete("/:identificador", deleteLuminaria);

export default router;
