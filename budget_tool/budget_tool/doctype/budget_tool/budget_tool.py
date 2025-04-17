import frappe
from frappe.model.document import Document


class BudgetTool(Document):
    def validate(self):
        total_monthly = sum([d.monthly_budget for d in self.monthly_budgets])
        if total_monthly > self.custom_total_budget:
            frappe.throw(
                f"Total monthly budgets ({total_monthly}) exceed the total budget ({self.custom_total_budget})"
            )

        self.update_consumed_amount()

        months = [
            "January",
            "February",
            "March",
            "April",
            "May",
            "June",
            "July",
            "August",
            "September",
            "October",
            "November",
            "December",
        ]
        previous_rollover = 0
        for i, row in enumerate(self.monthly_budgets):
            row.consumed_amount = row.consumed_amount or 0
            row.remaining_budget = (
                row.monthly_budget + previous_rollover - row.consumed_amount
            )
            row.rollover_amount = row.remaining_budget if row.remaining_budget > 0 else 0
            previous_rollover = row.rollover_amount
            frappe.log_error(
                f"Month: {row.month}, Monthly Budget: {row.monthly_budget}, "
                f"Consumed: {row.consumed_amount}, Remaining: {row.remaining_budget}, "
                f"Rollover: {row.rollover_amount}",
                "Budget Tool Debug",
            )

    def update_consumed_amount(self):
        months = [row.month for row in self.monthly_budgets]
        if not months:
            return

        expenses = frappe.db.sql(
            """
            SELECT MONTHNAME(posting_date) as month, SUM(debit - credit) as total
            FROM `tabGL Entry`
            WHERE account = %s
            AND MONTHNAME(posting_date) IN %s
            AND fiscal_year = %s
            AND docstatus = 1
            GROUP BY MONTHNAME(posting_date)
        """,
            (self.custom_accounts, tuple(months), self.custom_fiscal_year),
            as_dict=True,
        )

        expense_dict = {exp.month: exp.total for exp in expenses}
        for row in self.monthly_budgets:
            row.consumed_amount = expense_dict.get(row.month, 0)
            frappe.log_error(
                f"Account: {self.custom_accounts}, Month: {row.month}, "
                f"Consumed Amount: {row.consumed_amount}",
                "Consumed Amount Debug",
            )

    def on_submit(self):
        self.update_consumed_amount()
        self.save()