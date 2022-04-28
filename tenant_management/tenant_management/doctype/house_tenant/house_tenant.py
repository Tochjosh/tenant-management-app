# Copyright (c) 2022, Nwakaibeya Joshua and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.model.document import Document
from frappe.utils import (validate_phone_number, validate_email_address, random_string, pretty_date)

class HouseTenant(Document):
	def validate(self):
		validate_phone_number(self.phone, throw=True)
		if self.email:
			validate_email_address(self.email, throw=True)


	def before_insert(self):

		email_exist = frappe.db.exists({"doctype": "House Tenant", "email": self.email})
		if email_exist:
			frappe.throw('A user with this email already exist')


	def after_insert(self):

		message = _("""<h3>Welcome</h3>
	                          <p>This is to let you know that we have created a profile for you in our organization.</p>
	                          <p>Thank you for trusting us with your property needs.</p><br>
	                          <p>Welcome to the family.</p>""")

		subject = f"Welcome onboard {self.full_name}!"

		email_args = {
			"recipients": [self.email],
			"message": message,
			"subject": subject,
			"reference_doctype": self.doctype,
			"reference_name": self.name,
			"delayed": False
		}

		frappe.sendmail(**email_args)

