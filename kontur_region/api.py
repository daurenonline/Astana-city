# Copyright (c) 2026, Dauren Bolatov and contributors
# For license information, please see license.txt

import frappe
from frappe.utils import getdate, nowdate, now_datetime

@frappe.whitelist(allow_guest=True)
def get_dashboard_summary(category=None, district=None):
    """Возвращает расширенную аналитическую сводку для акима региона."""
    today = getdate(nowdate())
    filters = {}
    if category and category != "all":
        filters["category"] = category
    if district and district != "all":
        filters["district"] = district

    total = frappe.db.count("Infrastructure Object", filters)
    
    active_filters = {**filters, "status": "В работе"}
    active = frappe.db.count("Infrastructure Object", active_filters)
    
    done_filters = {**filters, "status": "Завершён"}
    done = frappe.db.count("Infrastructure Object", done_filters)

    # Overdue objects
    overdue_filters = {
        **filters,
        "status": ["!=", "Завершён"],
        "deadline": ["<", today]
    }
    overdue = frappe.db.count("Infrastructure Object", overdue_filters)

    # Budget at risk calculation
    overdue_objects = frappe.get_all(
        "Infrastructure Object",
        filters=overdue_filters,
        fields=["name", "object_name", "district", "category", "budget_kzt", "deadline", "owner_name", "contractor", "completion_percent"]
    )
    risk_budget_kzt = sum([o.budget_kzt or 0 for o in overdue_objects])

    # Recent Audit Log
    recent_logs = frappe.get_all(
        "Deadline Change Log",
        fields=["infrastructure_object", "object_name", "changed_by", "old_deadline", "new_deadline", "change_time", "reason"],
        order_by="change_time desc",
        limit=25
    )

    all_objects = frappe.get_all(
        "Infrastructure Object",
        filters=filters,
        fields=[
            "name", "object_name", "district", "category", "owner_name",
            "deadline", "status", "is_overdue", "completion_percent",
            "budget_kzt", "contractor", "latitude", "longitude"
        ],
        order_by="modified desc"
    )

    return {
        "metrics": {
            "total": total,
            "active": active,
            "overdue": overdue,
            "done": done,
            "risk_budget_kzt": risk_budget_kzt,
            "control_date": str(today)
        },
        "objects": all_objects,
        "overdue_details": overdue_objects,
        "recent_logs": recent_logs
    }

@frappe.whitelist()
def generate_executive_briefing():
    """Формирует служебную записку (селекторную справку) для аппаратного совещания акима."""
    summary = get_dashboard_summary()
    today = summary["metrics"]["control_date"]
    late_items = summary["overdue_details"]
    
    return {
        "title": f"Справка о ходе реализации инфраструктурных проектов на {today}",
        "total_projects": summary["metrics"]["total"],
        "risk_count": summary["metrics"]["overdue"],
        "risk_budget_kzt": summary["metrics"]["risk_budget_kzt"],
        "critical_items": [
            {
                "name": item.object_name,
                "district": item.district,
                "contractor": item.contractor,
                "deadline": str(item.deadline),
                "progress": item.completion_percent,
                "budget": item.budget_kzt
            }
            for item in late_items
        ]
    }
