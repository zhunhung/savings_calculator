# OCBC 360 Account
def ocbc(balance, expense, income, saving, invest):
	# Get the monthly interest of all components
    base_interest = 0.0005/12
    salary_interest = [0.012/12, 0.02/12]
    spend_interest = [0.003/12, 0.006/12]
    invest_interest = [0.006/12, 0.012/12]
    boost_interest = 0.01/12
    
    # Ensure at least 2k salary
    if income <2000:
        salary_interest = [0, 0]
        
    # If credit card below 500, no spend bonus
    if expense < 500:
        spend_interest = [0,0]
        
    # If no purchase of qualified product, no interest bonus
    if invest == 'No':
        invest_interest = [0,0]


    interest_earning = 0
    new_balance = balance
    for i in range(12):
    	# End of month balance
        new_balance += saving
        amt_earned = 0
        valid_balance = new_balance
        step_interest = [0.003/12, 0.006/12]

        # If increment less than $500, no step bonus
        if saving < 500:
            step_interest = [0,0]
        
        # If account balance less than 200k, no grow bonus
        grow_interest = 0.01/12
        if new_balance < 200000:
            grow_interest = 0 
        
        # If exceed 70k cap, only focus on the 70k for interest
        if new_balance > 70000:
            valid_balance = 70000

         # Interest computation for first 35k
        if valid_balance <= 35000:
            total_interest = salary_interest[0] + spend_interest[0] + step_interest[0] + grow_interest + invest_interest[0]
            amt_earned += (total_interest * valid_balance)
            amt_earned += (boost_interest * saving)
            
        # If more than 35k, split into 2 tiers
        else:
            total_interest = salary_interest[0] + spend_interest[0] + step_interest[0] + grow_interest + invest_interest[0]
            amt_earned += (total_interest * 35000)
            if i > 0:
            	# If more than 1 million, only give boost interest on the 1 million cap
                amt_earned += (boost_interest * min(saving,1000000))
            # Interest computation for second 35k
            rem_bal = valid_balance - 35000
            total_interest = salary_interest[1] + spend_interest[1] + step_interest[1] + grow_interest + invest_interest[1]
            amt_earned += (total_interest * rem_bal)
            
        # Annual base interest of 0.05%
        if i == 11:
            amt_earned += (0.0005 * new_balance)
            
        interest_earning += amt_earned
        new_balance += amt_earned
    
    return round(new_balance,2), round(interest_earning,2), round(interest_earning/new_balance*100, 2)
    
# UOB One Account
def uob(balance, expense, income, saving):
    bonus= 0

    # Determine if tier 1 or tier 2 interest
    if expense >= 500:
        bonus += 1
        if income >= 2000:
            bonus += 1
    
    new_balance = balance
    base_interest = 0.0005/12
    interest = 0.015/12
    interest_earning = 0
    bonus_interest = [0.0185/12,0.02/12,0.0215/12, 0.023/12, 0.0388/12]
    for i in range(12):
        # Assuming pay receives during first half of the month
        new_balance += saving
        amt_earned = 0
        # Minus 500 to account to roughly estimate average daily balance of the month
        valid_balance = new_balance-500

        # If above 75k cap, only focus on the 75k for interest
        if new_balance > 75000:
            valid_balance = 75000
            amt_earned += (new_balance - 75000) * base_interest
            
        # Compute respective interest for every 15k
        tiers = (valid_balance//15000) + 1
        for i in range(int(tiers)):
            deduct = min(valid_balance, 15000)
            i = min(i,4)
            if bonus == 0:
                amt_earned += (base_interest * deduct)
            elif bonus == 1:
                amt_earned += (interest * deduct)
            else:
                amt_earned += (bonus_interest[i] * deduct)
            valid_balance -= deduct
        interest_earning += amt_earned
        new_balance += amt_earned
        
    return round(new_balance,2), round(interest_earning,2), round(interest_earning/new_balance*100, 2)

# DBS Multiplier
def dbs(balance, expense, income, saving, invest, invest_amount):
    total_transac = expense + income + invest_amount

    # Respective tier interest for each transaction level
    if total_transac < 2000:
        interest = 0.0005 / 12
            
    elif total_transac < 2500:
        interest = 0.0155 / 12
        if invest == 'Yes':
            interest = 0.018 / 12
    elif total_transac < 5000:
        interest = 0.0185 / 12
        if invest == 'Yes':
            interest = 0.02/12
    elif total_transac < 15000:
        interest = 0.019/ 12
        if invest == 'Yes':
            interest = 0.022/12
    elif total_transac < 30000:
        interest = 0.02/ 12
        if invest == 'Yes':
            interest = 0.023/12
    else:
        interest = 0.0208 / 12
        if invest == 'Yes':
            interest = 0.035/12
        
    # If 0 category, base interest applies
    if (expense == 0) and (invest == 'No'):
        interest = 0.0005 / 12
    
    new_balance = balance
    interest_earning = 0
    base_interest = 0.0005
    for i in range(12):
        amt_earned = 0
        new_balance += saving

        # First 50k interest computation
        if new_balance <= 50000:
            amt_earned += (new_balance * interest)
        else:
        	# First and Next 50k interest computation
            if new_balance < 100000:
                amt_earned += (50000 * interest)
                amt_earned += ((new_balance-50000)*(base_interest / 12))
            else:
                # Only matters when more than 3 categories, not considered at the moment
                amt_earned += (50000 * interest)
                amt_earned += (50000 * (base_interest / 12))
                amt_earned += ((new_balance-100000)*(base_interest / 12))
        
        new_balance += amt_earned
        interest_earning += amt_earned
                
    return round(new_balance,2), round(interest_earning,2), round(interest_earning/new_balance*100, 2)
        
 