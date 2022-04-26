# Copyright (c) 2022, Nwakaibeya Joshua and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.utils import now


class Payment(Document):

    def check_transaction_and_pay(self):
        if not self.pay:
            frappe.throw('Check pay to proceed with payment')

        if self.balance > 0.0:
            if not self.amount_to_pay:
                frappe.throw('Enter amount to be paid')

            if self.amount_to_pay > self.balance:
                frappe.throw('Amount to pay in excess of balance')

            self.balance -= self.amount_to_pay
            self.last_payment_date = now().split(' ')[0]
            self.pay = False
        else:
            frappe.throw("You've completed your payment")

    def update_house_status(self):
        if self.balance == 0.0:
            frappe.db.set_value('House', self.house, 'payment_status', 'paid')
        elif 0.0 < self.balance < self.rent:
            frappe.db.set_value('House', self.house, 'payment_status', 'partly_paid')
        else:
            frappe.db.set_value('House', self.house, 'payment_status', 'not_paid')

    def before_insert(self):
        self.balance = self.total_rent_amount
        self.check_transaction_and_pay()

    def after_insert(self):
        self.update_house_status()

    def on_update(self):
        self.check_transaction_and_pay()

    def after_update(self):
        self.update_house_status()

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
