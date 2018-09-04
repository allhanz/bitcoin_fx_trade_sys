#-----------------------------------------------------------------------
# blackscholes.py
#-----------------------------------------------------------------------
#website:https://introcs.cs.princeton.edu/python/21function/blackscholes.py.html

import sys
import math
import numpy as np
import scipy.stats as si
import sympy as sy
#from sympy.statistics as systats
from sympy import *
#-----------------------------------------------------------------------

# Return the value of the Gaussian probability function with mean 0.0
# and standard deviation 1.0 at the given x value.
class blackscholes_model:
#-----------------------------------------------------------------------

# python blackscholes.py 23.75 15.00 0.01 0.35 0.5
# 8.879159263714124   (actual =  9.10)

# $ python blackscholes.py 30.14 15.0 0.01 0.332 0.25
# 15.177462481558178   (actual = 14.50)

# Information calculated based on closing data on Monday, June 9th 2003.
#
# Microsoft:   share price:             23.75
#              strike price:            15.00
#              risk-free interest rate:  1%
#              volatility:              35%      (historical estimate)
#              time until expiration:    0.5 years
#
# GE:          share price:             30.14
#              strike price:            15.00
#              risk-free interest rate   1%
#              volatility:              33.2%    (historical estimate)
#              time until expiration     0.25 years
#
# Reference:  http://www.hoadley.net/options/develtoolsvolcalc.htm

    def phi(self,x):
        return math.exp(-x * x / 2.0) / math.sqrt(2.0 * math.pi)

    #-----------------------------------------------------------------------

    # Return the value of the Gaussian probability function with mean mu
    # and standard deviation sigma at the given x value.

    def pdf(self,x, mu=0.0, sigma=1.0):
        return self.phi((x - mu) / sigma) / sigma

    #-----------------------------------------------------------------------

    # Return the value of the cumulative Gaussian distribution function
    # with mean 0.0 and standard deviation 1.0 at the given z value.

    def Phi(self,z):
        if z < -8.0: return 0.0
        if z >  8.0: return 1.0
        total = 0.0
        term = z
        i = 3
        while total != total + term:
            total += term
            term *= z * z / float(i)
            i += 2
        return 0.5 + total * self.phi(z)

    #-----------------------------------------------------------------------

    # Return standard Gaussian cdf with mean mu and stddev sigma.
    # Use Taylor approximation.

    def cdf(self,z, mu=0.0, sigma=1.0):
        return self.Phi((z - mu) / sigma)

    #-----------------------------------------------------------------------

    # Black-Scholes formula.

    def callPrice(self,s, x, r, sigma, t):
        a = (math.log(s/x) + (r + sigma * sigma/2.0) * t) / \
            (sigma * math.sqrt(t))
        b = a - sigma * math.sqrt(t)
        return s * self.cdf(a) - x * math.exp(-r * t) * self.cdf(b)

#-----------------------------------------------------------------------

class nonDividend_Paying_Black_Scholes_model: 
###################################################################################
#website: https://aaronschlegel.me/black-scholes-formula-python.html
    """
    The Black-Scholes model was first introduced by Fischer Black and Myron Scholes in 1973 in the paper "The Pricing of Options and Corporate Liabilities". Since being published, the model has become a widely used tool by investors and is still regarded as one of the best ways to determine fair prices of options.

    The purpose of the model is to determine the price of a vanilla European call and put options (option that can only be exercised at the end of its maturity) based on price variation over time and assuming the asset has a lognormal distribution.

    Assumptions
    To determine the price of vanilla European options, several assumptions are made:

    European options can only be exercised at expiration
    No dividends are paid during the option's life
    Market movements cannot be predicted
    The risk-free rate and volatility are constant
    Follows a lognormal distribution
    Non-Dividend Paying Black-Scholes Formula
    In Black-Scholes formulas, the following parameters are defined.

    SS, the spot price of the asset at time tt
    TT, the maturity of the option. Time to maturity is defined as T−tT−t
    KK, strike price of the option
    rr, the risk-free interest rate, assumed to be constant between tt and TT
    σσ, volatility of underlying asset, the standard deviation of the asset returns
    """
########################################################################################
    def euro_vanilla_call(self,S, K, T, r, sigma):
        
        #S: spot price
        #K: strike price
        #T: time to maturity
        #r: interest rate
        #sigma: volatility of underlying asset
        
        d1 = (np.log(S / K) + (r + 0.5 * sigma ** 2) * T) / (sigma * np.sqrt(T))
        d2 = (np.log(S / K) + (r - 0.5 * sigma ** 2) * T) / (sigma * np.sqrt(T))
        
        call = (S * si.norm.cdf(d1, 0.0, 1.0) - K * np.exp(-r * T) * si.norm.cdf(d2, 0.0, 1.0))
        
        return call
    
    def euro_vanilla_put(self,S, K, T, r, sigma):
        
        #S: spot price
        #K: strike price
        #T: time to maturity
        #r: interest rate
        #sigma: volatility of underlying asset
        
        d1 = (np.log(S / K) + (r + 0.5 * sigma ** 2) * T) / (sigma * np.sqrt(T))
        d2 = (np.log(S / K) + (r - 0.5 * sigma ** 2) * T) / (sigma * np.sqrt(T))
        
        put = (K * np.exp(-r * T) * si.norm.cdf(-d2, 0.0, 1.0) - S * si.norm.cdf(-d1, 0.0, 1.0))
        
        return put
    
    def euro_vanilla(self,S, K, T, r, sigma, option = 'call'):
        
        #S: spot price
        #K: strike price
        #T: time to maturity
        #r: interest rate
        #sigma: volatility of underlying asset
        
        d1 = (np.log(S / K) + (r + 0.5 * sigma ** 2) * T) / (sigma * np.sqrt(T))
        d2 = (np.log(S / K) + (r - 0.5 * sigma ** 2) * T) / (sigma * np.sqrt(T))
        
        if option == 'call':
            result = (S * si.norm.cdf(d1, 0.0, 1.0) - K * np.exp(-r * T) * si.norm.cdf(d2, 0.0, 1.0))
        if option == 'put':
            result = (K * np.exp(-r * T) * si.norm.cdf(-d2, 0.0, 1.0) - S * si.norm.cdf(-d1, 0.0, 1.0))
            
        return result
    
    def euro_call_sym(self,S, K, T, r, sigma):
        
        #S: spot price
        #K: strike price
        #T: time to maturity
        #r: interest rate
        #sigma: volatility of underlying asset
        
        N = systats.Normal(0.0, 1.0)
        
        d1 = (sy.ln(S / K) + (r + 0.5 * sigma ** 2) * T) / (sigma * sy.sqrt(T))
        d2 = (sy.ln(S / K) + (r - 0.5 * sigma ** 2) * T) / (sigma * sy.sqrt(T))
        
        call = (S * N.cdf(d1) - K * sy.exp(-r * T) * N.cdf(d2))
        
        return call

    def euro_put_sym(self,S, K, T, r, sigma):
        
        #S: spot price
        #K: strike price
        #T: time to maturity
        #r: interest rate
        #sigma: volatility of underlying asset
        
        N = systats.Normal(0.0, 1.0)
        
        d1 = (sy.ln(S / K) + (r + 0.5 * sigma ** 2) * T) / (sigma * sy.sqrt(T))
        d2 = (sy.ln(S / K) + (r - 0.5 * sigma ** 2) * T) / (sigma * sy.sqrt(T))
        
        put = (K * sy.exp(-r * T) * N.cdf(-d2) - S * N.cdf(-d1))
        
        return put

    def sym_euro_vanilla(self,S, K, T, r, sigma, option = 'call'):
        
        #S: spot price
        #K: strike price
        #T: time to maturity
        #r: interest rate
        #sigma: volatility of underlying asset
        
        N = systats.Normal(0.0, 1.0)
        
        d1 = (sy.ln(S / K) + (r + 0.5 * sigma ** 2) * T) / (sigma * sy.sqrt(T))
        d2 = (sy.ln(S / K) + (r - 0.5 * sigma ** 2) * T) / (sigma * sy.sqrt(T))
        
        if option == 'call':
            result = (S * N.cdf(d1) - K * sy.exp(-r * T) * N.cdf(d2))
        if option == 'put':
            result = (K * sy.exp(-r * T) * N.cdf(-d2) - S * N.cdf(-d1))
            
        return result
    
class dividend_Paying_Black_Scholes_model:
    """
    For assets that pay dividends, the Black-Scholes formula is rather similar to the non-dividend paying asset formula; however, a new parameter qq, is added.

    SS, the spot price of the asset at time tt
    TT, the maturity of the option. Time to maturity is defined as T−tT−t
    KK, strike price of the option
    rr, the risk-free interest rate, assumed to be constant between tt and TT
    σσ, volatility of underlying asset, the standard deviation of the asset returns
    qq, the dividend rate of the asset. This is assumed to pay dividends at a continuous rate
    """ 
    def black_scholes_call_div(self,S, K, T, r, q, sigma):
        
        #S: spot price
        #K: strike price
        #T: time to maturity
        #r: interest rate
        #q: rate of continuous dividend paying asset 
        #sigma: volatility of underlying asset
        
        d1 = (np.log(S / K) + (r - q + 0.5 * sigma ** 2) * T) / (sigma * np.sqrt(T))
        d2 = (np.log(S / K) + (r - q - 0.5 * sigma ** 2) * T) / (sigma * np.sqrt(T))
        
        call = (S * np.exp(-q * T) * si.norm.cdf(d1, 0.0, 1.0) - K * np.exp(-r * T) * si.norm.cdf(d2, 0.0, 1.0))
        
        return call

    def black_scholes_put_div(self,S, K, T, r, q, sigma):
        
        #S: spot price
        #K: strike price
        #T: time to maturity
        #r: interest rate
        #q: rate of continuous dividend paying asset 
        #sigma: volatility of underlying asset
        
        d1 = (np.log(S / K) + (r - q + 0.5 * sigma ** 2) * T) / (sigma * np.sqrt(T))
        d2 = (np.log(S / K) + (r - q - 0.5 * sigma ** 2) * T) / (sigma * np.sqrt(T))
        
        put = (K * np.exp(-r * T) * si.norm.cdf(-d2, 0.0, 1.0) - S * np.exp(-q * T) * si.norm.cdf(-d1, 0.0, 1.0))
        
        return put

    def euro_vanilla_dividend(self,S, K, T, r, q, sigma, option = 'call'):
        #Implementation that can be used to determine the put or call option price depending on specification
        #S: spot price
        #K: strike price
        #T: time to maturity
        #r: interest rate
        #q: rate of continuous dividend paying asset 
        #sigma: volatility of underlying asset
        
        d1 = (np.log(S / K) + (r - q + 0.5 * sigma ** 2) * T) / (sigma * np.sqrt(T))
        d2 = (np.log(S / K) + (r - q - 0.5 * sigma ** 2) * T) / (sigma * np.sqrt(T))
        
        if option == 'call':
            result = (S * np.exp(-q * T) * si.norm.cdf(d1, 0.0, 1.0) - K * np.exp(-r * T) * si.norm.cdf(d2, 0.0, 1.0))
        if option == 'put':
            result = (K * np.exp(-r * T) * si.norm.cdf(-d2, 0.0, 1.0) - S * np.exp(-q * T) * si.norm.cdf(-d1, 0.0, 1.0))
            
        return result

    def black_scholes_call_div_sym(self,S, K, T, r, q, sigma):
        #Sympy Implementation of Black-Scholes with Dividend-paying asset
        #S: spot price
        #K: strike price
        #T: time to maturity
        #r: interest rate
        #q: rate of continuous dividend paying asset 
        #sigma: volatility of underlying asset
        
        N = systats.Normal(0.0, 1.0)
        
        d1 = (sy.ln(S / K) + (r - q + 0.5 * sigma ** 2) * T) / (sigma * sy.sqrt(T))
        d2 = (sy.ln(S / K) + (r - q - 0.5 * sigma ** 2) * T) / (sigma * sy.sqrt(T))
        
        call = S * sy.exp(-q * T) * N.cdf(d1) - K * sy.exp(-r * T) * N.cdf(d2)
        
        return call

    def black_scholes_call_put_sym(self,S, K, T, r, q, sigma):
        #Sympy Implementation of Black-Scholes with Dividend-paying asset

        #S: spot price
        #K: strike price
        #T: time to maturity
        #r: interest rate
        #q: rate of continuous dividend paying asset 
        #sigma: volatility of underlying asset
        
        N = systats.Normal(0.0, 1.0)
        
        d1 = (sy.ln(S / K) + (r - q + 0.5 * sigma ** 2) * T) / (sigma * sy.sqrt(T))
        d2 = (sy.ln(S / K) + (r - q - 0.5 * sigma ** 2) * T) / (sigma * sy.sqrt(T))
        
        put = K * sy.exp(-r * T) * N.cdf(-d2) - S * sy.exp(-q * T) * N.cdf(-d1)
        
        return put

    def sym_euro_vanilla_dividend(self,S, K, T, r, q, sigma, option = 'call'):
        #Sympy implementation of pricing a European put or call option depending on specification
        #S: spot price
        #K: strike price
        #T: time to maturity
        #r: interest rate
        #q: rate of continuous dividend paying asset 
        #sigma: volatility of underlying asset
        
        N = systats.Normal(0.0, 1.0)
        
        d1 = (sy.ln(S / K) + (r - q + 0.5 * sigma ** 2) * T) / (sigma * sy.sqrt(T))
        d2 = (sy.ln(S / K) + (r - q - 0.5 * sigma ** 2) * T) / (sigma * sy.sqrt(T))
        
        if option == 'call':
            result = S * sy.exp(-q * T) * N.cdf(d1) - K * sy.exp(-r * T) * N.cdf(d2)
        if option == 'put':
            result = K * sy.exp(-r * T) * N.cdf(-d2) - S * sy.exp(-q * T) * N.cdf(-d1)
            
        return result




def main():
    # Accept s, x, r, sigma, and t from the command line and write
    # the Black-Scholes value.

    s     = float(sys.argv[1])
    x     = float(sys.argv[2])
    r     = float(sys.argv[3])
    sigma = float(sys.argv[4])
    t     = float(sys.argv[5])

    model=blackscholes_model()
    print("res:",model.callPrice(s, x, r, sigma, t))
    model2=nonDividend_Paying_Black_Scholes_model()
    x=model2.sym_euro_vanilla(50, 100, 1, 0.05, 0.25, option = 'put')
    print("x:",x)

if __name__=="__main__":
    main()
