# -*- coding: utf-8 -*-
from datetime import timedelta
from odoo import models, fields

class HrLeave(models.Model):
    _inherit = 'hr.leave'

    sandwich_leave = fields.Boolean(string='Apply Sandwich Rule', default=True)

    def _compute_duration(self):
        leave_dates_cache = {}
        non_working_days_cache = {}
        
        for leave in self:
            if leave.sandwich_leave:
                leave_duration = (leave.request_date_to - leave.request_date_from).days + 1
                leave_period = (leave.request_date_from, leave.request_date_to)
                
                if leave_period not in leave_dates_cache:
                    # Get all dates in the leave period
                    leave_dates_cache[leave_period] = set(
                        leave.request_date_from + timedelta(days=i)
                        for i in range((leave.request_date_to - leave.request_date_from).days + 1)
                    )
                
                leave_dates = leave_dates_cache[leave_period]
                
                if leave_period not in non_working_days_cache:
                    # Fetch non-working days using the employee's calendar
                    calendar = leave.employee_id.resource_calendar_id
                    non_working_days_cache[leave_period] = calendar._get_non_working_days(leave.request_date_from, leave.request_date_to)
                
                non_working_days = non_working_days_cache[leave_period]

                # Calculate effective leave days
                effective_days = leave_dates - non_working_days
                leave.number_of_days = len(effective_days)
            else:
                super()._compute_duration()
