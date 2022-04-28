# Copyright (c) 2022, Nwakaibeya Joshua and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.utils import now


class Payment(Document):

    def pay_and_update(self):

        if frappe.get_value('House', self.house, 'undergoing_work') == 1:
            frappe.throw("This house is undergoing work. Payments cannot be made yet")

        if self.balance > 0.0:
            if self.amount_to_pay > self.balance:
                frappe.throw('Amount to pay in excess of balance')

            self.balance -= self.amount_to_pay
            self.last_payment_date = now().split(' ')[0]
            self.amount_to_pay = 0.0
        else:
            frappe.throw('You have completed your payment')

        house = frappe.get_doc("House", self.house)
        if self.balance == 0.0:
            house.payment_status = 'Paid'
            house.save()
        elif 0.0 < self.balance < self.rent:
            house.payment_status = 'Partly Paid'
            house.save()
        else:
            house.payment_status = 'Not Paid'
            house.save()

    def before_save(self):
        self.pay_and_update()

    def before_insert(self):
        self.balance = self.rent
