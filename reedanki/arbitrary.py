SOURCE_DECLENSION = 'de-declin' #remove this; it's redundant
# from aqt import mw

# action = QAction("Philip 2", mw)
# action.triggered.connect(main)
# mw.form.menuTools.addAction(action)
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
  #set_current_model(model_name)
  assert_intended_model(model_name)
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
    'Front': 'dict_from front | ' +  datetime.datetime.now().strftime("%I:%M%p on %B %d, %Y"),
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
#### Sooooo bloated  
def old_convert_note(note_id, patt, new_fields):
  note = mw.col.getNote(note_id)
  the_match = re.match(patt, note['Front'])
  if (not the_match):
    #showInfo("Could not match %s with %s" % (patt, note['Front'] ))
    return (None, 'No equivalent')


  the_dict = {}
  new_note=make_new_declension_note()
  for i in range(1,5):
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
  
  new_note['Front'] += "SYNTHETIC: "
  new_count = mw.col.addNote(new_note)

  _logstring += ("new count of notes is %d\n" % new_count)
  return (new_note, str)
  
def convert_notes_of_model(source_model_id, dest_model_id, old_patt="(.*) (.*)\. (.*)\. (.*)\.", new_fields=[]):
  msg = "convert_notes_of_model() is a little too spaghetti code for us to use right now, but come back to this."
  showInfo(msg)
  raise msg

def convert_notes_hardcoded_model():
  global HC_EXAMPLE_DICT
  global convert_note
  source_model_id = SOURCE_DECLENSION_MODEL
  dest_model_id = source_model_id
  old_patt="(.*) (.*)\. (.*)\. (.*)\."
  new_fields=HC_EXAMPLE_DICT.keys()

  all_source_note_ids = mw.col.findNotes("mid:%d" % source_model_id)
  THROTTLE = 2
  all_source_note_ids = all_source_note_ids[0 : THROTTLE]
  rv_notes = [convert_note(id, old_patt, new_fields) for id in all_source_note_ids]
  return rv_notes
  
  

## GUI STUFF
def create_a_label(text, x=25):
  label = QLabel()
  label.setText(text)
  label.setGeometry(x, x/2 , 300 , 300,)
  layout = mw.layout()
  layout.addWidget(label)
  mw.setLayout(layout)
#mw.setCentralWidget(label) 

  
#MW=mw
def do_dumb_shit():
  action = QAction("A bogus item " + datetime.datetime.now().strftime("%I:%M%p "), mw)
  action.triggered.connect(dir)
  # mw.form.menuTools.addAction(action)
  
  create_a_label("PHILIP", 100)
  create_a_label("HEY", 150)
  create_a_label("THERE", 200)
  create_a_label("WHAT", 250)
  
#do_dumb_shit()
list_of_counts = convert_notes_hardcoded_model()
showInfo("convert_notes_hardcoded_model \n %s" % list_of_counts)
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