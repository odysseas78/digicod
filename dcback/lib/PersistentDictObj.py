import os, json, pickle
from decimal import Decimal

class PersistentDictObj(object):
    ''''modifiziert jsononly or pickleonly'''
    def __init__(self, **kwargs):
        self._jsononly = kwargs.get('jsononly', False)
        self._pickleonly = kwargs.get('pickleonly', False)
        self._dbjsonfileonly = kwargs.get('_dbjsonfileonly', False)
        self._file_path = kwargs.get('file_path', None)
        self._dbjsonfile = kwargs.get('dbjsonfile', None)
        
        if (not self._jsononly or not self._dbjsonfileonly) and self._file_path:
            if os.path.exists(self._file_path):
                with open(self._file_path, "rb") as f:
                    data = pickle.load(f)
                self._data = DictObj(data)
            else:
                self._data = DictObj({})
                
        if (not self._pickleonly or not self._dbjsonfileonly) and self._file_path:
            if os.path.exists(self._file_path+'.json'):
                with open(self._file_path+'.json', "r") as f:
                    data = json.load(f)
                self._data = DictObj(data)
            else:
                self._data = DictObj({})

        if (not self._pickleonly or not self._jsononly) and self._dbjsonfile:
                data = self._dbjsonfile.json
                self._data = DictObj(data)
    
    def __getattr__(self, name):
        # Zugriff auf Attribute des inneren Objekts weiterleiten
        return getattr(self._data, name)
    
    def __setattr__(self, name, value):
        # Für interne Attribute (_file_path und _data) Standardverhalten
        if name.startswith("_"):
            super().__setattr__(name, value)
        else:
            # Für alle anderen Attribute das Objekt ändern und speichern
            setattr(self._data, name, value)
            self._save()

    def __delattr__(self, name):
        # Attribut löschen und speichern
        if hasattr(self._data, name):
            delattr(self._data, name)
            self._save()
        else:
            raise AttributeError(f"'{type(self).__name__}' object has no attribute '{name}'")
    
    def _save(self):
        # Daten in die Datei speichern
        if (not self._jsononly or not self._dbjsonfileonly) and self._file_path:
            with open(self._file_path, "wb") as f:
                pickle.dump(self._data.to_dict(), f)

        if (not self._pickleonly or not self._dbjsonfileonly) and self._file_path:   
            with open(self._file_path+'.json', "w") as f:
                json.dump(self._data.to_dict(), f,indent=4)

        if (not self._pickleonly or not self._jsononly) and self._dbjsonfile:
                self._dbjsonfile.jdata = self._data.to_dict()
                self._dbjsonfile.save()

    def hasattr(self, name):
        return hasattr(self._data, name)
    
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

# Beispielklasse DictObj bleibt gleich
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
