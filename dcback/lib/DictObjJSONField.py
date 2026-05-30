class DictObj:
   def __init__(self, in_dict: dict):
      assert isinstance(in_dict, dict)

      for key, val in in_dict.items():
         if isinstance(val, (list, tuple)):
               setattr(
                  self,
                  key,
                  [
                     DictObj(x) if isinstance(x, dict) else x
                     for x in val
                  ],
               )
         elif isinstance(val, dict):
               setattr(self, key, DictObj(val))
         else:
               setattr(self, key, val)
                
   def get(self, key, default=None):
      """
      Wert lesen wie bei dict.get().
      Wenn key nicht existiert, wird default zurückgegeben.
      """
      return getattr(self, key, default)

   def has(self, key):
      """
      Prüfen, ob key existiert.
      """
      return hasattr(self, key)

   def delete(self, key):
      """
      Key löschen.
      Gibt True zurück, wenn gelöscht wurde.
      Gibt False zurück, wenn key nicht existiert.
      """
      if hasattr(self, key):
            delattr(self, key)
            return True

      return False

   def to_dict(self):
      out_dict = {}

      for key, val in self.__dict__.items():
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
     
     
from django.db import models


class DictObjJSONField(models.JSONField):
    """
    JSONField, das beim Lesen automatisch DictObj zurückgibt
    und beim Speichern DictObj wieder in normales dict umwandelt.
    """

    def from_db_value(self, value, expression, connection):
        """
        Wird aufgerufen, wenn der Wert aus der DB gelesen wird.
        """
        value = super().from_db_value(value, expression, connection)

        if isinstance(value, dict):
            return DictObj(value)

        return value

    def to_python(self, value):
        """
        Wird aufgerufen, wenn Django den Wert in Python-Objekt umwandelt.
        """
        value = super().to_python(value)

        if isinstance(value, dict):
            return DictObj(value)

        return value

    def get_prep_value(self, value):
        """
        Wird vor dem Speichern aufgerufen.
        Hier muss DictObj wieder zu dict werden,
        damit JSONField es als JSON speichern kann.
        """
        if isinstance(value, DictObj):
            value = value.to_dict()
  
        return super().get_prep_value(value)