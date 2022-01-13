# Copyright (c) 2022, Si Hay Sistema and contributors
# For license information, please see license.txt

from __future__ import unicode_literals

def calculate_amount(amount, currency="GTQ", exchange_rate=1):
    """
    Calcula el monto a cobrar segun el monto de ventas
    """

    SEMILLA = 0.01  # 1%
    EMPRESA = 0.000133335 # 0.0133335%
    ESCALADA = 0.02 # 2%
    ESTABLECIMIENTO = 4000

    total_due = 0

    if amount <= 25000:
        total_due = amount * SEMILLA

    if amount > 25000 and amount <= 100000:
        amt = amount * (SEMILLA + ((amount/1000) * EMPRESA))
        # Si el monto sobre pasa los 2000 se retorna 2000
        total_due = amt if amt <= 2000 else 2000

    if amount > 100000 and amount <= 200000:
        total_due = amount * ESCALADA

    if amount > 200000:
        total_due = ESTABLECIMIENTO

    return total_due