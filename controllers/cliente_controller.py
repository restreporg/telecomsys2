import re
from datetime import date
from models.models import ClienteModel

EMAIL_RE = re.compile(r"^[\w\.\+\-]+@[\w\-]+\.[a-zA-Z]{2,}$")


class ClienteController:
    """Lógica de negocio + validaciones para Clientes."""

    # ─ Validación ─
    @staticmethod
    def validate(tipo, nombre, documento, fecha_nac, telefono, email, clasif):
        errors = []

        if tipo not in ("Personal", "Empresarial"):
            errors.append("Tipo de cliente inválido.")

        if len(nombre.strip()) < 3:
            errors.append("Nombre/Razón Social debe tener al menos 3 caracteres.")
        if len(nombre.strip()) > 100:
            errors.append("Nombre/Razón Social no puede superar 100 caracteres.")

        if len(documento.strip()) < 5:
            errors.append("Documento debe tener al menos 5 caracteres.")
        if not documento.strip().replace("-", "").replace("_", "").isalnum():
            errors.append("Documento solo puede contener letras, números, guiones.")

        if fecha_nac:
            try:
                date.fromisoformat(str(fecha_nac))
            except ValueError:
                errors.append("Fecha de nacimiento/constitución inválida (use YYYY-MM-DD).")

        if telefono and not re.match(r"^\+?[\d\s\-\(\)]{7,20}$", telefono.strip()):
            errors.append("Teléfono inválido.")

        if email and not EMAIL_RE.match(email.strip()):
            errors.append("Correo electrónico con formato inválido.")

        if clasif not in ("A", "B", "C", "D"):
            errors.append("Clasificación crediticia debe ser A, B, C o D.")

        return errors

    # CRUD
    @staticmethod
    def get_all():
        return ClienteModel.get_all()

    @staticmethod
    def get_by_id(cliente_id):
        return ClienteModel.get_by_id(cliente_id)

    @staticmethod
    def search(term):
        return ClienteModel.search(term)

    @staticmethod
    def insert(tipo, nombre, documento, fecha_nac, direccion,
               telefono, email, clasif, foto):
        errors = ClienteController.validate(tipo, nombre, documento, fecha_nac, telefono, email, clasif)
        if errors:
            raise ValueError("\n".join(errors))
        return ClienteModel.insert(tipo, nombre, documento,
                                   fecha_nac or None, direccion,
                                   telefono, email, clasif, foto)

    @staticmethod
    def update(cliente_id, tipo, nombre, documento, fecha_nac, direccion,
               telefono, email, clasif, estado, foto):
        if not cliente_id:
            raise ValueError("Debe seleccionar un cliente para actualizar.")
        errors = ClienteController.validate(tipo, nombre, documento, fecha_nac, telefono, email, clasif)
        if errors:
            raise ValueError("\n".join(errors))
        return ClienteModel.update(int(cliente_id), tipo, nombre, documento,
                                   fecha_nac or None, direccion,
                                   telefono, email, clasif, estado, foto)

    @staticmethod
    def delete(cliente_id):
        if not cliente_id:
            raise ValueError("Debe seleccionar un cliente para eliminar.")
        return ClienteModel.delete(int(cliente_id))

    @staticmethod
    def get_combo():
        return ClienteModel.get_combo()
