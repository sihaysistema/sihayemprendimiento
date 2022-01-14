// Copyright (c) 2022, Si Hay Sistema and contributors
// For license information, please see license.txt

frappe.ui.form.on("SHS Data Received", {
  refresh: function (frm) {
    generate_invoice(frm);
    view_invoices(frm);
  },
});

function generate_invoice(frm) {
  frm
    .add_custom_button(__("Generate Invoice"), function () {
      frappe.db
        .get_value("SHE Config", "SHE Config", ["product_to_be_invoiced", "sales_taxes_and_charges_default"])
        .then((r) => {
          let values = r.message;
          console.log(values.product_to_be_invoiced, values.sales_taxes_and_charges_default);

          // template de factura
          let invoice = {
            doctype: "Sales Invoice",
            customer: frm.doc.customer,
            currency: frm.doc.currency,
            taxes_and_charges: values.sales_taxes_and_charges_default,
            items: [],
            taxes: [],
            // due_date: cur_frm.doc.posting_date_time,
          };

          // Productos a facturar
          invoice["items"].push({
            doctype: "Sales Invoice Item",
            item_code: values.product_to_be_invoiced,
            description: `Si Hay Emprendimiento Mes ${__(frm.doc.month)}`,
            rate: frm.doc.total_due,
            qty: 1.0,
          });

          frappe.call({
            method: "sihayemprendimiento.api.get_taxes",
            freeze: true, // Muestra efecto de pantalla congelada
            freeze_message: __("Generating Invoice..."),
            args: { template_name: values.sales_taxes_and_charges_default },
            callback: function (r) {
              // Impuestos
              invoice["taxes"].push(r.message);

              frappe.db.insert(invoice).then((doc) => {
                frm.save_or_update();
                frappe.set_route("Form", "Sales Invoice", doc.name);
              });
            },
          });
        });
    })
    .addClass("btn-primary");
}

function view_invoices(frm) {
  frm.add_custom_button(__("View Invoices"), function () {
    window.open("/app/sales-invoice", "_blank");
  });
}
