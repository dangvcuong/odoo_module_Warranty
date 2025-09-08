from odoo import models, fields
class ProductTemplate(models.Model):
    _inherit = 'product.template'

    warranty_period = fields.Integer(string="Warranty (Months)", default=12)