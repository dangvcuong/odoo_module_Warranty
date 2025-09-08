from odoo import models, fields
from datetime import timedelta


class StockPicking(models.Model):
    _inherit = 'stock.picking'

    warranty_mumber_id = fields.Many2one('warranty.record', string="Warranty Number", readonly=True)

    def button_validate(self):
        res = super().button_validate()
        for picking in self:
            if picking.picking_type_id.code == 'outgoing':
                warranty = False
                for move in picking.move_ids:
                    warranty_months = move.product_id.warranty_period or 12
                    start_date = fields.Date.today()
                    end_date = start_date + timedelta(days=warranty_months * 30)
                    w = self.env['warranty.record'].create({
                        'partner_id': picking.partner_id.id,
                        'product_id': move.product_id.id,
                        'picking_id': picking.id,
                        'start_date': start_date,
                        'end_date': end_date,
                    })
                    if not warranty:
                        warranty = w
                if warranty:
                    picking.warranty_mumber_id = warranty.id
        return res
