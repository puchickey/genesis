import os
import glob
import csv
import sys
from datetime import datetime
from collections import defaultdict

# Genesis Data Path
DATA_PATH = r"G:\マイドライブ\Genesis_OS\10_Domains\02_LifeBase\00_維持活動\Moneyforward入出金データ_2025"

def parse_amount(value_str):
    try:
        return int(value_str)
    except ValueError:
        return 0

def analyze_finances(path):
    all_files = glob.glob(os.path.join(path, "*.csv"))
    if not all_files:
        print(f"No CSV files found in {path}")
        return

    monthly_burn = defaultdict(int)
    housing_burn = defaultdict(int)
    large_expenses = []

    # Column Headers (Expected)
    # MoneyForward headers usually: "計算対象","日付","内容","金額（円）","保有金融機関","大項目","中項目","メモ","振替","ID"
    
    for filename in all_files:
        try:
            with open(filename, mode='r', encoding='shift_jis', errors='replace') as f:
                reader = csv.reader(f)
                header = next(reader, None)
                if not header:
                    continue

                # Identify Column Indices
                try:
                    idx_date = -1
                    idx_amount = -1
                    idx_category = -1
                    idx_content = -1

                    # Flexible search for headers
                    for i, col in enumerate(header):
                        if "日付" in col: idx_date = i
                        if "金額" in col: idx_amount = i
                        if "大項目" in col: idx_category = i
                        if "内容" in col: idx_content = i
                    
                    if idx_date == -1 or idx_amount == -1:
                        print(f"Skipping {filename}: Missing essential columns '日付' or '金額'")
                        continue

                except Exception as e:
                    print(f"Header parsing error in {filename}: {e}")
                    continue

                for row in reader:
                    if not row: continue
                    if len(row) <= idx_amount: continue

                    date_str = row[idx_date]
                    amount_str = row[idx_amount]
                    category = row[idx_category] if idx_category != -1 and len(row) > idx_category else ""
                    content = row[idx_content] if idx_content != -1 and len(row) > idx_content else ""

                    # Exclude Calculations? "計算対象" is usually col 0. '1' = Yes, '0' = No.
                    # Let's ignore this for now to catch everything, or check if user unchecked it.
                    # Usually "振替" is the big thing to exclude.

                    amount = parse_amount(amount_str)
                    
                    # Filter: Expenses only (< 0)
                    # Filter: Exclude Transfers (振替), Investments (投資)
                    if amount < 0:
                        if category in ['振替', '投資', '現金・カード']:
                            continue
                        
                        # Date parsing for Month grouping
                        try:
                            # Usually YYYY/MM/DD
                            dt = datetime.strptime(date_str, "%Y/%m/%d")
                            month_key = dt.strftime("%Y-%m")
                        except:
                            month_key = "Unknown"

                        monthly_burn[month_key] += amount
                        
                        if category == '住宅':
                            housing_burn[month_key] += amount
                        
                        # Store for Top 5 check
                        large_expenses.append({
                            'date': date_str,
                            'amount': amount,
                            'content': content,
                            'category': category
                        })

        except Exception as e:
            print(f"Error reading {filename}: {e}")

    # Output Results
    print("\n--- Monthly Burn Rate (Expenses only, No Transfer/Invest) ---")
    sorted_months = sorted(monthly_burn.keys())
    total_all = 0
    count_all = 0
    
    for m in sorted_months:
        if m == "Unknown": continue
        print(f"{m}: {monthly_burn[m]:,}")
        total_all += monthly_burn[m]
        count_all += 1
    
    if count_all > 0:
        avg = total_all / count_all
        print(f"\nAverage Monthly Burn: {avg:,.0f} JPY")
    else:
        print("\nNo expense data found.")

    print("\n--- Housing Expenses (Monthly) ---")
    for m in sorted_months:
        if m in housing_burn and housing_burn[m] != 0:
            print(f"{m}: {housing_burn[m]:,}")
    
    print("\n--- Top 10 Largest Expenses ---")
    # Sort by amount (ascending because expenses are negative)
    large_expenses.sort(key=lambda x: x['amount'])
    for x in large_expenses[:10]:
        print(f"{x['date']} : {x['amount']:,} : {x['category']} : {x['content']}")

if __name__ == "__main__":
    analyze_finances(DATA_PATH)
