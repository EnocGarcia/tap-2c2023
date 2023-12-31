from ._anvil_designer import HomepageTemplate
from anvil import *
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from ..Login import Login

class Homepage(HomepageTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    # Any code you write here will run before the form opens.

  def login_button_click(self, **event_args):
    """This method is called when the button is clicked"""
    user = {}
    login_clicked = alert(
      content=Login(item=user),
      title="Iniciar Sesión",
      large=True,
      buttons=[("Iniciar Sesión", True), ("Cancelar", False)]
    )

    if login_clicked:
      try:
        anvil.server.call('login_user', user)
        open_form('Eval', **user)
      except Exception as e:
        alert(str(e))

  def go_button_click(self, **event_args):
    """This method is called when the button is clicked"""
    _licensePlate = self.licensePlate_textbox.text.upper()
    try:
      anvil.server.call('login_licensePlate', _licensePlate)
      open_form('Turnos',licensePlate=_licensePlate)
    except Exception as e:
      alert(str(e))
