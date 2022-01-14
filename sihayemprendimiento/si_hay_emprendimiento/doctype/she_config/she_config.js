// Copyright (c) 2022, Si Hay Sistema and contributors
// For license information, please see license.txt

frappe.ui.form.on("SHE Config", {
  refresh: function (frm) {
    show_and_hide(frm);
  },
  receiver: function (frm) {
    show_and_hide(frm);
  },
});

function btn_sender(frm) {
  frm
    .add_custom_button(__("Send Data Manually"), function () {
      frappe.call({
        method: "sihayemprendimiento.api.sender",
        freeze: true, // Muestra efecto de pantalla congelada
        freeze_message: __("Sending data..."),
        callback: function (r) {
          // frm.reload_doc();
        },
      });
    })
    .addClass("btn-primary");
}

function show_and_hide(frm) {
  if (!frm.doc.receiver) {
    btn_sender(frm);
  } else {
    frm.clear_custom_buttons();
  }
}
