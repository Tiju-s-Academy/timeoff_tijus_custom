from odoo import models, fields, api, _
from odoo.exceptions import ValidationError

class HrLeaveType(models.Model):
    _inherit = 'hr.leave.type'

    sandwich_leave = fields.Boolean(string='Sandwich Leave', default=False)

class HrLeave(models.Model):
    _inherit = 'hr.leave'

    # ...existing code...

    @api.constrains('date_from', 'date_to', 'employee_id')
    def _check_sandwich_leave(self):
        for leave in self:
            if leave.holiday_status_id.sandwich_leave:
                # Get all leaves for the employee
                leaves = self.search([
                    ('employee_id', '=', leave.employee_id.id),
                    ('state', '=', 'validate'),
                    ('date_from', '>=', leave.date_from),
                    ('date_to', '<=', leave.date_to)
                ])
                # Check for weekends and holidays between leaves
                for day in range((leave.date_to - leave.date_from).days + 1):
                    current_day = leave.date_from + timedelta(days=day)
                    if current_day.weekday() in (6) or self.env['resource.calendar.leaves'].search([('date', '=', current_day)]):
                        if not any(l.date_from <= current_day <= l.date_to for l in leaves):
                            raise ValidationError(_('Sandwich leave policy violated.'))

    # ...existing code...
