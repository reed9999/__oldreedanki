################################################################################
# Backup code -- stuff I tried maybe worth keeping, maybe not.


################################################################################
# From my old main file.



####
# Right now the goal is to go through a particular (later, aribtrary)
# note type, parse out the content according to a regex, and put the 
# content into a new note of a different, particular (later, arbitrary)
# note type




# See https://apps.ankiweb.net/docs/addons21.html

# import the main window object (mw) from aqt
from aqt import mw
# import the "show info" tool from utils.py
from aqt.utils import showInfo
# import all of the Qt GUI library
from aqt.qt import *

# We're going to add a menu item below. First we want to create a function to
# be called when the menu item is activated.

def testFunction():
    # get the number of cards in the current collection, which is stored in
    # the main window
    cardCount = mw.col.cardCount()
    # show a message box
    showInfo("Card count: %d" % cardCount)

# create a new menu item, "test"
action = QAction("test", mw)
# set it to call testFunction when it's clicked
action.triggered.connect(testFunction)
# and add it to the tools menu
mw.form.menuTools.addAction(action)




from pprint   import pprint as pp
import re
import datetime

#reload (philip.main)

SOURCE_DECLENSION = 'de-declin'
SOURCE_DECLENSION_MODEL = 1342704714050L
WEIRD_DECLENSION_MODEL = 1450932830892L
# # DESTINATION_DECLENSION_MODEL = SOURCE_DECLENSION_MODEL

_counter = 0
_logstring = ""

##### NEWER CODE
# Try building from the ground up--something between a refactor and an overhaul.

def dangerous_exec():
  import os
  dir = os.path.dirname(__file__)

  #https://stackoverflow.com/a/1463370/742573
  ldict = locals()
  
  filename = os.path.join(dir, 'reedanki', 'arbitrary.py')
  with open(filename, 'r') as the_file:
    exec (the_file.read(), globals(), ldict) 
  return ldict

###GUI
def create_a_label(text, x=25):
  label = QLabel()
  label.setText(text)
  label.setGeometry(x, x/2 , 300 , 300,)
  layout = mw.layout()
  layout.addWidget(label)
  mw.setLayout(layout)

  
def main():


#Hang onto this code somewhere because it's how I want to run dynamically in the future.
  ldict = dangerous_exec()
#  convert_notes_hardcoded_model = ldict['convert_notes_hardcoded_model']
#  rv = convert_notes_hardcoded_model()
#  assert rv > 0

  create_a_label("I CREATED SOME NOTES (maybe)", 50)

  

##### OLDER CODE

#This is redundant. See anki code,  m = self.deck.models.byName(name)
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

#to use create_a_label see the locals() thing below 

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

  
#moved to arbitrary.py
# def convert_notes_of_model(source_model_id, dest_model_id, old_patt="(.*) (.*)\. (.*)\. (.*)\.", new_fields=[]):
# def convert_note(note_id, patt, new_fields):

def old_convert_note(note_id, patt, new_fields):
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

    
### BAD STUFF ABOVE? NOT SURE
### PASTE IN

HC_EXAMPLE_DICT = {
    'Front': 'This is the front ' +  datetime.datetime.now().strftime("%I:%M%p on %B %d, %Y"),
    'Back': 'This is the back ' +  datetime.datetime.now().strftime("%I:%M%p on %B %d, %Y"),
    'declension_context': 'some context',
    'gender': 'm f n',
    'number': 'singular',
    'case': 'nominagenitavocative',
  }


def set_current_model(model_name=SOURCE_DECLENSION):
  model = mw.col.models.byName(model_name)
  cdeck = mw.col.decks.current()
  cdeck['mid']= model['id']
  return mw.col.decks.save(cdeck)        
  

def assert_intended_model(model_name=SOURCE_DECLENSION):
  assert mw.col.models.current()['id'] == mw.col.models.byName(model_name)['id']

def create_note(model_name, dict):
  global set_current_model
  global assert_intended_model
  set_current_model(model_name)
  #assert_intended_model(model_name)
  new_note = mw.col.newNote()
  for k, v in dict.iteritems():
    new_note[k] = v
  new_count = mw.col.addNote(new_note)
  return new_count
  
def create_hardcoded_note():
  global create_note
  dict = HC_EXAMPLE_DICT
  return create_note(SOURCE_DECLENSION, dict)

#Probably some library implementation of this?
def get_match_groups(patt, text): 
  rv = []
  match = re.match(patt, text)
  for i in range (0, 100):    #I don't really want [0] but keep for standardization
    try:
      rv.append(match.group(i))
    except:
      return rv
  showInfo("Surprising. Didn't expect 100")
  return rv
  
def dict_from(match_groups, back):
  global dict_from
  return {
    'Front': 'PHILIP dict_from front | ' +  datetime.datetime.now().strftime("%I:%M%p on %B %d, %Y"),
    'Back': back,
    'declension_context': match_groups[1],
    'gender': match_groups[2],
    'number': match_groups[3],
    'case': match_groups[4],
  }

def convert_note(note_id, patt, new_fields):
  global SOURCE_DECLENSION
  global get_match_groups
  src_note = mw.col.getNote(note_id)
  match_groups = get_match_groups(patt, src_note['Front'])
  new_count = create_note(SOURCE_DECLENSION, dict_from(match_groups, src_note['Back']))
  return new_count


### END PASTE IN
###     
###     
    

action = QAction("Philip (from the .local place): Run arbitrary.py", mw)
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


# def old_main():
  # import philip.main

  # patt = "(.*) (.*)\. (.*)\. (.*)\."
  # fields=get_list_from_file()
  # global _logstring
  # try:
    # new_notes, rv = convert_notes_of_model(SOURCE_DECLENSION_MODEL, DESTINATION_DECLENSION_MODEL, patt, fields)
  # except:
    # showInfo(_logstring)
    # raise
  # showInfo(_logstring)
  # create_a_label("RV is %s" % rv, 25)


	###########################################################################

### __init__.py but still was live
#This is redundant. See anki code,  m = self.deck.models.byName(name)
def id_for_first_model_matching(patt):
  all_models = mw.col.models.all()
  for model in all_models:
    if re.match(patt, model['name']):
      return model['id']



################################################################################
# From my arbitrary.py file.

# from aqt import mw

# action = QAction("Philip 2", mw)
# action.triggered.connect(main)
# mw.form.menuTools.addAction(action)



#### Sooooo bloated  
# def old_convert_note(note_id, patt, new_fields):
  # note = mw.col.getNote(note_id)
  # the_match = re.match(patt, note['Front'])
  # if (not the_match):
    ##showInfo("Could not match %s with %s" % (patt, note['Front'] ))
    # return (None, 'No equivalent')


  # the_dict = {}
  # new_note=make_new_declension_note()
  # for i in range(1,5):
    # try:
      # new_note[new_fields[i-1]] = the_match.group(i)
    # except KeyError:
      # print( "You probably used a note type without a field for " + new_fields[i-1])
      # silly_keys(new_note.keys()) 

      # raise
  # global _logstring
  # _logstring += "\nstr is %s\n" % str
  # mw.col.log("str is %s" % str)
  
  # new_note['Front'] += "SYNTHETIC: "
  # new_count = mw.col.addNote(new_note)

  # _logstring += ("new count of notes is %d\n" % new_count)
  # return (new_note, str)
  
## GUI STUFF
#create_a_label removed from here to reedanki.
#mw.setCentralWidget(label) 

#Diagnostic
# all_source_note_ids = mw.col.findNotes("mid:%d" % SOURCE_DECLENSION_MODEL)
# id = all_source_note_ids[0]
# old_patt="(.*) (.*)\. (.*)\. (.*)\."
# new_fields=HC_EXAMPLE_DICT.keys()
# rv=convert_note(id, old_patt, new_fields)
# showInfo(str(rv))

# try: 
  # assert_intended_model(SOURCE_DECLENSION_MODEL)
# except:
  # showInfo("Bad model %s" % mw.col.models.current()['id'])


# rv = create_hardcoded_note()
# assert rv > 0

# showInfo("Worked even better!")


#HOW TO ACTUALLY CHANGE THE CURRENT DECK
#See the code here: 
#https://github.com/dae/anki/blob/master/aqt/modelchooser.py

# m = self.deck.models.byName(ret.name)
# self.deck.conf['curModel'] = m['id']
# cdeck = self.deck.decks.current()
# cdeck['mid'] = m['id']
# self.deck.decks.save(cdeck)

#In our environment it's like this:         
# s = 'Cloze'
# m = mw.col.models.byName(s)
# cdeck = mw.col.decks.current()
# cdeck['mid']= m['id']
# rv=mw.col.decks.save(cdeck)        
#END HOW TO ACTUALLY CHANGE THE CURRENT DECK


### arbitrary.py but still was live
def convert_notes_of_model(source_model_id, dest_model_id, old_patt="(.*) (.*)\. (.*)\. (.*)\.", new_fields=[]):
  msg = "convert_notes_of_model() is a little too spaghetti code for us to use right now, but come back to this."
  showInfo(msg)
  raise msg




