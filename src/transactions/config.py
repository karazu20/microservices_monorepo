import os

from setup.config import LOGS_PATH, Logs


def get_api_url():
    host = os.environ.get("API_HOST", "127.0.0.1")
    http = os.environ.get("API_PROTOCOL", "http")
    port = 5000 if host == "127.0.0.1" else 80
    return f"{http}://{host}:{port}"


LOGS_PATH = f"{LOGS_PATH}/transactions.log"

SOURCE_PATH = "src.transactions"

Logs.add_logs(SOURCE_PATH, LOGS_PATH)

TYPE_TRANSACTION = {
    "FEE_APPLIED": "Cargo aplicado",
    "REPAYMENT": "Pago Introducido",
    "DISBURSEMENT": "Desembolso",
    "INTEREST_APPLIED": "Interés Aplicado",
    "IMPORT": "Importe",
    "DISBURSEMENT_ADJUSTMENT": "Ajuste del Desembolso",
    "WRITE_OFF": "Cancelado",
    "WRITE_OFF_ADJUSTMENT": "Ajuste cancelado",
    "PAYMENT_MADE": "Pago realizado",
    "WITHDRAWAL_REDRAW": "Retirado",
    "WITHDRAWAL_REDRAW_ADJUSTMENT": "Ajuste Retirado",
    "FEE_CHARGED": "Cargo aplicado",
    "FEES_DUE_REDUCED": "Cargos pendientes reducidos",
    "FEE_ADJUSTMENT": "Cargo Ajustado",
    "PENALTY_APPLIED": "Aplicada Penalización",
    "PENALTY_ADJUSTMENT": "Penalización Ajustada",
    "PENALTIES_DUE_REDUCED": "Penalización reducida",
    "REPAYMENT_ADJUSTMENT": "Ajuste pago",
    "PAYMENT_MADE_ADJUSTMENT": "Pago ajustado",
    "INTEREST_RATE_CHANGED": "Cambio de tasa de interés",
    "TAX_RATE_CHANGED": "Tasa de impuesto cambiada",
    "PENALTY_RATE_CHANGED": "Tasa de penalizacion cambiada",
    "INTEREST_APPLIED_ADJUSTMENT": "Ajuste de interés aplicado",
    "INTEREST_DUE_REDUCED": "Interes Adeudado reducido",
    "PENALTY_REDUCTION_ADJUSTMENT": "Ajust reducción de penalizacion",
    "FEE_REDUCTION_ADJUSTMENT": "Ajuste reducción de pago",
    "INTEREST_REDUCTION_ADJUSTMENT": "Ajuste de reducción de interés",
    "DEFERRED_INTEREST_APPLIED": "Interés diferido aplicado",
    "DEFERRED_INTEREST_APPLIED_ADJUSTMENT": "Interés diferido ajustado",
    "DEFERRED_INTEREST_PAID": "Interés diferido pagado",
    "DEFERRED_INTEREST_PAID_ADJUSTMENT": "Interés diferido ajustado",
    "INTEREST_LOCKED": "Interes bloqueado",
    "FEE_LOCKED": "Cargo bloqueado",
    "PENALTY_LOCKED": "Penalización bloqueda",
    "INTEREST_UNLOCKED": "Interés desbloqueado",
    "FEE_UNLOCKED": "Cargo desbloqueado",
    "PENALTY_UNLOCKED": "Penalización desbloqueado",
    "REDRAW_TRANSFER": "Retiro transferencia",
    "REDRAW_REPAYMENT": "Ajuste de Pago",
    "REDRAW_TRANSFER_ADJUSTMENT": "Ajuste de transferencia de retiro",
    "REDRAW_REPAYMENT_ADJUSTMENT": "Ajuste de pago de retiro",
    "TRANSFER": "Transferencia",
    "TRANSFER_ADJUSTMENT": "Ajuste de transferencia",
    "BRANCH_CHANGED": "Asignacion de pago a otra sucursal",
    "TERMS_CHANGED": "Cambio de terminos",
    "CARD_TRANSACTION_REVERSAL": "CARD_TRANSACTION_REVERSAL",
    "CARD_TRANSACTION_REVERSAL_ADJUSTMENT": "CARD_TRANSACTION_REVERSAL_ADJUSTMENT",
    "DUE_DATE_CHANGED": "Cambio de fecha de vencimiento",
    "DUE_DATE_CHANGED_ADJUSTMENT": "Ajuste de cambio de fecha de vencimiento",
    "ACCOUNT_TERMINATED": "Cuenta Terminada",
    "ACCOUNT_TERMINATED_ADJUSTMENT": "Ajuste de cuenta terminada",
}
