from ._anvil_designer import RowTemplate1Template
from anvil import *
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

from datetime import datetime

class RowTemplate1(RowTemplate1Template):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    self.id.text = self.item['id']
    self.fecha.text = self.item['date'].strftime('%Y/%m/%d %H:%M')
    self.reserved.checked = bool(self.item['reserved'])
    # Any code you write here will run before the form opens.
