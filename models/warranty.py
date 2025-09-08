from odoo import models, fields, api
from datetime import date
class WarrantyRecord(models.Model):
    _name = 'warranty.record'
    _description = 'Warranty Record'

    name = fields.Char(string="Warranty Number", required=True, copy=False, default="New")
    partner_id = fields.Many2one('res.partner', string="Customer", required=True, readonly=True)
    product_id = fields.Many2one('product.product', string="Product", required=True, readonly=True)
    picking_id = fields.Many2one('stock.picking', string="Delivery Order", readonly=True)
    start_date = fields.Date(string="Start Date", required=True)
    end_date = fields.Date(string="End Date", required=True)
    state = fields.Selection([
        ('active', 'Active'),
        ('expired', 'Expired')
    ], string="Status", compute="_compute_state", store=True, default='active')

    @api.depends('start_date', 'end_date')
    def _compute_state(self):
        today = date.today()
        for record in self:
            if record.end_date and record.end_date <= today:
                record.state = 'expired'
            else:
                record.state = 'active'


    def update_state_cron(self):
        today = date.today()
        records = self.search([])
        for record in records:
            if record.end_date and record.end_date < today:
                record.state = 'expired'
            else:
                record.state = 'active'

    @api.model
    def create(self, vals):
        if vals.get('name', 'New') == 'New':
            vals['name'] = self.env['ir.sequence'].next_by_code('warranty.record') or 'New'
        return super().create(vals)
