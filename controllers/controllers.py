from datetime import date
from models.models import PlanModel, ContratoModel, FacturaModel


# ══════════════════════════════════════════════════════════════════
#  PLANES
# ══════════════════════════════════════════════════════════════════
class PlanController:
    TIPOS_VALIDOS = ("Telefonía Móvil", "Internet Fijo", "Televisión", "Paquete")
    ESTADOS_VALIDOS = ("Vigente", "Descontinuado")

    @staticmethod
    def validate(codigo, nombre, tipo, tarifa, permanencia):
        errors = []
        if len(codigo.strip()) < 3:
            errors.append("Código del plan debe tener al menos 3 caracteres.")
        if len(nombre.strip()) < 3:
            errors.append("Nombre comercial debe tener al menos 3 caracteres.")
        if tipo not in PlanController.TIPOS_VALIDOS:
            errors.append(f"Tipo de servicio inválido. Opciones: {PlanController.TIPOS_VALIDOS}")
        try:
            t = float(tarifa)
            if t < 0:
                errors.append("Tarifa mensual no puede ser negativa.")
        except (ValueError, TypeError):
            errors.append("Tarifa mensual debe ser un número.")
        try:
            p = int(permanencia)
            if p < 0:
                errors.append("Permanencia mínima no puede ser negativa.")
        except (ValueError, TypeError):
            errors.append("Permanencia mínima debe ser un número entero.")
        return errors

    @staticmethod
    def get_all():
        return PlanModel.get_all()

    @staticmethod
    def get_by_id(plan_id):
        return PlanModel.get_by_id(plan_id)

    @staticmethod
    def search(term):
        return PlanModel.search(term)

    @staticmethod
    def get_combo():
        return PlanModel.get_combo()

    @staticmethod
    def insert(codigo, nombre, tipo, descripcion, tarifa, permanencia, promocion, imagen):
        errors = PlanController.validate(codigo, nombre, tipo, tarifa, permanencia)
        if errors:
            raise ValueError("\n".join(errors))
        return PlanModel.insert(codigo, nombre, tipo, descripcion,
                                float(tarifa), int(permanencia), promocion, imagen)

    @staticmethod
    def update(plan_id, codigo, nombre, tipo, descripcion, tarifa,
               permanencia, promocion, estado, imagen):
        if not plan_id:
            raise ValueError("Debe seleccionar un plan para actualizar.")
        if estado not in PlanController.ESTADOS_VALIDOS:
            raise ValueError("Estado del plan inválido.")
        errors = PlanController.validate(codigo, nombre, tipo, tarifa, permanencia)
        if errors:
            raise ValueError("\n".join(errors))
        return PlanModel.update(int(plan_id), codigo, nombre, tipo, descripcion,
                                float(tarifa), int(permanencia), promocion, estado, imagen)

    @staticmethod
    def delete(plan_id):
        if not plan_id:
            raise ValueError("Debe seleccionar un plan para eliminar.")
        return PlanModel.delete(int(plan_id))


# ══════════════════════════════════════════════════════════════════
#  CONTRATOS
# ══════════════════════════════════════════════════════════════════
class ContratoController:
    ESTADOS_VALIDOS = ("Activo", "Suspendido", "Cancelado", "Vencido")

    @staticmethod
    def validate(numero, fecha_firma, cliente_id, plan_id,
                 fecha_inicio, duracion, monto):
        errors = []
        if len(numero.strip()) < 3:
            errors.append("Número de contrato debe tener al menos 3 caracteres.")
        if not cliente_id:
            errors.append("Debe seleccionar un cliente.")
        if not plan_id:
            errors.append("Debe seleccionar un plan.")
        for label, val in [("Fecha firma", fecha_firma), ("Fecha inicio", fecha_inicio)]:
            try:
                date.fromisoformat(str(val))
            except (ValueError, TypeError):
                errors.append(f"{label} inválida (use YYYY-MM-DD).")
        try:
            d = int(duracion)
            if d < 0:
                errors.append("Duración no puede ser negativa.")
        except (ValueError, TypeError):
            errors.append("Duración debe ser un número entero (meses).")
        try:
            m = float(monto)
            if m < 0:
                errors.append("Monto mensual no puede ser negativo.")
        except (ValueError, TypeError):
            errors.append("Monto mensual debe ser un número.")
        return errors

    @staticmethod
    def get_all():
        return ContratoModel.get_all()

    @staticmethod
    def get_by_id(contrato_id):
        return ContratoModel.get_by_id(contrato_id)

    @staticmethod
    def get_by_cliente(cliente_id):
        return ContratoModel.get_by_cliente(cliente_id)

    @staticmethod
    def get_combo():
        return ContratoModel.get_combo()

    @staticmethod
    def insert(numero, fecha_firma, cliente_id, plan_id, dir_inst,
               equipos, condiciones, fecha_inicio, duracion, monto):
        errors = ContratoController.validate(numero, fecha_firma, cliente_id,
                                             plan_id, fecha_inicio, duracion, monto)
        if errors:
            raise ValueError("\n".join(errors))
        return ContratoModel.insert(numero, fecha_firma, int(cliente_id),
                                    int(plan_id), dir_inst, equipos,
                                    condiciones, fecha_inicio,
                                    int(duracion), float(monto))

    @staticmethod
    def update(contrato_id, numero, fecha_firma, cliente_id, plan_id,
               dir_inst, equipos, condiciones, fecha_inicio,
               duracion, monto, estado):
        if not contrato_id:
            raise ValueError("Debe seleccionar un contrato para actualizar.")
        if estado not in ContratoController.ESTADOS_VALIDOS:
            raise ValueError("Estado de contrato inválido.")
        errors = ContratoController.validate(numero, fecha_firma, cliente_id,
                                             plan_id, fecha_inicio, duracion, monto)
        if errors:
            raise ValueError("\n".join(errors))
        return ContratoModel.update(int(contrato_id), numero, fecha_firma,
                                    int(cliente_id), int(plan_id),
                                    dir_inst, equipos, condiciones,
                                    fecha_inicio, int(duracion),
                                    float(monto), estado)

    @staticmethod
    def delete(contrato_id):
        if not contrato_id:
            raise ValueError("Debe seleccionar un contrato para eliminar.")
        return ContratoModel.delete(int(contrato_id))

 # FACTURAS
class FacturaController:
    ESTADOS_PAGO  = ("Pendiente", "Pagada", "Vencida", "Anulada")
    FORMAS_PAGO   = ("Efectivo", "Transferencia", "Tarjeta", "Débito Automático")

    @staticmethod
    def validate(numero, periodo, fecha_emision, fecha_venc,
                 cliente_id, contrato_id, fijos, variables, descuentos, impuestos):
        errors = []
        if len(numero.strip()) < 3:
            errors.append("Número de factura inválido.")
        if len(periodo.strip()) < 4:
            errors.append("Período facturado inválido (ej: 2024-01).")
        if not cliente_id:
            errors.append("Debe seleccionar un cliente.")
        if not contrato_id:
            errors.append("Debe seleccionar un contrato.")
        for label, val in [("Fecha emisión", fecha_emision), ("Fecha vencimiento", fecha_venc)]:
            try:
                date.fromisoformat(str(val))
            except (ValueError, TypeError):
                errors.append(f"{label} inválida (use YYYY-MM-DD).")
        for label, val in [("Cargos fijos", fijos), ("Cargos variables", variables),
                           ("Descuentos", descuentos), ("Impuestos", impuestos)]:
            try:
                if float(val) < 0:
                    errors.append(f"{label} no puede ser negativo.")
            except (ValueError, TypeError):
                errors.append(f"{label} debe ser un número.")
        return errors

    @staticmethod
    def calc_total(fijos, variables, descuentos, impuestos):
        return round(float(fijos) + float(variables) - float(descuentos) + float(impuestos), 2)

    @staticmethod
    def get_all():
        return FacturaModel.get_all()

    @staticmethod
    def get_by_id(factura_id):
        return FacturaModel.get_by_id(factura_id)

    @staticmethod
    def get_by_cliente(cliente_id):
        return FacturaModel.get_by_cliente(cliente_id)

    @staticmethod
    def get_by_rango(fecha_ini, fecha_fin):
        return FacturaModel.get_by_rango(fecha_ini, fecha_fin)

    @staticmethod
    def insert(numero, periodo, fecha_emision, fecha_venc,
               cliente_id, contrato_id, fijos, variables,
               descuentos, impuestos):
        errors = FacturaController.validate(numero, periodo, fecha_emision, fecha_venc,
                                            cliente_id, contrato_id, fijos, variables,
                                            descuentos, impuestos)
        if errors:
            raise ValueError("\n".join(errors))
        total = FacturaController.calc_total(fijos, variables, descuentos, impuestos)
        return FacturaModel.insert(numero, periodo, fecha_emision, fecha_venc,
                                   int(cliente_id), int(contrato_id),
                                   float(fijos), float(variables),
                                   float(descuentos), float(impuestos), total)

    @staticmethod
    def update(factura_id, numero, periodo, fecha_emision, fecha_venc,
               cliente_id, contrato_id, fijos, variables, descuentos,
               impuestos, estado_pago, forma_pago, fecha_pago):
        if not factura_id:
            raise ValueError("Debe seleccionar una factura para actualizar.")
        errors = FacturaController.validate(numero, periodo, fecha_emision, fecha_venc,
                                            cliente_id, contrato_id, fijos, variables,
                                            descuentos, impuestos)
        if errors:
            raise ValueError("\n".join(errors))
        total = FacturaController.calc_total(fijos, variables, descuentos, impuestos)
        return FacturaModel.update(int(factura_id), numero, periodo,
                                   fecha_emision, fecha_venc,
                                   int(cliente_id), int(contrato_id),
                                   float(fijos), float(variables),
                                   float(descuentos), float(impuestos), total,
                                   estado_pago, forma_pago or None, fecha_pago or None)

    @staticmethod
    def delete(factura_id):
        if not factura_id:
            raise ValueError("Debe seleccionar una factura para eliminar.")
        return FacturaModel.delete(int(factura_id))

    @staticmethod
    def pagar(factura_id, forma_pago, fecha_pago):
        if not factura_id:
            raise ValueError("Debe seleccionar una factura.")
        if forma_pago not in FacturaController.FORMAS_PAGO:
            raise ValueError("Forma de pago inválida.")
        try:
            date.fromisoformat(str(fecha_pago))
        except (ValueError, TypeError):
            raise ValueError("Fecha de pago inválida.")
        return FacturaModel.pagar(int(factura_id), forma_pago, fecha_pago)
