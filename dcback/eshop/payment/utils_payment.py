from datetime import datetime, timedelta, date, timezone
from django.db.models import Q
import json

class BlList:
    
    def __init__(self, ip=None, fiprint=None, checktime=None, count=None, bltime=None, appid=None):
        from eshop.models import BlackList
        self.qs = BlackList.objects.filter(appid=appid)
        self.fiprint = fiprint
        self.ip = ip
        self.appid = appid
        self.json = {"checktime":checktime, "count":count, "bltime":bltime, "appid":appid}
        if fiprint or ip:
            obj, create = self.qs.filter(Q(fprint=self.fiprint) | Q(ip=self.ip)).get_or_create(
                defaults={
                    'appid':self.appid,
                    'ip':self.ip,
                    'fprint':self.fiprint,
                    'description':json.dumps(self.json)
                }
            )
        
            self.db = obj
        self.bltime = bltime
        self.count = count
        self.checktime = checktime

    def bl_create(self):
        print(datetime.now(timezone.utc)-self.db.created_at)
        if datetime.now(timezone.utc) - self.db.created_at < timedelta(minutes=self.checktime):
            if self.db.count < self.count:
                self.db.count = self.db.count + 1
                self.db.save()
                return {'count':self.db.count}
            else:
                return {'blocked':self.db.created_at + timedelta(minutes=self.bltime)}
        else:
            d = self.qs.filter(id=self.db.id, count__lt=self.count)
            r = d.delete()
            if r[0] > 0:
                return {'delete':r}
            else:
                return {'blocked':self.db.created_at + timedelta(minutes=self.bltime)}
        
            

    def bl_clear(self):
        d = self.qs.filter(Q(created_at__lt=datetime.now(timezone.utc)-timedelta(minutes=self.bltime)) | 
                       Q(created_at__lt=datetime.now(timezone.utc)-timedelta(minutes=self.checktime), count__lt=self.count))
        r = d.delete()
        return r[0]