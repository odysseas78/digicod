import re

from django.db.models import Q


def substr(string, char, endleft, endright, rpls):
    global subs3
    def f1(string, char, richtung, endchar):
        gh = string.find(char)
        global pos
        while True:
            if string[gh] != endchar:
                if richtung == 'left':
                    gh -= 1
                elif richtung == 'right':
                    gh +=1
            elif string[gh] == endchar:
                pos = gh
                break
        return pos
    while string.count(char) > 0:   
        start = f1(string, char, 'left', endleft)
        end = f1(string, char, 'right', endright)+1
        subs = string[start: end]
        subs3 = subs
        for ij in rpls:
            subs3 = subs3.replace(*ij)
        string = string.replace(subs, subs3)
    string = string.replace(';',',')
    return string

def replace_symbol_between_brackets(string, symbol, replacement):
    pattern = rf'\[.*?{symbol}.*?,\s*'
    return re.sub(pattern, lambda match: match.group().replace(symbol, replacement), string)

def q_objconstr(filter):
    
    # ['("', '('], [',["!" ,', '~Q(['], ['["!"', '~Q(['], ['(,[', '(['], ['", "notcontains"', '__contains"']
    filter = replace_symbol_between_brackets(filter, '.', '__')
    dd = [
            ['[0]',''],
            ['", "<"', '__lt"'], ['", "<="', '__lte"'], ['", ">"', '__gt"'], ['", ">="', '__gte"'], [', "="', ''], 
            [', "or",', ' | '], [', "and",', ' & '], [',"or",', ' |'],
            ['","contains"', '__contains"'], ['","startswith"', '__startswith"'], ['","endswith"', '__endswith"'], 
            
            ['["!", ', '~['],['[', 'Q('], [']', ')'],
            
            
            ['","<"', '__lt"'], ['","<="', '__lte"'], ['",">"', '__gt"'], ['",">="', '__gte"'], [',"="', ''],
            ['", "contains"', '__contains"'], ['", "startswith"', '__startswith"'], ['", "endswith"', '__endswith"'], 
            [',"and",', ' & '], ['"or"', ' | '], ['"and"', ' & '], ['null', 'None'], ['  ', ' '], ['true', 'True'], ['false', 'False']
            
             
        ]

    rpls = [['[','~['],['", "notcontains"', '__contains"']]
    filter = substr(filter, 'notcontains', '[', ']', rpls)
    
    rpls = [[', "<>"',''],['[', '~[']]
    filter = substr(filter, '"<>"', '[', ']', rpls)
    
    for i in dd:
        filter = filter.replace(*i)
    
    # while True:
    #     g = filter.find('.')
    #     if g >= 0:
    #         if filter[g-1].isnumeric() or filter[g+1].isnumeric():
    #             filter = filter.replace('.','!!!!!', 1)
    #         else:
    #             filter = filter.replace('.','__')
    #     else:
    #         filter = filter.replace('!!!!!','.')
    #         break
    
    rpls = [['(','(['],[')','])'],[',',';']]
    filter = substr(filter, ',', '(', ')', rpls)
    
    return eval(filter)