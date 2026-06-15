from django.db.models import Count, Sum, Max, Min, Avg
import json
from django.db.models import Q, F
from loguru import logger


logger.add("logs/groupconstructor.log", backtrace=True, diagnose=True, filter=lambda record: record["extra"].get("name") == "groupconstlog")
groupconstlog = logger.bind(name="groupconstlog")
#----------------------------------------------------------
def getsumtype(gselsum, selector):
    gsumtyp = {'count':Count(selector), 'sum':Sum(selector),'max':[Max(selector)], \
        'min':[Min(selector)],'avg':[Avg(selector)]}
    r = gsumtyp.get(gselsum)
    return r
#------------------------------------------------------
def getsumary(request, qs):
    totalsumsel = json.loads(request.query_params.get('totalSummary'))[0].get("selector").replace('.','__').replace('[0]','')
    sumtype = json.loads(request.query_params.get('totalSummary'))[0].get("summaryType")
    summdata = qs.values(totalsumsel).aggregate(getsumtype(sumtype, totalsumsel)).get(totalsumsel+'__'+sumtype)
    return summdata


def grup_constructor(request, sel, qs):
                    
                    res = []
                    cnt = []
                    vls = []
                    
                    for sl in sel:
                        kj = sl.get('selector').replace('.','__').replace('[0]','')
                        # print(kj)
                        cnt.append(Count(kj))
                        vls.append(kj)
                    
                    if request.query_params.get('totalSummary') and len(json.loads(request.query_params.get('totalSummary'))) > 0:
                        summary = getsumary(request, qs)
                    else:
                        summary = ''
                    annon = []
                    getsum = []
                    orderby = ''
                    if request.query_params.get('groupSummary') and len(json.loads(request.query_params.get('groupSummary'))) > 0 and \
                        json.loads(request.query_params.get('groupSummary'))[0].get("selector").replace('.','__').replace('[0]','') \
                            .replace('true','True').replace('false','False'):
                        grupsumsel = json.loads(request.query_params.get('groupSummary').replace('.','__').replace('[0]','') 
                            .replace('true','True').replace('false','False'))
                        orderby = grupsumsel[0].get('selector')+'__'+grupsumsel[0].get('summaryType')
                        if len(orderby) < 1:
                            orderby = None
                        else:
                            orderby = f'-{orderby}'
                        for gsel in grupsumsel:
                            annon.append(getsumtype(gsel.get('summaryType'), gsel.get('selector').replace('.','__').replace('[0]','')))
                            getsum.append(gsel.get('selector')+'__'+ gsel.get('summaryType'))
                    grup = qs.values(*vls).annotate(*cnt).order_by()
                    try:
                        fd = grup.values(key=F(vls[0])).annotate(count=Count(vls[0]), *annon).order_by(orderby)
                    except:
                        fd = grup.values(key=F(vls[0])).annotate(count=Count(vls[0]), *annon).order_by()
                    for i in fd:
                        # groupconstlog.info(f'i - {i}')
                        q_obj = []
                        i['items']=None
                        i["summary"] = []
                        for u in getsum:
                            i["summary"].append(i.get(u))
                        if len(vls) > 1:
                            i['items']=[]
                            i.pop('count')
                            q_obj.append(Q([vls[0], i.get('key')]))
                            try:
                                fd1 = grup.values(key=F(vls[1])).annotate(count=Count(vls[1]), *annon).filter(*q_obj).order_by(orderby)
                            except:
                                fd1 = grup.values(key=F(vls[1])).annotate(count=Count(vls[1]), *annon).filter(*q_obj).order_by()
                            for i1 in fd1:
                                i1['items']=None
                                i1["summary"] = []
                                for u in getsum:
                                    i1["summary"].append(i1.get(u))
                                i['items'].append(i1)
                                if len(vls) > 2:
                                    i1['items']=[]
                                    i1.pop('count')
                                    q_obj.append(Q([vls[1], i1.get('key')]))
                                    try:
                                        fd2 = grup.values(key=F(vls[2])).annotate(count=Count(vls[2]), *annon).filter(*q_obj).order_by(orderby)
                                    except:
                                        fd2 = grup.values(key=F(vls[2])).annotate(count=Count(vls[2]), *annon).filter(*q_obj).order_by()
                                    for i2 in fd2:
                                        i2['items']=None
                                        i2["summary"] = []
                                        for u in getsum:
                                            i2["summary"].append(i2.get(u))
                                        i1['items'].append(i2)
                                        if len(vls) > 3:
                                            i2['items']=[]
                                            i2.pop('count')
                                            q_obj.append(Q([vls[2], i2.get('key')]))
                                            try:
                                                fd3 = grup.values(key=F(vls[3])).annotate(count=Count(vls[3]), *annon).filter(*q_obj).order_by(orderby)
                                            except:
                                                fd3 = grup.values(key=F(vls[3])).annotate(count=Count(vls[3]), *annon).filter(*q_obj).order_by()
                                            for i3 in fd3:
                                                i3['items']=None
                                                i3["summary"] = []
                                                for u in getsum:
                                                    i3["summary"].append(i3.get(u))
                                                i2['items'].append(i3)
                                                if len(vls) > 4:
                                                    i3['items']=[]
                                                    i3.pop('count')
                                                    q_obj.append(Q([vls[3], i3.get('key')]))
                                                    try:
                                                        fd4 = grup.values(key=F(vls[4])).annotate(count=Count(vls[4]), *annon).filter(*q_obj).order_by(orderby)
                                                    except:
                                                        fd4 = grup.values(key=F(vls[4])).annotate(count=Count(vls[4]), *annon).filter(*q_obj).order_by()
                                                    for i4 in fd4:
                                                        i4['items']=None
                                                        i4["summary"] = []
                                                        for u in getsum:
                                                            i4["summary"].append(i4.get(u))
                                                        i3['items'].append(i4)
                                                        if len(vls) > 5:
                                                            i4['items']=[]
                                                            i4.pop('count')
                                                            q_obj.append(Q([vls[4], i4.get('key')]))
                                                            try:
                                                                fd5 = grup.values(key=F(vls[5])).annotate(count=Count(vls[5]), *annon).filter(*q_obj).order_by(orderby)
                                                            except:
                                                                fd5 = grup.values(key=F(vls[5])).annotate(count=Count(vls[5]), *annon).filter(*q_obj).order_by()
                                                            for i5 in fd5:
                                                                i5['items']=None
                                                                i5["summary"] = []
                                                                for u in getsum:
                                                                    i5["summary"].append(i5.get(u))
                                                                i4['items'].append(i5)
                        res.append(i)
                    return [res, [summary]]
            #---------------------------------------------------------------------------------------------------  