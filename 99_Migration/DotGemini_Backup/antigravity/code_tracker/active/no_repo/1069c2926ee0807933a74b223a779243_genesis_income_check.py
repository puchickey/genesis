�import os
import glob
import csv
import sys
from datetime import datetime
from collections import defaultdict

DATA_PATH = r"G:\マイドライブ\Genesis_OS\10_Domains\02_LifeBase\00_維持活動\Moneyforward入出金データ_2025"

def parse_amount(value_str):
    try:
        return int(value_str)
    except ValueError:
        return 0

def analyze_income(path):
    all_files = glob.glob(os.path.join(path, "*.csv"))
    monthly_income = defaultdict(int)
    large_incomes = []

    for filename in all_files:
        try:
            with open(filename, mode='r', encoding='shift_jis', errors='replace') as f:
                reader = csv.reader(f)
                header = next(reader, None)
                if not header: continue

                idx_date = -1
                idx_amount = -1
                idx_category = -1
                idx_content = -1

                for i, col in enumerate(header):
                    if "日付" in col: idx_date = i
                    if "金額" in col: idx_amount = i
                    if "大項目" in col: idx_category = i
                    if "内容" in col: idx_content = i
                
                if idx_date == -1 or idx_amount == -1: continue

                for row in reader:
                    if not row or len(row) <= idx_amount: continue
                    amount = parse_amount(row[idx_amount])

                    # Income Analysis (> 0)
                    if amount > 0:
                        cat = row[idx_category] if idx_category != -1 else ""
                        # Exclude internal transfers (振替)
                        if cat in ['振替', '投資', '現金・カード']:
                            continue
                            
                        try:
                            dt = datetime.strptime(row[idx_date], "%Y/%m/%d")
                            month_key = dt.strftime("%Y-%m")
                            monthly_income[month_key] += amount
                            
                            large_incomes.append({
                                'date': row[idx_date],
                                'amount': amount,
                                'cat': cat,
                                'content': row[idx_content]
                            })
                        except:
                            pass

        except Exception:
            pass

    print("\n--- Monthly Income (Net, No Transfers) ---")
    sorted_months = sorted(monthly_income.keys())
    total_inc = 0
    for m in sorted_months:
        print(f"{m}: {monthly_income[m]:,}")
        total_inc += monthly_income[m]
        
    print(f"\nTotal Detected Income (2025): {total_inc:,}")
    if len(sorted_months) > 0:
        print(f"Average Monthly: {total_inc / 12:,.0f} (Assuming 12 month data)")
        
    print("\n--- Top Income Sources ---")
    large_incomes.sort(key=lambda x: x['amount'], reverse=True)
    for x in large_incomes[:10]:
         print(f"{x['date']} : {x['amount']:,} : {x['cat']} : {x['content']}")

if __name__ == "__main__":
    analyze_income(DATA_PATH)
�*cascade082Bfile:///C:/Users/puchi/Desktop/antigravity/genesis_income_check.py