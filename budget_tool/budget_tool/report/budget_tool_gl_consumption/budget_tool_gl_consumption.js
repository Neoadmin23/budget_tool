frappe.query_reports["Budget Tool GL Consumption"] = {
    "filters": [
        {
            "fieldname": "fiscal_year",
            "label": __("Fiscal Year"),
            "fieldtype": "Link",
            "options": "Fiscal Year",
            "reqd": 1,
            "default": frappe.defaults.get_user_default("fiscal_year")
        },
        {
            "fieldname": "company",
            "label": __("Company"),
            "fieldtype": "Link",
            "options": "Company",
            "reqd": 1,
            "default": frappe.defaults.get_user_default("company")
        },
        {
            "fieldname": "account",
            "label": "Account",
            "fieldtype": "Link",
            "options": "Account",
            "reqd": 0
        }
    ],
    "formatter": function(value, row, column, data, default_formatter) {
        if (column.fieldname === "consumed_amount" && data.consumed_amount !== data.gl_expenses) {
            return `<span style="color: red;">${value}</span>`;
        }
        return default_formatter(value, row, column, data);
    },
    "onload": function(report) {
        report.page.add_inner_button(__("Refresh Consumed Amount"), function() {
            frappe.call({
                method: "budget_tool.budget_tool.utils.refresh_consumed_amount",
                args: {
                    fiscal_year: report.get_values().fiscal_year,
                    company: report.get_values().company,
                    account: report.get_values().account
                },
                callback: function(r) {
                    if (r.message) {
                        frappe.msgprint(__("Consumed Amount updated successfully"));
                        report.refresh();
                    }
                }
            });
        });
    }
};