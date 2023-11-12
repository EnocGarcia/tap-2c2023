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
    _initdate = dt.date.today()
    _id = 0
  else :
    _initdate = dates[0]['date'] + dt.timedelta(days=1)
    _id = dates[0]['id']

  for i in range(50):
    _date = _initdate + dt.timedelta(days=i)
    for j in range(12):
      _id += 1
      _datetime = dt.datetime.combine(_date, dt.time(hour=10))
      _datetime = _datetime + dt.timedelta(minutes=30*j)
      app_tables.fechas.add_row(date=_datetime,reserved=False,id=_id, eval=False)
      
  return True
      
@anvil.server.callable
def launch_generate_dates():
  task = anvil.server.launch_background_task('generate_dates')
  return task

@anvil.server.callable
def login_user(user_dict):
  if app_tables.usuarios.get(**user_dict):
    return True
  raise Exception("USUARIO NO ENCONTRADO")

@anvil.server.callable
def login_licensePlate(licensePlate):
  if not licensePlate:
    raise Exception("INGRESAR MATRICULA")
    
  if not app_tables.matriculas.get(licensePlate=licensePlate):
    app_tables.matriculas.add_row(licensePlate=licensePlate)
    
  return True

@anvil.server.callable
def get_open_dates(date):
  return app_tables.fechas.search(
    date=q.between(date, date+dt.timedelta(days=1))
  )

@anvil.server.callable
def get_history(licensePlate):
  _rows = app_tables.fechas.search(
    licensePlate=licensePlate
  )

  _ids = [row['id'] for row in _rows]
  
  return app_tables.evaluaciones.search(
    id=q.any_of(*_ids)
  )