# Copyright (c) 2022, Si Hay Sistema and contributors
# For license information, please see license.txt

from __future__ import unicode_literals

import json
import frappe
import requests

from frappe import _
from frappe.utils import get_site_name, get_first_day, get_last_day, nowdate, flt
from factura_electronica.factura_electronica.report.gt_sales_ledger.gt_sales_ledger import execute
from sihayemprendimiento.utils.she_math import calculate_amount

MONTHS = ("January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December",)


@frappe.whitelist()
def sender():
    """
    Envia el total de ventas por mes al server de sihaysistema
    """

    try:
        today = nowdate()

        # Primer y ultimo dia del mes actual
        from_date = str(get_first_day(today))
        to_date = str(get_last_day(today))
        companies = frappe.db.get_values('SHE Company', filters={'parent': 'SHE Config'},
                                        fieldname=['company', 'currency', 'tax_id',
                                                   'customer'], as_dict=1)

        # Por cada compañia configurada se realiza la consulta y envio de datos
        for company in companies:
            filters = frappe._dict({
                "company": company.company,
                "nit": company.tax_id,
                "from_date": from_date,
                "to_date": to_date,
                "company_currency": company.currency,
                "options": "Monthly"
            })

            # Ejecuta el reporte de GT Sales Ledger
            res = execute(filters)[1][0]
            res.update({
                "company": company.company,
                "tax_id": company.tax_id,
                "customer": company.customer,
            })

            with open("resultado.json", "w") as f:
                f.write(json.dumps(res, indent=2, default=str))

        frappe.msgprint(
            msg=f'Datos Enviados al servidor de Si Hay Sistema',
            title=_(f'Datos enviados'),
            indicator='green'
        )

    except:
        frappe.msgprint(
            msg=f'Detalle del error <br><hr> <code>{frappe.get_traceback()}</code>',
            title=_(f'Datos no enviados'),
            raise_exception=True
        )


@frappe.whitelist(methods=['POST'])
def receiver(**kwargs):
    """Endpoint para recibir datos de ventas por mes

    Returns:
        tuple: status
    """
    try:
        frappe.local.response.http_status_code = 200

        if not kwargs: False, "No Recibido"

        doc = frappe.get_doc({
            'doctype': 'SHS Data Received',
            'month': MONTHS[kwargs.get('month_repo')],
            'year': kwargs.get('year_repo'),
            'currency': kwargs.get('currency'),
            'total': kwargs.get('total'),
            'total_due': calculate_amount(flt(kwargs.get('total'), 2)),
            'company': kwargs.get('company'),
            'customer': kwargs.get('customer'),
            'tax_id': kwargs.get('tax_id'),
        })
        doc.insert()

        return True, "Recibido"

    except:
        return False, "No Recibido"