
# from lib.PersistentDictObj import PersistentDictObj


import os, json, pickle
from decimal import Decimal

class DictObj:
   def __init__(self, in_dict: dict):
      assert isinstance(in_dict, dict)

      for key, val in in_dict.items():
         if isinstance(val, (list, tuple)):
               setattr(
                  self,
                  key,
                  [DictObj(x) if isinstance(x, dict) else x for x in val],
               )
         else:
               setattr(
                  self,
                  key,
                  DictObj(val) if isinstance(val, dict) else val,
               )
                
   def get(self, key, default=None):
      return getattr(self, key, default)

   def has(self, key):
      return hasattr(self, key)

   def delete(self, key):
      if hasattr(self, key):
            delattr(self, key)

            save_method = getattr(self, "save", None)

            if callable(save_method):
               save_method()

            return True

      return False

   def to_dict(self):
      out_dict = {}

      for key, val in self.__dict__.items():
         if key.startswith("_"):
               continue

         if isinstance(val, DictObj):
               out_dict[key] = val.to_dict()

         elif isinstance(val, (list, tuple)):
               out_dict[key] = [
                  item.to_dict() if isinstance(item, DictObj) else item
                  for item in val
               ]

         else:
               out_dict[key] = val

      return out_dict


class GetDatafile(DictObj):
      """
      Datafile Model nach name suchen Datafile.objects.filter(name=name).first()
      """
      
      def __init__(self, name):
         from apps.shop.models import Datafile
         model_obj = Datafile.objects.filter(name=name).first()

         if model_obj is None:
            raise ValueError(f"Datafile mit name='{name}' nicht gefunden")

         field_name = "jdata"

         object.__setattr__(self, "_autosave_enabled", True)
         object.__setattr__(self, "_model_obj", model_obj)
         object.__setattr__(self, "_field_name", field_name)

         field_value = getattr(model_obj, field_name)

         if field_value is None:
            field_value = {}

         if not isinstance(field_value, dict):
            raise TypeError("jdata muss dict oder None sein")

         super().__init__(field_value)

         object.__setattr__(self, "_autosave_enabled", True)

      def __setattr__(self, key, value):
         object.__setattr__(self, key, value)

         if key.startswith("_"):
            return

         if not getattr(self, "_autosave_enabled", False):
            return

         self.save()

      def save(self):
         setattr(
            self._model_obj,
            self._field_name,
            self.to_dict(),
         )

         self._model_obj.save(update_fields=[self._field_name])


