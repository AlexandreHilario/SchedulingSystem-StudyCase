import frappe
from frappe.utils import get_datetime, add_to_date

def before_save(doc, method):
    if doc.start_date and doc.duration:
        start_datetime = get_datetime(doc.start_date)
        hours, minutes = map(int, str(doc.duration).split(':'))
        doc.end_date = add_to_date(start_datetime, hours=hours, minutes=minutes)

def validate(doc, method):
    validate_seller_availability(doc)

def validate_seller_availability(doc):
    if not doc.seller or not doc.start_date or not doc.end_date:
        return

    overlapping_appointments = frappe.db.sql("""
        SELECT name 
        FROM `tabAppointment`
        WHERE seller = %(seller)s
        AND name != %(name)s
        AND (
            (start_date <= %(start_date)s AND end_date > %(start_date)s)
            OR (start_date < %(end_date)s AND end_date >= %(end_date)s)
            OR (start_date >= %(start_date)s AND end_date <= %(end_date)s)
        )
        AND docstatus < 2
        AND status != 'Canceled'
    """, {
        'seller': doc.seller,
        'start_date': doc.start_date,
        'end_date': doc.end_date,
        'name': doc.name or 'None'
    }, as_dict=True)

    if overlapping_appointments:
        frappe.throw(f"O vendendor já possui um compromisso neste horário: {overlapping_appointments[0].name}")