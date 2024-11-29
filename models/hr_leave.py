# -*- coding: utf-8 -*-
from datetime import timedelta
from odoo import models, fields

class HrLeave(models.Model):
    _inherit = 'hr.leave'

    sandwich_leave = fields.Boolean(string='Apply Sandwich Rule', default=True)

    def _compute_duration(self):
        for leave in self:
            if leave.sandwich_leave:
                # Get all dates in the leave period
                leave_dates = set(
                    leave.request_date_from + timedelta(days=i)
                    for i in range((leave.request_date_to - leave.request_date_from).days + 1)
                )
                # Use _get_global_attendances to fetch non-working days
                non_working_days = self.env['resource.calendar']._get_global_attendances(leave.employee_id.id)
                # Calculate effective leave days
                effective_days = leave_dates - non_working_days
                leave.number_of_days = len(effective_days)
            else:
                super(HrLeave, self)._compute_duration()
