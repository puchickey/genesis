import glob
import csv
import os
import sys

# Path provided by user
DATA_DIR = r"G:\マイドライブ\Genesis_OS\10_Domains\02_LifeBase\00_維持活動\Moneyforward入出金データ_2025"

def to_int(val):
    try:
        return int(val)
    except:
        return 0

def analyze_expenses():
    csv_files = glob.glob(os.path.join(DATA_DIR, "*.csv"))
    
    if not csv_files:
        print(f"No CSV files found in {DATA_DIR}")
        return

    # Accumulators
    cat_large = {}
    cat_mid = {}
    
    total_records = 0
    all_dates = []

    for f in csv_files:
        try:
            with open(f, 'r', encoding='shift_jis', errors='replace') as csvfile:
                # Skip to header? (MF CSV usually starts directly or has 1 line)
                # Let's read header
                reader = csv.reader(csvfile)
                header = next(reader, None)
                
                if not header: continue
                
                # Find indices
                try:
                    idx_calc = header.index("計算対象")
                    idx_date = header.index("日付")
                    idx_amount = header.index("金額（円）")
                    idx_large = header.index("大項目")
                    idx_mid = header.index("中項目")
                    idx_cont = header.index("内容")
                except ValueError as e:
                    print(f"Skipping {f}: Missing column {e}")
                    continue

                for row in reader:
                    if len(row) <= idx_amount: continue
                    
                    # 1. Filter: Calc Target
                    if row[idx_calc].strip() == "0": continue
                    
                    # 2. Filter: Amount (Expenses are negative)
                    try:
                        amount = int(row[idx_amount])
                    except:
                        continue
                        
                    if amount >= 0: continue # Skip Income
                    
                    # Store Date
                    all_dates.append(row[idx_date])
                    
                    # Abs amount for summing
                    abs_amount = abs(amount)
                    
                    large = row[idx_large]
                    mid = row[idx_mid]
                    content = row[idx_cont]
                    
                    # Exclude Investment keywords locally if needed, but let's see RAW first.
                    # Usually "振替" (Transfer) needs filtering if it appears as negative?
                    # MF usually handles transfers distinctly, but let's assume calc=1 && neg is expense.
                    
                    if large not in cat_large: cat_large[large] = 0
                    cat_large[large] += abs_amount
                    
                    key_mid = (large, mid)
                    if key_mid not in cat_mid: cat_mid[key_mid] = 0
                    cat_mid[key_mid] += abs_amount
                    
                    total_records += 1

        except Exception as e:
            print(f"Error reading {f}: {e}")

    if not all_dates:
        print("No expense records found.")
        return

    # Sort dates to find duration
    all_dates.sort()
    # Simple Date parse (YYYY-MM-DD or YYYY/MM/DD)
    start_str = all_dates[0]
    end_str = all_dates[-1]
    
    # Very rough Month calc without datetime lib dependencies if possible, 
    # but standard lib datetime is fine.
    from datetime import datetime
    try:
        start_dt = datetime.strptime(start_str.replace('/', '-'), "%Y-%m-%d")
        end_dt = datetime.strptime(end_str.replace('/', '-'), "%Y-%m-%d")
        months = (end_dt - start_dt).days / 30.41 + 1 # +1 to include first month roughly
        if months < 1: months = 1
    except:
        months = 1
        print("Date parse error, assuming 1 month")

    print(f"Analysis Period: {start_str} to {end_str} (approx {months:.1f} months)")
    
    # Output Large
    sorted_large = sorted(cat_large.items(), key=lambda x: x[1], reverse=True)
    print("\n--- Monthly Expense Breakdown (Large Category) ---")
    for k, v in sorted_large:
        avg = int(v / months)
        print(f"{k}: {avg:,} JPY")

    # Output Mid
    sorted_mid = sorted(cat_mid.items(), key=lambda x: x[1], reverse=True)
    print("\n--- Detailed Breakdown (Top 20) ---")
    for (l, m), v in sorted_mid[:20]:
        avg = int(v / months)
        print(f"{l} - {m}: {avg:,} JPY")

    # Deep Dive: Housing
    print("\n--- Deep Dive: 住宅 (Housing) ---")
    housing_details = {}
    
    # Re-scan for details (inefficient but safe)
    # Or just track it in main loop next time, but let's re-open specific for clarity in this one-off script
    # actually, let's just use the main loop if we modify it, but re-reading is easier for now to keep logic simple.
    
    for f in csv_files:
        try:
            with open(f, 'r', encoding='shift_jis', errors='replace') as csvfile:
                reader = csv.reader(csvfile)
                header = next(reader, None)
                if not header: continue
                
                try:
                    idx_calc = header.index("計算対象")
                    idx_amount = header.index("金額（円）")
                    idx_large = header.index("大項目")
                    idx_cont = header.index("内容")
                except: continue

                for row in reader:
                    if len(row) <= idx_amount: continue
                    if row[idx_calc].strip() == "0": continue
                    try: 
                        amt = int(row[idx_amount])
                    except: continue
                    
                    if amt >= 0: continue
                    
                    if row[idx_large] == "住宅":
                        cont = row[idx_cont]
                        if cont not in housing_details: housing_details[cont] = 0
                        housing_details[cont] += abs(amt)
        except: pass

    for cont, total in sorted(housing_details.items(), key=lambda x: x[1], reverse=True):
        avg = int(total / months)
        print(f"Content: {cont} -> {avg:,} JPY/mo")

if __name__ == "__main__":
    analyze_expenses()
