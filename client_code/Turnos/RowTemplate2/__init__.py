from ._anvil_designer import RowTemplate2Template
from anvil import *
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import datetime as dt

class RowTemplate2(RowTemplate2Template):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    _fecha = app_tables.fechas.get(id=self.item['id'])
    self.fecha.text = _fecha['date'].strftime('%Y/%m/%d %H:%M')
    
    if self.item['Score'] == 0 and _fecha['date'].date() < dt.date.today():
      self.status.text = 'Incompleta'
    elif self.item['Score'] == 0:
      self.status.text = 'Pendiente'
    elif self.item['Score'] < 40:
      self.status.text = 'Desaprobado'
    else:
      if (
        self.item['S1'] < 5 or
        self.item['S2'] < 5 or
        self.item['S3'] < 5 or
        self.item['S4'] < 5 or
        self.item['S5'] < 5 or
        self.item['S6'] < 5 or
        self.item['S7'] < 5 or
        self.item['S8'] < 5
      ):
        self.status.text = 'Sección Desaprobada'
      else:
        self.status.text = 'Aprobado'
        

    # Any code you write here will run before the form opens.

  def status_click(self, **event_args):
    """This method is called when the link is clicked"""
    alert(self.item['Comments'])
