from ._anvil_designer import HomepageTemplate
from anvil import *
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from ..SignUp import SignUp

class Homepage(HomepageTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    # Any code you write here will run before the form opens.

  def signup_button_click(self, **event_args):
    """This method is called when the button is clicked"""
    new_user = {}
    save_clicked = alert(
      content=SignUp(item=new_user),
      title="Registrar Usuario",
      large=True,
      buttons=[("Crear", True), ("Cancelar", False)]
    )

    if save_clicked:
      anvil.server.call('add_user', new_user)
      alert("Usuario creado!")


