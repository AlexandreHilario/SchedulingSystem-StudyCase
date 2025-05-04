frappe.ui.form.on('Appointment', {
  refresh(frm) {
    if (frm.doc.start_date && frm.doc.duration) {
      const startDate = frappe.datetime.str_to_obj(frm.doc.start_date);
      const duration = frm.doc.duration.split(':');
      const hours = parseInt(duration[0]);
      const minutes = parseInt(duration[1]);
      startDate.setHours(startDate.getHours() + hours);
      startDate.setMinutes(startDate.getMinutes() + minutes);
      frm.set_value('end_date', frappe.datetime.obj_to_str(startDate));
    }
  }
});