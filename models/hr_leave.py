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
                # Fetch non-working days using the employee's calendar
                calendar = leave.employee_id.resource_calendar_id
                non_working_days = calendar._get_non_working_days(leave.request_date_from, leave.request_date_to)

                # Calculate effective leave days
                effective_days = leave_dates - non_working_days
                leave.number_of_days = len(effective_days)
            else:
                super(HrLeave, self)._compute_duration()
