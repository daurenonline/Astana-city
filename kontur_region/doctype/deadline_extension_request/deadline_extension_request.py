# Copyright (c) 2026, Dauren Bolatov and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.utils import nowdate, now_datetime

class DeadlineExtensionRequest(Document):
    def on_submit(self):
        # When workflow transitions to 'Утверждено', apply new deadline to the object
        if self.workflow_state == "Утверждено":
            self.apply_deadline_to_object()

    def apply_deadline_to_object(self):
        obj = frappe.get_doc("Infrastructure Object", self.infrastructure_object)
        old_deadline = obj.deadline
        obj.deadline = self.requested_deadline
        obj.deadline_change_count = (obj.deadline_change_count or 0) + 1
        obj.save(ignore_permissions=True)

        # Log into audit trail
        log = frappe.get_doc({
            "doctype": "Deadline Change Log",
            "infrastructure_object": obj.name,
            "object_name": obj.object_name,
            "changed_by": self.approved_by or frappe.session.user,
            "change_time": now_datetime(),
            "old_deadline": old_deadline,
            "new_deadline": self.requested_deadline,
            "reason": f"Утверждена заявка {self.name}: {self.reason_category} ({self.justification[:100]}...)"
        })
        log.insert(ignore_permissions=True)
