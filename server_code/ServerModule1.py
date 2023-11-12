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

@anvil.server.callable
def get_open_eval():
  _open_dates = app_tables.fechas.search(eval=False,reserved=True)
  _ids = [row['id'] for row in _open_dates]
  return app_tables.evaluaciones.search(id=q.any_of(*_ids))

@anvil.server.callable
def set_eval(eval):
  _eval = app_tables.evaluaciones.get(id=eval['id'])
  _fecha = app_tables.fechas.get(id=eval['id'])
  
  _eval['S1'] = eval['S1'] 
  _eval['S2'] = eval['S2'] 
  _eval['S3'] = eval['S3'] 
  _eval['S4'] = eval['S4'] 
  _eval['S5'] = eval['S5'] 
  _eval['S6'] = eval['S6'] 
  _eval['S7'] = eval['S7'] 
  _eval['S8'] = eval['S8'] 
  _eval['Score'] = eval['Score'] 
  _eval['Comments'] = eval['Comments'] 

  _fecha['eval'] = eval['eval']

  return True

@anvil.server.callable
def reserve_date(id, licensePlate):
  _reserve = app_tables.fechas.search(licensePlate=licensePlate, eval=False)
  _reserve = [row for row in _reserve if row['date'].date() >= dt.date.today()]
  row = app_tables.fechas.get(id=id)
  if len(_reserve) > 0:
    raise Exception('EXISTE EVALUACIÓN PENDIENTE')
  
  if not row:
    raise Exception('ID NO EXISTE')

  if row['reserved']:
    raise Exception('ID RESERVADO')
  
  row['reserved'] = True
  row['licensePlate'] = licensePlate
  app_tables.evaluaciones.add_row(id=id, S1=0, S2=0, S3=0, S4=0, S5=0, S6=0, S7=0, S8=0, Score=0)
