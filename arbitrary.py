from reedanki.library import * 
from aqt.utils import tooltip
print(type(tooltip))
print (type(HC_EXAMPLE_DICT))
print("****XXX")
print(type(convert_note))

from aqt import mw

def foo():
	print("In foo")
	print (type(HC_EXAMPLE_DICT))
	print("YY****XXX")
	print(type(library.convert_note))
foo()

### SOURCE_DECLENSION = 'de-declin' #remove this; it's redundant

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
  
  


  
#MW=mw
def do_dumb_shit():
  button = QPushButton('PHILIP')
  button.show()


  action = QAction("A bogus item " + datetime.datetime.now().strftime("%I:%M%p "), mw)
  action.triggered.connect(dir)
  # mw.form.menuTools.addAction(action)
  
  create_a_label("PHILIP", 100)
  create_a_label("HEY", 150)
  create_a_label("THERE", 200)
  create_a_label("WHAT", 250)
  

list_of_counts = convert_notes_hardcoded_model()
# showInfo("convert_notes_hardcoded_model \n %s" % list_of_counts)
do_dumb_shit()
showInfo("I just did dumb stuff and created a button.")
