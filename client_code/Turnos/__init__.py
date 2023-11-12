from ._anvil_designer import TurnosTemplate
from anvil import *
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

class Turnos(TurnosTemplate):
  def __init__(self, licensePlate, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    self.licensePlate = licensePlate
    self.welcome_label.text = f"Dominio: {self.licensePlate}"
    self.historial.items = anvil.server.call('get_open_dates', self.licensePlate)
    # Any code you write here will run before the form opens.
  
  def logout_click(self, **event_args):
    """This method is called when the button is clicked"""
    open_form('Homepage')

  def search_click(self, **event_args):
    """This method is called when the button is clicked"""
    self.turnos.items = anvil.server.call('get_open_dates', self.date_picker_1.date)
    self.historial.items = anvil.server.call('get_open_dates', self.licensePlate)

  def save_click(self, **event_args):
    """This method is called when the button is clicked"""
    _reserve = app_tables.fechas.search(licensePlate=self.licensePlate, eval=False)
    if len(_reserve) > 0:
      alert('EXISTE EVALUACIÓN PEDIENTE')
      raise Exception('EXISTE EVALUACIÓN PENDIENTE')
    
    _id = int(self.reserve_id.text)
    row = app_tables.fechas.get(id=_id)
    
    if not row:
      alert('ID NO EXISTE')
      raise Exception('ID NO EXISTE')

    if row['reserved']:
      alert('ID RESERVADO')
      raise Exception('ID RESERVADO')

    row['reserved'] = True
    row['licensePlate'] = self.licensePlate

    app_tables.evaluaciones.add_row(id=_id)

