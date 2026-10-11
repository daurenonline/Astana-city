# Copyright (c) 2026, Dauren Bolatov and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.utils import getdate, nowdate, now_datetime

class InfrastructureObject(Document):
    def validate(self):
        self.update_overdue_flag()
        self.track_deadline_changes()

    def update_overdue_flag(self):
        """Просрочен, если дата дедлайна раньше сегодняшней и объект еще не завершён."""
        if not self.deadline:
            self.is_overdue = 0
            return
        today = getdate(nowdate())
        deadline_date = getdate(self.deadline)
        if self.status != "Завершён" and deadline_date < today:
            self.is_overdue = 1
        else:
            self.is_overdue = 0

    def track_deadline_changes(self):
        """Если срок изменился по сравнению с БД, фиксируем запись в Deadline Change Log."""
        if self.is_new():
            return
        
        old_doc = self.get_doc_before_save()
        if not old_doc:
            return

        if old_doc.deadline != self.deadline:
            self.deadline_change_count = (self.deadline_change_count or 0) + 1
            log = frappe.get_doc({
                "doctype": "Deadline Change Log",
                "infrastructure_object": self.name,
                "object_name": self.object_name,
                "changed_by": frappe.session.user or "Administrator",
                "change_time": now_datetime(),
                "old_deadline": old_doc.deadline,
                "new_deadline": self.deadline,
                "reason": "Корректировка календарного графика"
            })
            log.insert(ignore_permissions=True)


def validate_deadline(doc, method):
    doc.update_overdue_flag()

def on_object_update(doc, method):
    pass
