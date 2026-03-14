from models.database import call_procedure

#  CLIENTES
class ClienteModel:
    @staticmethod
    def get_all():
        return call_procedure("sp_GetAllClientes")

    @staticmethod
    def get_by_id(cliente_id):
        rows = call_procedure("sp_GetCliente", (cliente_id,))
        return rows[0] if rows else None

    @staticmethod
    def search(term):
        return call_procedure("sp_SearchClientes", (term,))

    @staticmethod
    def insert(tipo, nombre, documento, fecha_nac, direccion, telefono, email, clasif, foto):
        return call_procedure("sp_InsertCliente",
                              (tipo, nombre, documento, fecha_nac,
                               direccion, telefono, email, clasif, foto))

    @staticmethod
    def update(cliente_id, tipo, nombre, documento, fecha_nac, direccion,
               telefono, email, clasif, estado, foto):
        return call_procedure("sp_UpdateCliente",
                              (cliente_id, tipo, nombre, documento, fecha_nac,
                               direccion, telefono, email, clasif, estado, foto))

    @staticmethod
    def delete(cliente_id):
        return call_procedure("sp_DeleteCliente", (cliente_id,))

    @staticmethod
    def get_combo():
        return call_procedure("sp_GetAllClientesCombo")


# ══════════════════════════════════════════════════════════════════
#  PLANES
# ══════════════════════════════════════════════════════════════════
class PlanModel:
    @staticmethod
    def get_all():
        return call_procedure("sp_GetAllPlanes")

    @staticmethod
    def get_by_id(plan_id):
        rows = call_procedure("sp_GetPlan", (plan_id,))
        return rows[0] if rows else None

    @staticmethod
    def search(term):
        return call_procedure("sp_SearchPlanes", (term,))

    @staticmethod
    def get_by_tipo(tipo):
        return call_procedure("sp_GetPlanesByTipo", (tipo,))

    @staticmethod
    def insert(codigo, nombre, tipo, descripcion, tarifa, permanencia, promocion, imagen):
        return call_procedure("sp_InsertPlan",
                              (codigo, nombre, tipo, descripcion,
                               tarifa, permanencia, promocion, imagen))

    @staticmethod
    def update(plan_id, codigo, nombre, tipo, descripcion, tarifa,
               permanencia, promocion, estado, imagen):
        return call_procedure("sp_UpdatePlan",
                              (plan_id, codigo, nombre, tipo, descripcion,
                               tarifa, permanencia, promocion, estado, imagen))

    @staticmethod
    def delete(plan_id):
        return call_procedure("sp_DeletePlan", (plan_id,))

    @staticmethod
    def get_combo():
        return call_procedure("sp_GetAllPlanesCombo")


# ══════════════════════════════════════════════════════════════════
#  CONTRATOS
# ══════════════════════════════════════════════════════════════════
class ContratoModel:
    @staticmethod
    def get_all():
        return call_procedure("sp_GetAllContratos")

    @staticmethod
    def get_by_id(contrato_id):
        rows = call_procedure("sp_GetContrato", (contrato_id,))
        return rows[0] if rows else None

    @staticmethod
    def get_by_cliente(cliente_id):
        return call_procedure("sp_GetContratosByCliente", (cliente_id,))

    @staticmethod
    def insert(numero, fecha_firma, cliente_id, plan_id, dir_inst,
               equipos, condiciones, fecha_inicio, duracion, monto):
        return call_procedure("sp_InsertContrato",
                              (numero, fecha_firma, cliente_id, plan_id,
                               dir_inst, equipos, condiciones,
                               fecha_inicio, duracion, monto))

    @staticmethod
    def update(contrato_id, numero, fecha_firma, cliente_id, plan_id,
               dir_inst, equipos, condiciones, fecha_inicio,
               duracion, monto, estado):
        return call_procedure("sp_UpdateContrato",
                              (contrato_id, numero, fecha_firma,
                               cliente_id, plan_id, dir_inst, equipos,
                               condiciones, fecha_inicio, duracion,
                               monto, estado))

    @staticmethod
    def delete(contrato_id):
        return call_procedure("sp_DeleteContrato", (contrato_id,))

    @staticmethod
    def get_combo():
        return call_procedure("sp_GetAllContratosCombo")


# ══════════════════════════════════════════════════════════════════
#  FACTURAS
# ══════════════════════════════════════════════════════════════════
class FacturaModel:
    @staticmethod
    def get_all():
        return call_procedure("sp_GetAllFacturas")

    @staticmethod
    def get_by_id(factura_id):
        rows = call_procedure("sp_GetFactura", (factura_id,))
        return rows[0] if rows else None

    @staticmethod
    def get_by_cliente(cliente_id):
        return call_procedure("sp_GetFacturasByCliente", (cliente_id,))

    @staticmethod
    def get_by_rango(fecha_ini, fecha_fin):
        return call_procedure("sp_GetFacturasByRangoFecha", (fecha_ini, fecha_fin))

    @staticmethod
    def insert(numero, periodo, fecha_emision, fecha_venc,
               cliente_id, contrato_id, fijos, variables,
               descuentos, impuestos, total):
        return call_procedure("sp_InsertFactura",
                              (numero, periodo, fecha_emision, fecha_venc,
                               cliente_id, contrato_id, fijos, variables,
                               descuentos, impuestos, total))

    @staticmethod
    def update(factura_id, numero, periodo, fecha_emision, fecha_venc,
               cliente_id, contrato_id, fijos, variables, descuentos,
               impuestos, total, estado_pago, forma_pago, fecha_pago):
        return call_procedure("sp_UpdateFactura",
                              (factura_id, numero, periodo, fecha_emision,
                               fecha_venc, cliente_id, contrato_id,
                               fijos, variables, descuentos, impuestos,
                               total, estado_pago, forma_pago, fecha_pago))

    @staticmethod
    def delete(factura_id):
        return call_procedure("sp_DeleteFactura", (factura_id,))

    @staticmethod
    def pagar(factura_id, forma_pago, fecha_pago):
        return call_procedure("sp_PagarFactura", (factura_id, forma_pago, fecha_pago))
