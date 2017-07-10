from Midi_Fighter_64 import Midi_Fighter_64

def create_instance(c_instance):
	return Midi_Fighter_64(c_instance)

from _Framework.Capabilities import *

def get_capabilities():
	return {CONTROLLER_ID_KEY: controller_id(vendor_id=2580, product_ids=[0008], model_name='Midi Fighter 64'),
	 PORTS_KEY: [inport(props=[NOTES_CC, SCRIPT, REMOTE]), outport(props=[SCRIPT, REMOTE])]}