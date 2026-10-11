# Copyright (c) 2026, Dauren Bolatov and contributors
# For license information, please see license.txt

import frappe
from frappe.utils import getdate, nowdate

def recalculate_all_overdue():
    """Ежедневная крон-задача: автоматический пересчёт флага просрочки по всем объектам."""
    today = getdate(nowdate())
    
    # 1. Помечаем просроченные
    frappe.db.sql("""
        UPDATE `tabInfrastructure Object`
        SET is_overdue = 1
        WHERE status != 'Завершён'
          AND deadline < %s
          AND is_overdue = 0
    """, (today,))
    
    # 2. Снимаем признак просрочки с тех, чей срок еще не вышел или кто завершен
    frappe.db.sql("""
        UPDATE `tabInfrastructure Object`
        SET is_overdue = 0
        WHERE (status = 'Завершён' OR deadline >= %s)
          AND is_overdue = 1
    """, (today,))
    
    frappe.db.commit()
