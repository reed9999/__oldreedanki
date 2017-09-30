# from aqt import mw

# action = QAction("Philip 2", mw)
# action.triggered.connect(main)
# mw.form.menuTools.addAction(action)

def assert_intended_model(model_id=SOURCE_DECLENSION_MODEL):
  assert mw.col.models.current()['id'] == model_id

def create_note(model_id, dict):
  assert_intended_model(model_id)
  new_note = mw.col.newNote()
  for k, v in dict.iteritems():
    new_note[k] = v
  new_count = mw.col.addNote(new_note)
  return new_count
  
def create_hardcoded_note():
  global assert_intended_model
  global create_note
  dict = {
    'Front': 'This is the front ' +  datetime.datetime.now().strftime("%I:%M%p on %B %d, %Y"),
    'Back': 'This is the back ' +  datetime.datetime.now().strftime("%I:%M%p on %B %d, %Y"),
    'declension_context': 'some context',
    'gender': 'm f n',
    'number': 'singular',
    'case': 'nominagenitavocative',
  }
  return create_note(SOURCE_DECLENSION_MODEL, dict)
  
def create_hardcoded_note_old():
  assert_intended_model()
  new_note = mw.col.newNote()
  new_note['Front'] = 'This is the front ' +  datetime.datetime.now().strftime("%I:%M%p on %B %d, %Y")
  new_note['Back'] = 'This is the back ' +  datetime.datetime.now().strftime("%I:%M%p on %B %d, %Y")
  new_note['declension_context'] = 'some context'
  new_note['gender'] = 'm f n'
  new_note['number'] = '1294'
  new_note['case'] = 'suitcase'
  new_count = mw.col.addNote(new_note)
  return new_count

  


try: 
  assert_intended_model(SOURCE_DECLENSION_MODEL)
#  showInfo("try Worked")
except:
  showInfo("Bad model %s" % mw.col.models.current()['id'])


rv = create_hardcoded_note()
assert rv > 0

showInfo("Worked even better!")
