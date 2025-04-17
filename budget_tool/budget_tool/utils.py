import frappe

@frappe.whitelist()
def refresh_consumed_amount(fiscal_year, company, account=None):
    filters = {
        "custom_fiscal_year": fiscal_year,
        "custom_company": company,
        "docstatus": 1
    }
    if account:
        filters["custom_accounts"] = account
    
    budgets = frappe.get_all("Budget Tool", filters=filters)
    for budget in budgets:
        budget_doc = frappe.get_doc("Budget Tool", budget.name)
        budget_doc.update_consumed_amount()
        budget_doc.save()
    return True

def update_budget_consumed_amount(doc, method):
    for account in doc.accounts:
        budgets = frappe.get_all("Budget Tool", filters={
            "custom_accounts": account.account,
            "custom_fiscal_year": doc.fiscal_year,
            "docstatus": 1
        })
        for budget in budgets:
            budget_doc = frappe.get_doc("Budget Tool", budget.name)
            month = frappe.utils.getdate(doc.posting_date).strftime("%B")
            expenses = frappe.db.sql("""
                SELECT SUM(debit - credit) as total
                FROM `tabGL Entry`
                WHERE account = %s
                AND MONTHNAME(posting_date) = %s
                AND fiscal_year = %s
                AND docstatus = 1
            """, (budget_doc.custom_accounts, month, budget_doc.custom_fiscal_year), as_dict=True)
            for row in budget_doc.monthly_budgets:
                if row.month == month:
                    row.consumed_amount = expenses[0].total or 0
                    row.remaining_budget = row.monthly_budget - row.consumed_amount
            budget_doc.save()