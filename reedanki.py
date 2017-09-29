####
# Right now the goal is to go through a particular (later, aribtrary)
# note type, parse out the content according to a regex, and put the 
# content into a new note of a different, particular (later, arbitrary)
# note type


# import the main window object (mw) from aqt
from aqt import mw
# import the "show info" tool from utils.py
from aqt.utils import showInfo
# import all of the Qt GUI library
from aqt.qt import *
from pprint   import pprint as pp
import re
import datetime

#reload (philip.main)

SOURCE_DECLENSION_MODEL = 1342704714050L
WEIRD_DECLENSION_MODEL = 1450932830892L
DESTINATION_DECLENSION_MODEL = SOURCE_DECLENSION_MODEL

_counter = 0
_logstring = ""

##### NEWER CODE
# Try building from the ground up--something between a refactor and an overhaul.

def assert_intended_model():
  assert mw.col.models.current()['id'] == SOURCE_DECLENSION_MODEL
  
def create_hardcoded_note():
  assert_intended_model()
  new_note = mw.col.newNote()
  new_note['Front'] = 'This is the front ' +  datetime.datetime.now().strftime("%I:%M%p on %B %d, %Y")
  new_note['Back'] = 'This is the back ' +  datetime.datetime.now().strftime("%I:%M%p on %B %d, %Y")
  new_note['declension_context'] = 'some context'
  new_note['gender'] = 'm f n'
  new_note['number'] = '1294'
  new_note['case'] = 'suitcase'
  new_count = mw.col.addNote(new_note)



##### OLDER CODE

#This isn't needed since we hard coded...
#REFACTOR: don't hard code!
def id_for_first_model_matching(patt):
  all_models = mw.col.models.all()
  for model in all_models:
    if re.match(patt, model['name']):
      return model['id']


def get_list_from_file():
  import os
  dir = os.path.dirname(__file__)
  filename = os.path.join(dir, 'reedanki', 'config.txt')
  with open(filename) as f:
    lines = f.read().splitlines()   
  return lines

def create_a_label(text, x=25):
  label = QLabel()
  label.setText(text)
  label.setGeometry(x, 50, 500, 50,)
  layout = mw.layout()
  layout.addWidget(label)
  mw.setLayout(layout)
#mw.setCentralWidget(label) 


def make_new_declension_note():
  #This feels like it has an extra unneccessary step.
  # Could we simply mw.col.conf['curModel'] = DESTINATION_DECLENSION_MODEL???
  new_declension_id = DESTINATION_DECLENSION_MODEL
  model_we_want = mw.col.models.get(new_declension_id)
  mw.col.models.setCurrent(model_we_want)  #Does this work? Seems to require us to do it GUI anyway.
  new_note = mw.col.newNote()
  #new_note.model = model_we_want  #breaks things because Note.model apparently a different type?
  # global _counter
  # if _counter < 10:
    # showInfo("new count of notes is %d" % new_count)
  global _logstring
  _logstring += ("empty new note has been created\n")
  return new_note

  

def convert_notes_of_model(source_model_id, dest_model_id, old_patt="(.*) (.*)\. (.*)\. (.*)\.", new_fields=[]):
  all_source_note_ids = mw.col.findNotes("mid:%d" % source_model_id)
  str = ''
  rv_notes = list()
  for id in all_source_note_ids:
    new_note, s = convert_note(id, old_patt, new_fields)
    str += s
    rv_notes.append(new_note)
  return rv_notes, str

  
def convert_note(note_id, patt, new_fields):
  note = mw.col.getNote(note_id)
  the_match = re.match(patt, note['Front'])
  if (not the_match):
    #showInfo("Could not match %s with %s" % (patt, note['Front'] ))
    return (None, 'No equivalent')


  the_dict = {}
  str = ''
  new_note=make_new_declension_note()
  for i in range(1,5):
    str += "New field %s will be %s.   " % (new_fields[i-1], the_match.group(i))
    #the_dict[new_fields[i-1]] = m.group(i)
    try:
      new_note[new_fields[i-1]] = the_match.group(i)
    except KeyError:
      print( "You probably used a note type without a field for " + new_fields[i-1])
      silly_keys(new_note.keys()) 

      raise
  # global _counter
  # if _counter < 10:
    # showInfo("str is %s" % str)
    # showInfo("new_note is %s" % new_note)
  global _logstring
  _logstring += "\nstr is %s\n" % str
  mw.col.log("str is %s" % str)
  new_count = mw.col.addNote(new_note)

  _logstring += ("new count of notes is %d\n" % new_count)
  return (new_note, str)

def silly_keys(the_keys):
  n = 100
  for a_key in the_keys:
    create_a_label(str(a_key), n)
    n += 33
  
def main():
  rv = create_hardcoded_note()
  assert rv > 0
  rv = create_hardcoded_note()
  assert rv > 0
  create_a_label("I CREATED 2 NOTES", 50)
    
def old_main():
  #import philip.main

  patt = "(.*) (.*)\. (.*)\. (.*)\."
  fields=get_list_from_file()
  global _logstring
  try:
    new_notes, rv = convert_notes_of_model(SOURCE_DECLENSION_MODEL, DESTINATION_DECLENSION_MODEL, patt, fields)
  except:
    showInfo(_logstring)
    raise
  showInfo(_logstring)
  create_a_label("RV is %s" % rv, 25)

action = QAction("Philip declension", mw)
action.triggered.connect(main)
mw.form.menuTools.addAction(action)



# rv=declension_stuff(".*de-dec")
# make_new_declension_note("[Dd]eclens")

#### MORE FUN STUFF

#This worked 
# import datetime
# MOD = 1506565101476
# new_note = mw.col.newNote()
# new_note['Front'] = 'This is the front ' +  datetime.datetime.now().strftime("%I:%M%p on %B %d, %Y")
# new_note['Back'] = 'This is the back ' +  datetime.datetime.now().strftime("%I:%M%p on %B %d, %Y")
# new_count = mw.col.addNote(new_note)
# print(new_count)