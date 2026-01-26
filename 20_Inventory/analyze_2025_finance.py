import glob
import csv
import os
import io

# Define the directory containing the CSV files
data_dir = r"g:\マイドライブ\Genesis_OS\10_Domains\02_LifeBase\00_維持活動\Moneyforward入出金データ_2025"
csv_files = glob.glob(os.path.join(data_dir, "*.csv"))

print(f"Found {len(csv_files)} CSV files.")

# Data storage
income_data = {} # (Large, Middle) -> amount
expense_data = {} # (Large, Middle) -> amount
large_expense_data = {} # Large -> amount
total_income = 0
total_expense = 0
dates = set()

for file in csv_files:
    try:
        # Open with shift_jis
        with open(file, mode='r', encoding='shift_jis', errors='replace') as f:
            reader = csv.reader(f)
            header = next(reader, None) # Skip header
            
            for row in reader:
                if not row: continue
                # Expected format:
                # 0: Calc Target ("1" or "0")
                # 1: Date
                # 2: Content
                # 3: Amount
                # 4: Account
                # 5: Large Cat
                # 6: Middle Cat
                
                if len(row) < 7: continue
                
                # Check calculation target
                calc_target = row[0]
                if calc_target != "1":
                    continue
                
                date_str = row[1]
                # content = row[2]
                try:
                    amount = int(row[3])
                except ValueError:
                    continue
                    
                large_cat = row[5]
                middle_cat = row[6]
                
                # Track dates for month counting
                if len(date_str) >= 7: # YYYY/MM
                    dates.add(date_str[:7])

                if amount > 0:
                    total_income += amount
                    key = (large_cat, middle_cat)
                    income_data[key] = income_data.get(key, 0) + amount
                else:
                    # Expense is negative in CSV, stick to absolute for summary
                    abs_amount = abs(amount)
                    total_expense += abs_amount
                    
                    key = (large_cat, middle_cat)
                    expense_data[key] = expense_data.get(key, 0) + abs_amount
                    
                    large_expense_data[large_cat] = large_expense_data.get(large_cat, 0) + abs_amount

    except Exception as e:
        print(f"Error reading {file}: {e}")

# Summary Output
balance = total_income - total_expense
months = len(dates)

print("-" * 30)
print(f"2025 Annual Financial Summary")
print(f"Data Months: {months} ({sorted(list(dates))})")
print("-" * 30)
print(f"Total Income:  {total_income:,.0f} JPY")
print(f"Total Expense: {total_expense:,.0f} JPY")
print(f"Net Balance:   {balance:,.0f} JPY")
print("-" * 30)

if months > 0:
    monthly_avg = total_expense / months
    print(f"Monthly Avg Expense: {monthly_avg:,.0f} JPY")
    monthly_inc = total_income / months
    print(f"Monthly Avg Income:  {monthly_inc:,.0f} JPY")
    print(f"Monthly Burn Rate:   {monthly_avg:,.0f} JPY")

print("-" * 30)
print("\nTop Expenses by Large Category:")
sorted_large = sorted(large_expense_data.items(), key=lambda x: x[1], reverse=True)
for cat, amt in sorted_large:
    avg = amt / months if months > 0 else 0
    print(f"{cat:<15}: {amt:,.0f} JPY (Avg: {avg:,.0f})")

print("-" * 30)
print("\nTop 20 Expenses by Detailed Category:")
sorted_detailed = sorted(expense_data.items(), key=lambda x: x[1], reverse=True)[:20]
for (large, middle), amt in sorted_detailed:
    avg = amt / months if months > 0 else 0
    print(f"[{large}] {middle:<15}: {amt:,.0f} JPY (Avg: {avg:,.0f})")

