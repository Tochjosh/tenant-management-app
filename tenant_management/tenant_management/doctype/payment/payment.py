# Copyright (c) 2022, Nwakaibeya Joshua and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.model.document import Document


class Payment(Document):

    def before_submit(self):

        if self.pay and self.balance > 0.0:
            if not self.amount_to_pay:
                frappe.throw('Enter amount to be paid')

            elif self.amount_to_pay > self.balance:
                frappe.throw('Amount to pay in excess of balance')

            else:
                self.balance = self.total_rent_amount - self.amount_to_pay

        else:
            frappe.throw(_("You've completed your payment"))

    def before_insert(self):

        if self.pay and self.balance > 0.0:
            if not self.amount_to_pay:
                frappe.throw('Enter amount to be paid')

            elif self.amount_to_pay > self.balance:
                frappe.throw('Amount to pay in excess of balance')

            self.balance = self.total_rent_amount - self.amount_to_pay

        else:
            frappe.throw(_("You've completed your payment"))


        self.pay = False

    def after_insert(self):

        if self.balance == 0.0:
            frappe.db.set_value('House', self.house, 'payment_status', 'paid')
        elif 0.0 < self.balance < self.rent:
            frappe.db.set_value('House', self.house, 'payment_status', 'partly_paid')
        else:
            frappe.db.set_value('House', self.house, 'payment_status', 'not_paid')


        # email = frappe.db.get_value('Tenant', self.tenant, 'email')
        #
        # message = _(f"""<h3>Payment Recieved</h3>
        #                 <p>We recieved you payment of {self.amount_to_pay}.</p><br>""")
        #
        # subject = f"Welcome onboard {self.full_name}!"
        #
        #
        #
        # email_args = {
        #     "recipients": [email],
        #     "message": message,
        #     "subject": subject,
        #     "reference_doctype": self.doctype,
        #     "reference_name": self.name,
        #     "delayed": False
        # }
        #
        # frappe.sendmail(**email_args)