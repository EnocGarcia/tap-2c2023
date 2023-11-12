from ._anvil_designer import EvalTemplate
from anvil import *
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

class Eval(EvalTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    self.evaluation.items = anvil.server.call('get_open_eval')

    # Any code you write here will run before the form opens.

  def logout_click(self, **event_args):
    """This method is called when the button is clicked"""
    open_form('Homepage')

  def generate_dates_click(self, **event_args):
    """This method is called when the button is clicked"""
    anvil.server.call('launch_generate_dates')
    alert('Se generaron nuevos turnos!')
    return True

  def refresh_click(self, **event_args):
    """This method is called when the button is clicked"""
    self.evaluation.items = anvil.server.call('get_open_eval')


