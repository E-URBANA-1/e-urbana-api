import luminariaDAO from "../dao/luminariaDao.js";

const C = console.log.bind(console.log);

// Obtener todas las luminarias
export const getAllLuminarias = async (req, res) => {
    const page = parseInt(req.query.page) || 1;
    const limit = parseInt(req.query.limit) || 1000;
    const skip = (page - 1) * limit;

    try {
        const [data, total] = await Promise.all([
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
        console.error(err);
        res.status(500).json({ status: "Server unavailable" });
    }
};


// Obtener una luminaria por identificador
export const getOneLuminaria = (req, res) => {
    luminariaDAO.getOne(req.params.identificador)
        .then(result => {
            if (result) {
                res.json(result);
            } else {
                res.status(404).json({ status: "Luminaria not found" });
            }
        })
        .catch(err => {
            console.error(err);
            res.status(500).json({ status: "Server unavailable" });
        });
};

// Insertar una luminaria
export const insertLuminaria = (req, res) => {
    luminariaDAO.insertLuminaria(req.body)
        .then(result => {
            if (result) {
                res.status(201).json({ status: "Luminaria saved" });
            }
        })
        .catch(err => {
            console.error(err);
            res.status(500).json({ status: "Server unavailable" });
        });
};

// Actualizar una luminaria por identificador
export const updateLuminaria = (req, res) => {
    luminariaDAO.updateLuminaria(req.params.identificador, req.body)
        .then(result => {
            if (result) {
                res.json({ status: "Luminaria updated" });
            } else {
                res.status(404).json({ status: "Luminaria not found" });
            }
        })
        .catch(err => {
            console.error(err);
            res.status(500).json({ status: "Server unavailable" });
        });
};

// Eliminar una luminaria por identificador
export const deleteLuminaria = (req, res) => {
    luminariaDAO.deleteLuminaria(req.params.identificador)
        .then(result => {
            if (result) {
                res.json({ status: "Luminaria deleted" });
            } else {
                res.status(404).json({ status: "Luminaria not found" });
            }
        })
        .catch(err => {
            console.error(err);
            res.status(500).json({ status: "Server unavailable" });
        });
};


// Insertar múltiples luminarias en lote (batch)
export const insertLuminariasBatch = (req, res) => {
    const luminarias = req.body;

    if (!Array.isArray(luminarias)) {
        return res.status(400).json({ status: "Bad request: se esperaba un array de luminarias" });
    }

    luminariaDAO.insertManyLuminarias(luminarias)
        .then(result => {
            res.status(201).json({ status: "Luminarias insertadas", cantidad: result.length });
        })
        .catch(err => {
            console.error(err);
            res.status(500).json({ status: "Error al insertar luminarias" });
        });
};
