# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError

class ProjectTaskOptimizer(models.Model):
    _name = "project.task.optimizer"
    _description = "Advanced Task Optimizer"
    _order = "sequence, id desc"
    _check_company_auto = True

    name = fields.Char(string="Title", required=True)
    sequence = fields.Integer(string="Sequence", default=10)
    state = fields.Selection([
        ('draft', 'Draft'),
        ('progress', 'In Progress'),
        ('done', 'Completed')
    ], string="State", default="draft", required=True)
    
    company_id = fields.Many2one(
        'res.company', string="Company", 
        default=lambda self: self.env.company, required=True
    )
    
    partner_id = fields.Many2one(
        'res.partner', string="Customer", 
        check_company=True, index="btree"
    )
    
    estimated_hours = fields.Float(string="Estimated Hours")
    discount_rate = fields.Float(string="Discount Rate", default=0.0)
    
    cost_total = fields.Monetary(
        compute="_compute_cost_total", 
        currency_field="currency_id", 
        store=True
    )
    
    currency_id = fields.Many2one(
        'res.currency', related="company_id.currency_id", store=True
    )

    # Odoo 19 modern naming computed display_name
    @api.depends('name', 'state')
    def _compute_display_name(self):
        for record in self:
            state_label = dict(self._fields['state'].selection(self)).get(record.state, '')
            record.display_name = f"[{state_label.upper()}] {record.name}"

    # Stored computed field with precise dependencies
    @api.depends('estimated_hours', 'discount_rate')
    def _compute_cost_total(self):
        for record in self:
            base_rate = 50.0
            net_rate = base_rate * (1.0 - (record.discount_rate / 100.0))
            record.cost_total = record.estimated_hours * net_rate

    # Database-level constraint validation
    @api.constrains('estimated_hours', 'discount_rate')
    def _check_task_values(self):
        for record in self:
            if record.estimated_hours <= 0:
                raise ValidationError(_("Estimated hours must be strictly positive."))
            if not (0.0 <= record.discount_rate <= 100.0):
                raise ValidationError(_("Discount rate must be between 0% and 100%."))

    # Batch creation support
    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if not vals.get('name'):
                vals['name'] = _("Untitled Task")
        return super(ProjectTaskOptimizer, self).create(vals_list)

    # Safe delete prevention
    @api.ondelete(at_uninstall=False)
    def _prevent_done_deletion(self):
        for record in self:
            if record.state == 'done':
                raise ValidationError(_("You cannot delete completed records."))\n