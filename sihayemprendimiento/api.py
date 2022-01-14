# Copyright (c) 2022, Si Hay Sistema and contributors
# For license information, please see license.txt

from __future__ import unicode_literals

import base64
import json

import frappe
import requests
from factura_electronica.factura_electronica.report.gt_sales_ledger.gt_sales_ledger import \
    execute
from frappe import _
from frappe.utils import (flt, get_first_day, get_last_day, get_site_name,
                          nowdate)
from frappe.utils.password import get_decrypted_password

from sihayemprendimiento.utils.she_math import calculate_amount

MONTHS = ("January", "February", "March", "April", "May", "June",
          "July", "August", "September", "October", "November", "December",)


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

            # Ejecuta el reporte de GT Sales Ledger para obtener el total de ventas
            # del mes actual
            res = execute(filters)[1][0]
            res.update({
                "company": company.company,
                "tax_id": company.tax_id,
                "customer": company.customer,
            })

            response = request_server(res)

            doc = frappe.get_doc({
                'doctype': 'SHE Data Sent',
                'month': MONTHS[res.get('month_repo')],
                'year': res.get('year_repo'),
                'currency': res.get('currency'),
                'total': res.get('total'),
                'total_due': calculate_amount(flt(res.get('total'), 2)),
                'company': res.get('company'),
                'customer': res.get('customer'),
                'tax_id': res.get('tax_id'),
                'status': response[1]
            })
            doc.insert()

            if response[0]:
                frappe.msgprint(
                    msg=f'Datos enviados al servidor de Si Hay Sistema',
                    title=_(f'Datos enviados'),
                    indicator='green'
                )
            else:
                frappe.msgprint(
                    msg=f'Dato no recibido, por favor reportar este incidente <hr> <code>{response[1]}</code>',
                    title=_(f'Datos No Recibidos'),
                    indicator='red'
                )
                
            return

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
        with open('datos-recibidos.json', 'w') as f:
            f.write(json.dumps(kwargs))

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


def request_server(res):
    try:
        # Envio de datos
        url = frappe.db.get_single_value('SHE Config', 'master_domain')
        api_key = get_decrypted_password('SHE Config', 'SHE Config', 'public_key', False)
        api_secret = get_decrypted_password('SHE Config', 'SHE Config', 'private_key', False)
        secret = "{0}:{1}".format(api_key, api_secret)

        with open('decrypted.txt', 'w') as f:
            f.write(str(url))

        key_p = base64.b64encode(secret.encode('ascii'))

        payload = res
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Basic {key_p.decode("utf-8")}'
        }

        response = requests.request("POST", url, headers=headers, data=json.dumps(payload))

        frappe.msgprint(json.loads(response.content))

        if json.loads(response.content.get("message"))[0]:
            return True, "Enviado"
        else:
            return False, "No Enviado"

    except:
        return False, frappe.get_traceback()