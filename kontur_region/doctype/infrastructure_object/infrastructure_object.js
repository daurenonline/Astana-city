// Copyright (c) 2026, Dauren Bolatov and contributors
// For license information, please see license.txt

frappe.ui.form.on('Infrastructure Object', {
    refresh: function(frm) {
        if (frm.doc.is_overdue) {
            frm.dashboard.set_headline_alert(
                __('Внимание: объект просрочен! Плановый срок завершения прошёл.'),
                'red'
            );
        } else if (frm.doc.status === 'Завершён') {
            frm.dashboard.set_headline_alert(
                __('Объект успешно завершён.'),
                'green'
            );
        }
    },
    deadline: function(frm) {
        if (frm.doc.deadline && frm.doc.status !== 'Завершён') {
            const today = frappe.datetime.get_today();
            if (frm.doc.deadline < today) {
                frappe.msgprint({
                    title: __('Контроль дедлайна'),
                    indicator: 'orange',
                    message: __('Выбранный срок находится в прошлом. При сохранении объект будет помечен как просроченный, а перенос зафиксирован в аудит-журнале.')
                });
            }
        }
    }
});
