from odoo import http
from odoo.http import request

class WarrantyDashboardController(http.Controller):

    @http.route('/warranty/dashboard/data', type='json', auth='user')
    def get_dashboard_data(self):
        records = request.env['warranty.record'].sudo()
        return {
            'active': records.search_count([('state', '=', 'active')]),
            'expiring': records.search_count([('state', '=', 'expiring')]),
            'expired': records.search_count([('state', '=', 'expired')]),
        }
