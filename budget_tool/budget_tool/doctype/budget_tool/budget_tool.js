frappe.ui.form.on("Budget Tool", {
    refresh: function (frm) {
        // Add custom button to refresh consumed amount
        frm.add_custom_button(__("Refresh Consumed Amount"), function () {
            frappe.call({
                method: "budget_tool.budget_tool.utils.refresh_consumed_amount",
                args: {
                    fiscal_year: frm.doc.custom_fiscal_year,
                    company: frm.doc.custom_company,
                    account: frm.doc.custom_accounts,
                },
                callback: function (r) {
                    if (!r.exc) {
                        frm.reload_doc();
                        frappe.msgprint(__("Consumed Amount updated successfully"));
                    }
                },
            });
        });

        // Set fiscal year and company as mandatory
        frm.set_df_property("custom_fiscal_year", "reqd", 1);
        frm.set_df_property("custom_company", "reqd", 1);
        frm.set_df_property("custom_accounts", "reqd", 1);
        frm.set_df_property("custom_total_budget", "reqd", 1);
    },

    custom_fiscal_year: function (frm) {
        // Validate fiscal year
        if (frm.doc.custom_fiscal_year) {
            frappe.db.get_value(
                "Fiscal Year",
                frm.doc.custom_fiscal_year,
                "name",
                function (r) {
                    if (!r.name) {
                        frappe.msgprint(
                            __("Fiscal Year {0} does not exist", [
                                frm.doc.custom_fiscal_year,
                            ])
                        );
                        frm.set_value("custom_fiscal_year", "");
                    }
                }
            );
        }
    },

    custom_company: function (frm) {
        // Validate company
        if (frm.doc.custom_company) {
            frappe.db.get_value(
                "Company",
                frm.doc.custom_company,
                "name",
                function (r) {
                    if (!r.name) {
                        frappe.msgprint(
                            __("Company {0} does not exist", [frm.doc.custom_company])
                        );
                        frm.set_value("custom_company", "");
                    }
                }
            );
        }
    },

    custom_accounts: function (frm) {
        // Validate account
        if (frm.doc.custom_accounts) {
            frappe.db.get_value(
                "Account",
                frm.doc.custom_accounts,
                "name",
                function (r) {
                    if (!r.name) {
                        frappe.msgprint(
                            __("Account {0} does not exist", [frm.doc.custom_accounts])
                        );
                        frm.set_value("custom_accounts", "");
                    }
                }
            );
        }
    },
});