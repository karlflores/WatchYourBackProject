from random import randint
'''
PICKS RANDOM MOVES BASED ON THE LENGTH OF CURRENTLY AVAILABLE MOVES TO MAKE 

THIS WAS THE STARTING POINT OF OUR ALGORITHMIC DESIGN AND BOARD MECHANISM VALIDATION/TESTING 
'''

class Random(object):
    
    @staticmethod
    def choose_move(actions):
        return randint(0,len(actions)-1)
