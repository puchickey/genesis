import locale

# Simulation Parameters
INITIAL_ASSET = 14735674
CURRENT_AGE = 32
RETIREMENT_AGE = 60
PENSION_START_AGE = 65
DEATH_AGE = 90

# Economic Assumptions
INFLATION_RATE = 0.015
ROI_RATE = 0.04

# Income Assumption (Net)
# Based on 2025 Actuls (3.37M)
ANNUAL_NET_INCOME_BASE = 3370000 

# Pension Assumption
# Conservative: 120k/mo = 1.44M/year
ANNUAL_PENSION = 1440000

# Scenarios
SCENARIOS = {
    "A1: Survival (200k/mo)": {
        "monthly_cost": 200000,
        "description": "Basic Living + Rent Hike Buffer"
    },
    "A2: Comfort (250k/mo)": {
        "monthly_cost": 250000,
        "description": "With Cat, Better Rent, Travel"
    }
}

def simulate(scenario_name, params):
    asset = INITIAL_ASSET
    base_annual_cost = params["monthly_cost"] * 12
    
    print(f"\n--- Simulation: {scenario_name} ---")
    print(f"Initial Asset: {asset:,.0f}")
    print(f"Initial Annual Cost: {base_annual_cost:,.0f}")
    
    survival = True
    
    for age in range(CURRENT_AGE, DEATH_AGE + 1):
        # 1. Asset Growth (Start of Year)
        asset = asset * (1 + ROI_RATE)
        
        # 2. Income
        income = 0
        if age < RETIREMENT_AGE:
            income += ANNUAL_NET_INCOME_BASE
        if age >= PENSION_START_AGE:
            income += ANNUAL_PENSION
            
        # 3. Cost (Inflated)
        year_index = age - CURRENT_AGE
        current_cost = base_annual_cost * ((1 + INFLATION_RATE) ** year_index)
        
        # 4. Balance
        cashflow = income - current_cost
        asset += cashflow
        
        # Check Bankruptcy
        if asset < 0:
            print(f"!! BANKRUPTCY at Age {age} !! (Asset: {asset:,.0f})")
            survival = False
            break
            
        if age in [40, 50, 60, 65, 70, 80, 90]:
            print(f"Age {age}: Asset = {asset:,.0f} | In: {income:,.0f} Out: {current_cost:,.0f}")
            
    if survival:
        print(f"SUCCESS! Survived until {DEATH_AGE}. Final Asset: {asset:,.0f}")
    
    return survival, asset

if __name__ == "__main__":
    results = {}
    for name, params in SCENARIOS.items():
        survived, end_asset = simulate(name, params)
        results[name] = end_asset if survived else 0
