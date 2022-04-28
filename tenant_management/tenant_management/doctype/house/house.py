# Copyright (c) 2022, Nwakaibeya Joshua and contributors
# For license information, please see license.txt

# import frappe
from frappe.model.document import Document


class House(Document):

    def update_status(self):

        if self.tenant:
            self.undergoing_work = 0
            self.occupancy_status = 'Occupied'
        else:
            if self.undergoing_work == 1:
                self.occupancy_status = 'Out Of Service'
            else:
                self.occupancy_status = 'Available'

    def on_update(self):
        self.update_status()

    def before_save(self):
        self.update_status()
