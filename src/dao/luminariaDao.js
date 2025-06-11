import Luminaria from '../models/luminariaModel.js'

const C = console.log.bind(console.log)
const luminariaDAO = {}

// Obtener todas las luminarias (sin filtro)
luminariaDAO.getAll = async () => {
    const luminarias = await Luminaria.find()
    return luminarias
}

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

// Consultar luminarias con filtro//

export default luminariaDAO
