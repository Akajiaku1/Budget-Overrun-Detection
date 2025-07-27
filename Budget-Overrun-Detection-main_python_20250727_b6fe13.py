class Budget:
    def __init__(self, category: str, allocated_amount: float):
        self.category = category
        self.allocated = allocated_amount
        self.transactions = []
        # Record initial allocation as a starting transaction
        self.add_transaction('initial', allocated_amount, "Initial allocation")

    def add_transaction(self, transaction_type: str, amount: float, description: str):
        if amount <= 0:
            raise ValueError("Amount must be positive")
        self.transactions.append({
            'type': transaction_type,
            'amount': amount,
            'description': description
        })
    
    def add_income(self, amount: float, description: str):
        self.add_transaction('income', amount, description)
    
    def add_expense(self, amount: float, description: str):
        self.add_transaction('expense', amount, description)
    
    def calculate_balance(self) -> float:
        """Calculate current balance (allocated + income - expenses)"""
        total_income = sum(
            t['amount'] for t in self.transactions 
            if t['type'] in ('initial', 'income')
        )
        total_expenses = sum(
            t['amount'] for t in self.transactions 
            if t['type'] == 'expense'
        )
        return total_income - total_expenses
    
    def check_overrun(self) -> bool:
        """Check if expenses exceed allocated budget"""
        total_expenses = sum(
            t['amount'] for t in self.transactions 
            if t['type'] == 'expense'
        )
        return total_expenses > self.allocated
    
    def generate_report(self) -> str:
        """Generate budget status report"""
        balance = self.calculate_balance()
        total_expenses = sum(t['amount'] for t in self.transactions if t['type'] == 'expense')
        overrun = total_expenses - self.allocated
        
        report = [
            f"Budget Category: {self.category}",
            f"Allocated Amount: ${self.allocated:.2f}",
            f"Total Expenses: ${total_expenses:.2f}",
            f"Current Balance: ${balance:.2f}",
        ]
        
        if self.check_overrun():
            report.append(f"⚠️ BUDGET OVERRUN! Exceeded by ${overrun:.2f}")
        else:
            report.append(f"Remaining Budget: ${self.allocated - total_expenses:.2f}")
        
        return "\n".join(report)

    def get_transactions(self) -> list:
        """Get all transactions in chronological order"""
        return self.transactions.copy()

# Example Usage
if __name__ == "__main__":
    # Create a new budget for marketing
    marketing_budget = Budget("Marketing", 5000.00)
    
    # Add income and expenses
    marketing_budget.add_income(200.00, "Sponsorship")
    marketing_budget.add_expense(1500.00, "Google Ads")
    marketing_budget.add_expense(800.00, "Social Media Campaign")
    marketing_budget.add_expense(3000.00, "Influencer Partnership")
    
    # Check status and detect overruns
    print(marketing_budget.generate_report())
    print("\nTransaction History:")
    for i, t in enumerate(marketing_budget.get_transactions(), 1):
        print(f"{i}. {t['type'].title()}: ${t['amount']:.2f} - {t['description']}")