import Luminaria from '../models/luminariaModel.js'

const C = console.log.bind(console.log)
const luminariaDAO = {}

// Obtener todas las luminarias (sin filtro)
luminariaDAO.getPaginated = async (skip, limit) => {
    return await Luminaria.find().skip(skip).limit(limit).lean();
};

luminariaDAO.countAll = async () => {
    return await Luminaria.countDocuments();
};


// Obtener una luminaria por su identificador (ID)
luminariaDAO.getOne = async (identificador) => {
    const luminaria = await Luminaria.findOne({ identificador })
    return luminaria
}

// Insertar una nueva luminaria (crear)	
luminariaDAO.insertLuminaria = async (luminaria) => {
    const luminariaSaved = new Luminaria(luminaria)
    await luminariaSaved.save()
    return true
}

// Actualizar una luminaria por su identificador (ID)
luminariaDAO.updateLuminaria = async (identificador, luminaria) => {
    const luminariaUpdated = await Luminaria.findOneAndUpdate({ identificador }, luminaria)
    return luminariaUpdated !== null
}

// Eliminar una luminaria por su identificador (ID)
luminariaDAO.deleteLuminaria = async (identificador) => {
    const luminariaDeleted = await Luminaria.findOneAndDelete({ identificador })
    return luminariaDeleted !== null
}


// Insertar en batch varias luminarias
luminariaDAO.insertManyLuminarias = async (luminarias) => {
    const inserted = await Luminaria.insertMany(luminarias);
    return inserted;
};


export default luminariaDAO
