from app.repositories import curso_repository


def obtener_todos():
    return curso_repository.obtener_todos()


def obtener_por_id(curso_id):
    curso = curso_repository.obtener_por_id(curso_id)
    if not curso:
        raise ValueError(f'Curso {curso_id} no encontrado')
    return curso


def crear(datos):
    # Validar campos obligatorios
    if not datos.get('nombre'):
        raise ValueError('El nombre es obligatorio')
    if not datos.get('cuatrimestre'):
        raise ValueError('El cuatrimestre es obligatorio')
    if not datos.get('anio'):
        raise ValueError('El año es obligatorio')

    # Validar que cuatrimestre sea 1C o 2C
    if datos['cuatrimestre'] not in ('1C', '2C'):
        raise ValueError('El cuatrimestre debe ser 1C o 2C')

    # Validar que anio sea un número razonable
    anio = datos['anio']
    if not isinstance(anio, int) or anio < 2000 or anio > 2100:
        raise ValueError('El año debe ser un número válido')

    # Verificar si ya existe un curso con el mismo nombre, cuatrimestre y año → 409
    curso_existente = curso_repository.buscar_duplicado(
        datos['nombre'],
        datos['cuatrimestre'],
        datos['anio']
    )
    if curso_existente:
        raise ValueError(
            f"Ya existe un curso '{datos['nombre']}' para el {datos['cuatrimestre']} de {datos['anio']}"
        )

    return curso_repository.insertar(datos)


def actualizar(curso_id, datos):
    # Verificar que el curso existe
    obtener_por_id(curso_id)

    # Validar campos obligatorios
    if not datos.get('nombre'):
        raise ValueError('El nombre es obligatorio')
    if not datos.get('cuatrimestre'):
        raise ValueError('El cuatrimestre es obligatorio')
    if not datos.get('anio'):
        raise ValueError('El año es obligatorio')

    # Validar cuatrimestre
    if datos['cuatrimestre'] not in ('1C', '2C'):
        raise ValueError('El cuatrimestre debe ser 1C o 2C')

    # Verificar duplicado excluyendo el curso actual
    curso_existente = curso_repository.buscar_duplicado(
        datos['nombre'],
        datos['cuatrimestre'],
        datos['anio'],
        excluir_id=curso_id
    )
    if curso_existente:
        raise ValueError(
            f"Ya existe un curso '{datos['nombre']}' para el {datos['cuatrimestre']} de {datos['anio']}"
        )

    return curso_repository.actualizar(curso_id, datos)


def eliminar(curso_id):
    obtener_por_id(curso_id)
    curso_repository.eliminar(curso_id)