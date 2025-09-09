/** @odoo-module **/

import {registry} from "@web/core/registry";
import {useService} from "@web/core/utils/hooks";
import {Component, onWillStart} from "@odoo/owl";
import {rpc} from "@web/core/network/rpc";

class WarrantyDashboard extends Component {
    static template = "warranty_management.WarrantyDashboard";

    setup() {
        this.orm = useService("orm");
        this.counts = {active: 0, expiring: 0, expired: 0};

        onWillStart(async () => {
            this.counts = await rpc("/warranty/dashboard/data", {});
        });
    }
}

registry.category("actions").add("warranty_dashboard", WarrantyDashboard);

