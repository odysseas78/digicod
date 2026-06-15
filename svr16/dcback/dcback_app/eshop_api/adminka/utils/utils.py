from django.db.models import Q
from loguru import logger
import decimal
from datetime import datetime, timedelta, date
import json
import django_filters
from django_filters.rest_framework import DjangoFilterBackend
import jsons


def construct(filter):
    logger.add("logs/constructLog.log", backtrace=True, diagnose=True, filter=lambda record: record["extra"].get("name") == "constructLog")
    constructLog = logger.bind(name="constructLog")
    # constructLog.info(f"construct(filter) - {filter}")
    q_object = Q()
    q_exlude = Q()
    # constructLog.info(f"q_object: - {q_exlude}")
    # constructLog.info(f"q_exlude: - {q_exlude}")
    def check(item, value):
        if item == '>':
            return '__gt'
        elif item == '>=':
            return '__gte'
        elif item == 'contains':
            return '__contains'
        elif item == '<':
            return '__lt'
        elif item == '<=':
            return '__lte'
        elif item == '=':
            # constructLog.info(f"value: - {value}")
            if type(value) == str and value[:2] == '20' and len(value) == 10 and value[4] == '-' and value[7] == '-':
                return '__startswith'
            else:
                return ''
        elif item == 'startswith':
            return '__startswith'
        elif item == 'endswith':
            return '__endswith'
        else:
            return None
    def checkexcl(item, value):
        if item == '<>':
            if type(value) == str and value[:2] == '20' and len(value) == 10 and value[4] == '-' and value[7] == '-':
                return '__startswith'
            else:
                return ''
        elif item == 'notcontains':
            return '__contains'
        else:
            return None

    def filterbuild(filtr):
        def getq(a=Q(),b=Q(), con_type="and"):
            if con_type == "and":
                return a & b
            elif con_type == "or":
                return a | b
            else: 
                return None
            
        fin = list()
        finex = list()
        d = ['and', 'or']
        itlist = list()
        def funct(data):
            for item in data:
                if type(item) == list or item in d:
                    # print(item)
                    itlist.append(item)
                    funct(item)
                    
        if type(filtr[0]) == str and type(filtr) == list and filtr[1] not in d:
            if check(filtr[1], filtr[2]) != None:
                fin.append(Q([filtr[0].replace('.','__').replace('[0]','')+check(filtr[1], filtr[2]), filtr[2]]))
            if checkexcl(filtr[1], filtr[2]) != None:
                fin.append(~Q([filtr[0].replace('.','__').replace('[0]','')+checkexcl(filtr[1]), filtr[2]]))
            ergb = list()
            if len(fin) > 0:
                ergb.append(fin[0])
            else:
                ergb.append(fin)
            # if len(finex) > 0:
            #     ergb.append(finex[0])
            # else:
            #     ergb.append(finex)
            
            return ergb   
        else:
            funct(filtr)

        h = list()
        open = 0
        closed = 0
        for s in itlist:
            # print(s)
            if type(s[0]) == list and s not in d:
                if closed == 0:
                    open += 1
                elif open > 0 and closed > 0:
                    closed += 1
                    
            elif s not in d:
                if closed == 0 and open > 0:
                    closed = 1
                if check(s[1], s[2]) != None:
                    fin.append(Q([s[0].replace('.','__').replace('[0]','')+check(s[1], s[2]), s[2]]))
                if checkexcl(s[1], s[2]) != None:
                    fin.append(~Q([s[0].replace('.','__').replace('[0]','')+checkexcl(s[1]), s[2]]))
            else:
                if len(fin) == 1:
                    fin.append(s)
                # if len(finex) == 1:
                #     finex.append(s)
                # if len(fin) == 1:
                #     fin.append(s)
                
            if len(fin) == 3:
                l = fin.copy()
                fin=list()
                fin.append(getq(l[0], l[2], l[1]))
            # if len(finex) == 3:
            #     l = finex.copy()
            #     finex=list()
            #     finex.append(getq(l[0], l[2], l[1]))
                # fin.append(getq(h[0],h[2], h[1]))
                # h = list()
            # if len(fin) == 3:
            #     w = fin.copy()
            #     fin = list()
            #     fin.append(getq(w[0],w[2], w[1]))
        ergb = list()
        if len(fin) > 0:
            ergb.append(fin[0])
        else:
            ergb.append(fin)
        # if len(finex) > 0:
        #     ergb.append(finex[0])
        # else:
        #     ergb.append(finex)
        
        return ergb   

    result = filterbuild(filter)
    constructLog.info(f"result: - {result}")
    return {'q_object':result[0]}



def construct_selectors(group, queryset):
    logger.add("logs/Orders2ViewSet.log", backtrace=True, diagnose=True, filter=lambda record: record["extra"].get("name") == "Orders2ViewSet")
    Orders2ViewSet = logger.bind(name="Orders2ViewSet")
    selectors = list()
    
    for item in group:
        selectors.append({'isExpanded':item.get('isExpanded'),'selector':item.get('selector').replace('.', '__').replace('[0]', '')})
   
    # selectors.reverse()
    q_set = {}
    q_set2 = []
    for sel in selectors:
        valset = set()
        valueslist = queryset.values_list(sel.get('selector'))
        dt = False
        # Orders2ViewSet.info(f"sel.get('selector'): {sel.get('selector')}")
        # Orders2ViewSet.info(f"valueslist: {valueslist}")
        for value in set(valueslist):
            # Orders2ViewSet.info(f"value[0]: {value[0]}")
            if type(value[0]) == datetime:
                value1 = value[0].date()
                dt = True
            else:
                dt = False
                value1 = value[0]
            if value1:
                valset.add(value1)
            # Orders2ViewSet.info(f"valset - {valset}")
        for val in sorted(valset):
            # Orders2ViewSet.info(f"val: {val}")
            if dt == True:
                selectr = sel.get('selector')+'__startswith'
            else:
                selectr = sel.get('selector')
            if not q_set.get(selectr):
                q_set.update({selectr:[]})
            q_set.get(selectr).append(Q([selectr, val]))
    # Orders2ViewSet.info(f"q_set: {q_set}")
    return [q_set, selectors]