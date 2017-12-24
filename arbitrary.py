from aqt import mw
import re
import importlib
importlib.reload(reedlibrary)

## This is profoundly inelegant but I don't know best practices for constants
# in an Anki addon. Module import-s do not behave as normal Python   
HC_EXAMPLE_DICT = reedlibrary.HC_EXAMPLE_DICT
SOURCE_DECLENSION_MODEL = reedlibrary.SOURCE_DECLENSION_MODEL
SOURCE_DECLENSION = reedlibrary.SOURCE_DECLENSION
convert_note = reedlibrary.convert_note



def convert_notes_hardcoded_model():
  global HC_EXAMPLE_DICT
  global SOURCE_DECLENSION_MODEL
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

