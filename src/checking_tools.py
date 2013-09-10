'''
Created on Sep 9, 2013

@author: pierreadrienguez
'''
import functools

TRADERS_LIST = ["damien", "pierre"]

def typecheck(f):
    """ useful type checking decorator from annotations when types are used
        potentially check parameters and return type
    """
    @functools.wraps(f)
    def decorated(*args, **kws):
        for i, arg in enumerate(f.__code__.co_varnames):
            argtype = f.__annotations__.get(arg)
            # Only check if annotation exists and it is as a type
            if isinstance(argtype, type):
                # First len(args) are positional, after that keywords
                value_to_test = args[i] if i < len(args) else kws[arg]
                if not isinstance(value_to_test, argtype):
                    raise ValueError("Wrong parameter: %s is not of type " +
                                     "%s when calling %s with %s" %
                                      (value_to_test, argtype, 
                                       f.__qualname__, arg))
        # check the return type
        result = f(*args, **kws)
        returntype = f.__annotations__.get('return')
        if returntype is not None and not isinstance(returntype, type):
            print(result, returntype, type)
            raise ValueError("Wrong return type: " +
                             "%s is not of type %s when calling %s" %
                             (result, returntype, f.__qualname__))
        return result
    return decorated
    
def check_trade(trade, trade_class) -> bool:
    if not isinstance(trade, trade_class):
        message = trade.to_string() if hasattr(trade, "to_string") else "Unknown"
        raise TypeError("The following is not a %s trade \n %s" % 
                        (trade_class.__name__, message))
    return True    
    

def datetime_check(datetime):
    pass #TODO
    
def trader_check(trader: str) -> None:
    if trader not in TRADERS_LIST:
        raise ValueError("Trader %s traded but is not in the list of traders" % trader)
            
def symbol_check(symbol: str) -> None:
    # TODO:
    pass

def currency_pair_check(currency_pair: str) -> None:
    # TODOm
    pass

def year_check(year: int) -> None:
    if year < 2012:
        raise ValueError("How did you trade an expired product " +
                         "(expired in %d)?" % year)
    if year > 2100:
        raise ValueError("How can you trade a product with such " +
                         " a big maturity (expiration year %d)?" % year)
    
def month_check(month: int) -> None:
    if not 0 < month < 13:
        raise ValueError("Impossible month: %d" % month)