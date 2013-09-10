'''
Created on Sep 9, 2013

@author: pierreadrienguez
'''
from abc import abstractmethod

class Trade:
    @staticmethod
    @abstractmethod
    def get_variables_names():
        """ define the variables"""
        raise TypeError("Cannot instantiate Trade abstract class")
    
    def __setattr__(self, *ignored):
        """ trade are immutable objects
        in order to keep the integrity of the database"""
        return NotImplemented

    def __delattr__(self, *ignored):
        """ trade are immutable objects
        in order to keep the integrity of the database"""
        return NotImplemented
    
    def __str__(self):
        __dict = self.get_variables_dict()
        return ", ".join(param + ": " + str(getattr(self, param)) 
                         for param in __dict)
        
    def get_variables_dict(self):
        params = self.get_variables_names()
        return {param: getattr(self, param) for param in params}
    
    def get_variables_dict_no_id(self):
        variables_dict = self.get_variables_dict()
        return {var: variables_dict[var] for var in variables_dict
                                    if var != "id"}