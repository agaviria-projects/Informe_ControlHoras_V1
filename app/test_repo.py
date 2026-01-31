from app.data.repository import crear_registro, buscar_registros

crear_registro({
    "cedula": "123456",
    "nombre": "Juan Perez",
    "placa": "ABC123",
    "fecha": "2026-01-30",
    "kilometro": 120,
    "horas_trabajadas": 8,
    "valor_hora_extra": 15000
})

registros = buscar_registros(nombre="Juan")
print(registros)
