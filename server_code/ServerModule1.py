import datetime as dt
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server

# This is a server module. It runs on the Anvil server,
# rather than in the user's browser.
#
# To allow anvil.server.call() to call functions here, we mark
# them with @anvil.server.callable.
# Here is an example - you can replace it with your own:
#
# @anvil.server.callable
# def say_hello(name):
#   print("Hello, " + name + "!")
#   return 42
#


@anvil.server.background_task
def generate_dates():
  dates = app_tables.fechas.search(
    tables.order_by("date", ascending=False)
  )
  if not len(dates):
    _date = dt.date.today()
  else :
    _date = dates[0]['date'] + dt.timedelta(days=1)

  for i in range(50):
    _date = _date + dt.timedelta(days=i)
    for j in range(12):
      _datetime = dt.datetime.combine(_date, dt.time(hour=10))
      _datetime = _datetime + dt.timedelta(minutes=30*j)
      app_tables.fechas.add_row(date=_datetime,reserved=False)
      
  return True
      
    

@anvil.server.callable
def login_user(user_dict):
  if app_tables.usuarios.get(**user_dict):
    return True
  raise Exception("USUARIO NO ENCONTRADO")

@anvil.server.callable
def login_licensePlate(licensePlate):
  if not licensePlate:
    raise Exception("MATRICULA INVALIDA")
    
  if not app_tables.matriculas.get(licensePlate=licensePlate):
    app_tables.matriculas.add_row(licensePlate=licensePlate)
    
  return True
