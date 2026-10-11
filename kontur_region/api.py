# Copyright (c) 2026, Dauren Bolatov and contributors
# For license information, please see license.txt

import frappe
from frappe.utils import getdate, nowdate, now_datetime

@frappe.whitelist(allow_guest=True)
def get_dashboard_summary():
    """Возвращает агрегированную сводку для дашборда акима."""
    today = getdate(nowdate())
    
    total = frappe.db.count("Infrastructure Object")
    active = frappe.db.count("Infrastructure Object", {"status": "В работе"})
    done = frappe.db.count("Infrastructure Object", {"status": "Завершён"})
    
    # Overdue: status != 'Завершён' and deadline < today
    overdue = frappe.db.count("Infrastructure Object", {
        "status": ["!=", "Завершён"],
        "deadline": ["<", today]
    })
    
    recent_logs = frappe.get_all(
        "Deadline Change Log",
        fields=["infrastructure_object", "object_name", "changed_by", "old_deadline", "new_deadline", "change_time", "reason"],
        order_by="change_time desc",
        limit=20
    )
    
    objects = frappe.get_all(
        "Infrastructure Object",
        fields=["name", "object_name", "district", "owner_name", "deadline", "status", "is_overdue"],
        order_by="modified desc"
    )
    
    return {
        "metrics": {
            "total": total,
            "active": active,
            "overdue": overdue,
            "done": done,
            "control_date": str(today)
        },
        "objects": objects,
        "recent_logs": recent_logs
    }

@frappe.whitelist()
def update_object_deadline(object_id, new_deadline, reason=None):
    """Обновляет срок завершения объекта с фиксацией в журнале аудита."""
    if not frappe.has_permission("Infrastructure Object", "write"):
        frappe.throw("Недостаточно прав для изменения срока объекта", frappe.PermissionError)
        
    doc = frappe.get_doc("Infrastructure Object", object_id)
    doc.deadline = new_deadline
    if reason:
        doc.description = f"{doc.description or ''}\n[{now_datetime()}] Срок изменен: {reason}".strip()
    doc.save()
    
    return {
        "status": "success",
        "name": doc.name,
        "deadline": doc.deadline,
        "is_overdue": doc.is_overdue
    }
