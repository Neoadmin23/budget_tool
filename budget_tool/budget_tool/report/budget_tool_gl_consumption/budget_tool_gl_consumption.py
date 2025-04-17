import frappe

def execute(filters=None):
    # Initialize filters if None
    if not filters:
        filters = {}

    # Default values for optional filters
    fiscal_year = filters.get("fiscal_year")
    company = filters.get("company")
    account = filters.get("account")

    columns = [
        {"label": "Budget Tool", "fieldname": "budget_tool", "fieldtype": "Link", "options": "Budget Tool", "width": 120},
        {"label": "Account", "fieldname": "account", "fieldtype": "Link", "options": "Account", "width": 150},
        {"label": "Fiscal Year", "fieldname": "fiscal_year", "fieldtype": "Link", "options": "Fiscal Year", "width": 100},
        {"label": "Month", "fieldname": "month", "fieldtype": "Data", "width": 100},
        {"label": "Monthly Budget", "fieldname": "monthly_budget", "fieldtype": "Currency", "width": 120},
        {"label": "Consumed Amount", "fieldname": "consumed_amount", "fieldtype": "Currency", "width": 120},
        {"label": "Remaining Budget", "fieldname": "remaining_budget", "fieldtype": "Currency", "width": 120},
        {"label": "Rollover Amount", "fieldname": "rollover_amount", "fieldtype": "Currency", "width": 120},
        {"label": "GL Expenses", "fieldname": "gl_expenses", "fieldtype": "Currency", "width": 120},
    ]

    query = """
        SELECT
            bt.name as budget_tool,
            bt.custom_accounts as account,
            bt.custom_fiscal_year as fiscal_year,
            mb.month,
            mb.monthly_budget,
            mb.consumed_amount,
            mb.remaining_budget,
            mb.rollover_amount,
            (SELECT SUM(debit - credit)
             FROM `tabGL Entry` gle
             WHERE gle.account = bt.custom_accounts
             AND MONTHNAME(gle.posting_date) = mb.month
             AND gle.fiscal_year = bt.custom_fiscal_year
             AND gle.docstatus = 1) as gl_expenses
        FROM
            `tabBudget Tool` bt
        LEFT JOIN
            `tabMonthly Budget` mb ON mb.parent = bt.name
        WHERE
            bt.docstatus = 1
            AND bt.custom_fiscal_year = %s
            AND bt.custom_company = %s
            AND (%s IS NULL OR bt.custom_accounts = %s)
        ORDER BY
            bt.custom_accounts, FIELD(mb.month, 'January', 'February', 'March', 'April', 'May', 'June', 
                                     'July', 'August', 'September', 'October', 'November', 'December')
    """

    # Pass filter values, ensuring account is None if not provided
    data = frappe.db.sql(query, (fiscal_year, company, account, account), as_dict=True)
    return columns, data