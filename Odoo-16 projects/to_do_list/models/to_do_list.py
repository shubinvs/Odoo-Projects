from odoo import fields, models, api


class ToDoList(models.Model):
    _name = "to.do.list"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = "To Do List"
    _rec_name = 'summary'

    priority = fields.Selection([
        ('1', 'low'),
        ('2', 'medium'),
        ('3', 'high'),
        ('4', 'very high')
    ])
    user_id = fields.Many2one(
        'res.users', string='Salesperson')
    activity_type = fields.Many2one('mail.activity')
    summary = fields.Char(string="Summary")
    due_date = fields.Date(string="Due Date", required=True)
    recurring = fields.Boolean(string="Recurring")
    recurring_period = fields.Selection(selection=[('daily', 'Daily'),
                                                   ('weekly', 'Weekly'),
                                                   ('monthly', 'Monthly')])
    next_recurring_date = fields.Date(string="Next Recurring")
    notes = fields.Html(help="Type something here!!!!!!")
    state = fields.Selection(selection=[('planned', 'Planned'),
                                        ('today', 'Today'),
                                        ('expired', 'Expired'),
                                        ('done', 'Done'),
                                        ('cancelled', 'Cancel')])
    check = fields.Boolean(compute="_compute_state", readonly=False)

    @api.depends('due_date')
    def _compute_state(self):
        to_day = fields.date.today()
        print(to_day)
        print(self.due_date)
        try:
            if self.due_date == to_day:
                self.check = True
                if self.check:
                    self.write({'state': 'today'})
            elif self.due_date > to_day:
                self.write({'state': 'planned'})
            elif self.due_date < to_day:
                self.write({'state': 'expired'})
        except:pass

    def button_mark_as_done(self):
        self.write({'state': "done"})

    def button_cancel(self):
        self.write({'state': "cancelled"})

    @api.model
    def to_do_list(self):
        to_day = fields.date.today()
        to_do = self.search([('state', 'in', ('planned', 'today')),
                             ('next_recurring_date', '=', to_day),
                             ('recurring', '=', True)])

        for rec in to_do:
            if rec.recurring_period == 'daily':
                new_date = fields.Date.add(rec.next_recurring_date, days=1)
            elif rec.recurring_period == 'weekly':
                new_date = fields.Date.add(rec.next_recurring_date, days=7)
            elif rec.recurring_period == 'monthly':
                new_date = fields.Date.add(rec.next_recurring_date, days=30)

            self.create({
                'priority': rec.priority,
                'activity_type': rec.activity_type.id,
                'summary': rec.summary,
                'due_date': rec.due_date,
                'recurring': rec.recurring,
                'recurring_period': rec.recurring_period,
                'next_recurring_date': new_date,
                'notes': rec.notes,
                'state': rec.state
            })
            rec.state = 'done'
