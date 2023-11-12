from ._anvil_designer import RowTemplate3Template
from anvil import *
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

class RowTemplate3(RowTemplate3Template):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    self._fecha = app_tables.fechas.get(id=self.item['id'])
    
    self.S1.text = self.item['S1']
    self.S2.text = self.item['S2']
    self.S3.text = self.item['S3']
    self.S4.text = self.item['S4']
    self.S5.text = self.item['S5']
    self.S6.text = self.item['S6']
    self.S7.text = self.item['S7']
    self.S8.text = self.item['S8']
    self.Score.text = self.item['Score']
    self.Comments.text = self.item['Comments']
    
    self.eval.checked = bool(self._fecha['eval'])

    # Any code you write here will run before the form opens.

  # def S1_change(self, **event_args):
  #   """This method is called when the text in this text box is edited"""
  #   self.item['S1'] = int(self.S1.text)

  # def S2_change(self, **event_args):
  #   """This method is called when the text in this text box is edited"""
  #   self.item['S2'] = int(self.S2.text)

  # def S3_change(self, **event_args):
  #   """This method is called when the text in this text box is edited"""
  #   self.item['S3'] = int(self.S3.text)

  # def S4_change(self, **event_args):
  #   """This method is called when the text in this text box is edited"""
  #   self.item['S4'] = int(self.S4.text)

  # def S5_change(self, **event_args):
  #   """This method is called when the text in this text box is edited"""
  #   self.item['S5'] = int(self.S5.text)

  # def S6_change(self, **event_args):
  #   """This method is called when the text in this text box is edited"""
  #   self.item['S6'] = int(self.S6.text)

  # def S7_change(self, **event_args):
  #   """This method is called when the text in this text box is edited"""
  #   self.item['S7'] = int(self.S7.text)

  # def S8_change(self, **event_args):
  #   """This method is called when the text in this text box is edited"""
  #   self.item['S8'] = int(self.S8.text)

  def Score_change(self, **event_args):
    """This method is called when the text in this text box is edited"""
    _s1 = self.item['S1']
    _s2 = self.item['S2']
    _s3 = self.item['S3']
    _s4 = self.item['S4']
    _s5 = self.item['S5']
    _s6 = self.item['S6']
    _s7 = self.item['S7']
    _s8 = self.item['S8']

    _score = _s1+_s2+_s3+_s4+_s5+_s5+_s6+_s7+_s8

    if _score != int(self.Score.text):
      alert('NO COINCIDE EL PUNTAJE FINAL CON LOS PARCIALES')
      self.Score.text = 0

  def eval_change(self, **event_args):
    """This method is called when this checkbox is checked or unchecked"""
    eval = {
      "id": int(self.item['id']),
      "S1": int(self.S1.text),
      "S2": int(self.S2.text),
      "S3": int(self.S3.text),
      "S4": int(self.S4.text),
      "S5": int(self.S5.text),
      "S6": int(self.S6.text),
      "S7": int(self.S7.text),
      "S8": int(self.S8.text),
      "Score": int(self.Score.text),
      "Comments": int(self.Comments.text),
      "eval": self.eval.checked
    }
    
    try:
      anvil.server.call('set_eval', eval)
    except Exception as e:
      alert(str(e))
