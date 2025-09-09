from odoo import models, fields, api, _
from datetime import timedelta
from collections import defaultdict

class WarrantyRecord(models.Model):
    _name = 'warranty.record'
    _description = 'Warranty Record'
    _inherit = ['portal.mixin', 'mail.thread']

    name = fields.Char(string="Coupon code", required=True, copy=False, default="New")
    partner_id = fields.Many2one('res.partner', string="Customer", required=True, readonly=True)
    product_id = fields.Many2one('product.product', string="Product", required=True, readonly=True)
    picking_id = fields.Many2one('stock.picking', string="Delivery Order", readonly=True)
    start_date = fields.Date(string="Start Date", required=True)
    end_date = fields.Date(string="End Date", required=True)
    state = fields.Selection([
        ('active', 'Active'),
        ('expiring', 'Expiring Soon'),
        ('expired', 'Expired')
    ], string="Status", compute="_compute_state", store=True, default='active')

    def action_print_warranty(self):
        return self.env.ref('warranty_management.action_request_report_warranty').report_action(self)

    @api.depends('start_date', 'end_date')
    def _compute_state(self):
        today =  fields.Date.today()
        for record in self:
            if record.end_date and record.end_date < today:
                record.state = 'expired'
            elif today <= record.end_date <= today + timedelta(days=7):
                record.state = 'expiring'
            else:
                record.state = 'active'

    def update_state_cron(self):
        today =  fields.Date.today()
        records = self.search([])
        if not records:
            return

        records._compute_state()

        warrantys_overdue = records.filtered(lambda t: t.end_date < today)
        warrantys_near_deadline = records.filtered(lambda t: today <= t.end_date <= today + timedelta(days=7))

        if warrantys_near_deadline or warrantys_overdue:
            self.send_expiring_email(warrantys_near_deadline, warrantys_overdue)

    def send_expiring_email(self, expiring_records, expired_records):
        if not expiring_records and not expired_records:
            return

        # Gom dữ liệu theo customer
        grouped_records = defaultdict(lambda: self.env['warranty.record'])
        all_records = expiring_records | expired_records

        for rec in all_records:
            grouped_records[rec.partner_id] |= rec

        if not grouped_records:
            return

        template = self.env['ir.qweb']
        odoobot_user = self.env.ref('base.partner_root')

        for partner, records in grouped_records.items():
            expiring_list, expired_list = [], []

            for rec in records:
                record_info = {
                    'product_name': rec.product_id.display_name,
                    'end_date': rec.end_date.strftime('%d/%m/%Y'),
                    'partner_name': rec.partner_id.name,
                }
                if rec in expiring_records:
                    expiring_list.append(record_info)
                elif rec in expired_records:
                    expired_list.append(record_info)

            # Render template
            body_html = template._render(
                'warranty_management.warranty_expiry_warning_template',
                values={
                    'expiring_records': expiring_list,
                    'expired_records': expired_list,
                }
            )

            # Gửi email
            if partner.email:
                self.env['mail.mail'].create({
                    'subject': _("[Warning] Product warranty information"),
                    'body_html': body_html,
                    'email_from': self.env.user.email,
                    'email_to': partner.email,
                }).send()

            # Gửi Discuss message tới chuyên viên sale
            if partner.user_id:
                channel_info = self.env['discuss.channel'].channel_get([odoobot_user.id, partner.user_id.partner_id.id])
                channel = self.env['discuss.channel'].browse(channel_info["id"])
                channel.message_post(
                    body=body_html,
                    author_id=odoobot_user.id,
                    message_type='comment',
                    subtype_xmlid='mail.mt_comment',
                )

    @api.model
    def create(self, vals):
        if vals.get('name', 'New') == 'New':
            vals['name'] = self.env['ir.sequence'].next_by_code('warranty.record') or 'New'
        return super().create(vals)
