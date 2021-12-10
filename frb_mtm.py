def frb_mtm(valuation_date, maturity_date, coupon_rate,compounding_freq, market_price, face_value, guess=0.05):
    import QuantLib as ql
    import pandas as pd
    import numpy as np
    import scipy.optimize as optimize
    
    ql.Settings.instance().evaluationDate = effective_date
    calendar = ql.SouthAfrica()
    business_convention = ql.Following
    termination_business_convention = ql.Unadjusted
    date_generation = ql.DateGeneration.Backward
    month_end = False
    tenor = ql.Period(compounding_freq)
    compounding_freq = float(compounding_freq)
    coupon = coupon_rate*face_value/compounding_freq
    
    schedule = ql.Schedule (valuation_date, maturity_date, tenor, calendar, business_convention, termination_business_convention, date_generation, month_end)
    dt = pd.DataFrame({'cashflow_date': list(schedule)})
    dt = ((dt['cashflow_date'] - dt['cashflow_date'].iloc[0])/365)[1:]
    T = dt.iloc[-1]
    
    ytm_func = lambda y : sum([coupon/(1+y/compounding_freq)**(compounding_freq*t) for t in dt]) + face_value/(1+y/compounding_freq)**(compounding_freq*T) - market_price
    ytm = optimize.newton(ytm_func, guess)
    
    # Duration
    duration = (sum([coupon/(1+ytm/compounding_freq)**(compounding_freq*t)*t for t in dt]) + face_value/(1+ytm/compounding_freq)**(compounding_freq*T)*T )/ market_price
    
    # Modified Duration
    modified_duration = duration/(1+y/compounding_freq)
    
    #Convexity
    convexity = (sum([coupon/(1+ytm/compounding_freq)**(compounding_freq*t)*t**2 for t in dt]) + face_value/(1+ytm/compounding_freq)**(compounding_freq*T)*T**2 )/ market_price
    
    return ytm, duration,modified_duration,convexity
