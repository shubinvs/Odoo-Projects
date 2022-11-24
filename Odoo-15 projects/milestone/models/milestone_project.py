from odoo import fields, models


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    milestone = fields.Integer(string='Milestone')


class ProjectProject(models.Model):
    _inherit = 'project.project'

    project_id = fields.Char(string="project id")


class ProjectTask(models.Model):
    _inherit = 'project.task'

    task_id = fields.Char(string="task id")
    milestone_id = fields.Char(string="milestone id")
    product_id = fields.Char(string="product id")


class CreateProject(models.Model):
    _inherit = 'sale.order'

    project = fields.Boolean(copy=False)

    def button_create_project(self):

        project = self.env['project.project'].create({
            'name': self.name,
            'project_id': self.id,
            'partner_id': self.partner_id.id
        })
        milestone_list = []
        for rec in self.order_line:
            milestone_list.append(rec.milestone)
        non_dup = [*set(milestone_list)]
        for non_duplicate in non_dup:
            project_id = self.env['project.project'].search(
                [('id', '=', project.id)])
            if non_duplicate:
                new = rec.env['project.task'].create({
                    'name': 'Milestone ' + str(non_duplicate),
                    'task_id': self.id,
                    'milestone_id': non_duplicate,
                    'project_id': project_id.id
                })
                for rec in self.order_line:
                    if rec.milestone == non_duplicate:
                        new.write({
                            'child_ids': [(0, 0, {
                                'name': new.name + ' - ' + rec.product_id.name,
                                'product_id': rec.product_id.id
                            })]
                        })
        self.project = True

    def button_update_project(self):
        for rec in self.order_line:
            project_exist = self.env['project.project'].search(
                [('project_id', '=', self.id)])
            record_milestone = rec.milestone
            if record_milestone:
                task_exist = self.env['project.task'].search(
                    [('milestone_id', '=', record_milestone),
                     ('project_id', '=', project_exist.id)])
                if task_exist:
                    child_exist = self.env['project.task'].search(
                        [('parent_id', '=', task_exist.name),
                         ('product_id', '=', rec.product_id.id)
                         ])
                    if not child_exist:
                        task_exist.write({
                            'child_ids': [(0, 0, {
                                'name': task_exist.name + ' - ' + rec.product_id.name,
                                'product_id': rec.product_id.id
                            })]
                        })
                else:
                    new_task = rec.env['project.task'].create({
                        'name': 'Milestone ' + str(record_milestone),
                        'task_id': self.id,
                        'milestone_id': record_milestone,
                        'project_id': project_exist.id
                    })
                    new_task.write({
                        'child_ids': [(0, 0, {
                            'name': new_task.name + ' - ' + rec.product_id.name,
                            'product_id': rec.product_id.id
                        })]
                    })

    def get_project(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'project',
            'view_mode': 'tree,form',
            'res_model': 'project.project',
            'domain': [
                ('project_id', '=', self.id)],
            'context': "{'create': False}"
        }
