import itertools
import pickle
import base64,sys,os
sys.path.insert(0, '/home/dcback')
import django
os.environ['DJANGO_SETTINGS_MODULE'] = 'config.settings'
django.setup()
from basket import BasketCls 
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
import requests




class DictObj:
    def __init__(self, in_dict: dict):
        assert isinstance(in_dict, dict)
        for key, val in in_dict.items():
            if isinstance(val, (list, tuple)):
                setattr(self, key, [DictObj(x) if isinstance(x, dict) else x for x in val])
            else:
                setattr(self, key, DictObj(val) if isinstance(val, dict) else val)

    def to_dict(self):
        out_dict = {}
        for key, val in self.__dict__.items():
            if isinstance(val, DictObj):
                out_dict[key] = val.to_dict()
            elif isinstance(val, (list, tuple)):
                out_dict[key] = [item.to_dict() if isinstance(item, DictObj) else item for item in val]
            else:
                out_dict[key] = val
        return out_dict




ob = DictObj({
    'Dobj': DictObj,
    'BasketCls': BasketCls
})



            

