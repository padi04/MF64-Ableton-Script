from __future__ import with_statement
import Live
from _Framework.ControlSurface import ControlSurface
from _Framework.DeviceComponent import DeviceComponent
from _Framework.MixerComponent import MixerComponent # Class encompassing several channel strips to form a mixer
from _Framework.SliderElement import SliderElement
from _Framework.TransportComponent import TransportComponent
from _Framework.InputControlElement import *
from _Framework.ButtonElement import ButtonElement
from _Framework.ButtonMatrixElement import ButtonMatrixElement
from _Framework.SessionComponent import SessionComponent
from _Framework.EncoderElement import *
from Launchpad.ConfigurableButtonElement import ConfigurableButtonElement
from pushbase import colors
from SkinDefault import make_rgb_skin, make_default_skin


class Midi_Fighter_64(ControlSurface):

	def __init__(self, c_instance):
		super(Midi_Fighter_64, self).__init__(c_instance)
		self._color_skin = make_rgb_skin()
		self._default_skin = make_default_skin()
		with self.component_guard():
			global _map_modes
			_map_modes = Live.MidiMap.MapMode
			self.current_track_offset = 0
			self.current_scene_offset = 0
			# mixer
			global mixer
			num_tracks = 128
			num_returns = 24
			self.mixer = MixerComponent(num_tracks, num_returns)
			global active_mode
			self._mode0()
			active_mode = "_mode1"
			self._set_active_mode()
			self._set_track_select_led()
 			self.show_message("Powered by DJ TechTools")


	def _mode4(self):
		self.show_message("_mode4 is active")
		# mixer
		global mixer
		# session
		global _session
		num_tracks = 8
		num_scenes = 7
		self._session = SessionComponent(num_tracks, num_scenes)
  		clip_color_table = colors.LIVE_COLORS_TO_MIDI_VALUES.copy()
 		clip_color_table[16777215] = 119
 		self._session.set_rgb_mode(colors.LIVE_COLORS_TO_MIDI_VALUES, colors.RGB_COLOR_TABLE)
		track_offset = self.current_track_offset
		scene_offset = self.current_scene_offset
		self._session.set_offsets(track_offset, scene_offset)
		self._session._reassign_scenes()
		self.set_highlighting_session_component(self._session)
		# clip launch buttons
		session_buttons = [60, 61, 62, 63, 92, 93, 94, 95, 56, 57, 58, 59, 88, 89, 90, 91, 52, 53, 54, 55, 84, 85, 86, 87, 48, 49, 50, 51, 80, 81, 82, 83, 44, 45, 46, 47, 76, 77, 78, 79, 40, 41, 42, 43, 72, 73, 74, 75, 36, 37, 38, 39, 68, 69, 70, 71]
		session_channels = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
		session_types = [MIDI_NOTE_TYPE, MIDI_NOTE_TYPE, MIDI_NOTE_TYPE, MIDI_NOTE_TYPE, MIDI_NOTE_TYPE, MIDI_NOTE_TYPE, MIDI_NOTE_TYPE, MIDI_NOTE_TYPE, MIDI_NOTE_TYPE, MIDI_NOTE_TYPE, MIDI_NOTE_TYPE, MIDI_NOTE_TYPE, MIDI_NOTE_TYPE, MIDI_NOTE_TYPE, MIDI_NOTE_TYPE, MIDI_NOTE_TYPE, MIDI_NOTE_TYPE, MIDI_NOTE_TYPE, MIDI_NOTE_TYPE, MIDI_NOTE_TYPE, MIDI_NOTE_TYPE, MIDI_NOTE_TYPE, MIDI_NOTE_TYPE, MIDI_NOTE_TYPE, MIDI_NOTE_TYPE, MIDI_NOTE_TYPE, MIDI_NOTE_TYPE, MIDI_NOTE_TYPE, MIDI_NOTE_TYPE, MIDI_NOTE_TYPE, MIDI_NOTE_TYPE, MIDI_NOTE_TYPE, MIDI_NOTE_TYPE, MIDI_NOTE_TYPE, MIDI_NOTE_TYPE, MIDI_NOTE_TYPE, MIDI_NOTE_TYPE, MIDI_NOTE_TYPE, MIDI_NOTE_TYPE, MIDI_NOTE_TYPE, MIDI_NOTE_TYPE, MIDI_NOTE_TYPE, MIDI_NOTE_TYPE, MIDI_NOTE_TYPE, MIDI_NOTE_TYPE, MIDI_NOTE_TYPE, MIDI_NOTE_TYPE, MIDI_NOTE_TYPE, MIDI_NOTE_TYPE, MIDI_NOTE_TYPE, MIDI_NOTE_TYPE, MIDI_NOTE_TYPE, MIDI_NOTE_TYPE, MIDI_NOTE_TYPE, MIDI_NOTE_TYPE, MIDI_NOTE_TYPE]
		session_is_momentary = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
		self._pads = [ButtonElement(session_is_momentary[index], session_types[index], session_channels[index], session_buttons[index]) for index in range(num_tracks*num_scenes)]
		self._grid = ButtonMatrixElement(rows=[self._pads[(index*num_tracks):(index*num_tracks)+num_tracks] for index in range(num_scenes)])
		self._session.set_clip_launch_buttons(self._grid)
		# LED feedback
		self._session._enable_skinning()
		for scene_index in range(num_scenes):
			scene = self._session.scene(scene_index)
			for track_index in range(num_tracks):
				clip_slot = scene.clip_slot(track_index)
				clip_slot.set_triggered_to_play_value(61)
				clip_slot.set_triggered_to_record_value(13)
				clip_slot.set_record_button_value(19)
				#clip_slot.set_stopped_value(49)
				#clip_slot.set_started_value(127)
				clip_slot.set_recording_value(13)
		self.delete_button = ConfigurableButtonElement(0, MIDI_NOTE_TYPE, 1, 67)
		self.delete_button.set_on_off_values(49, 55)
		self._session._link()
		self.refresh_state()
		self.clip_xtra_back = ConfigurableButtonElement(1, MIDI_NOTE_TYPE, 1, 96)
		self.clip_xtra_back.add_value_listener(self._activate_mode1,identify_sender= False)
		self.clip_xtra_back.send_value(85)
		# transport
		global transport
		self.transport = TransportComponent()
		self.transport.name = 'Transport'
		overdub_button = ConfigurableButtonElement(1, MIDI_NOTE_TYPE, 1, 64)
		overdub_button.set_on_off_values(13, 19)
		overdub_button.name = 'overdub_button'
		self.transport.set_overdub_button(overdub_button)
		if((hasattr(self, 'clip_xtra')) and (self.clip_xtra is not None)):
			self.clip_xtra.send_value(85)

	def _remove_mode4(self):
		# mixer
		global mixer
		# session
		global _session
		# clip launch buttons
		self._session.set_clip_launch_buttons(None)
		self.set_highlighting_session_component(None)
		self.current_track_offset = self._session._track_offset
		self.current_scene_offset = self._session._scene_offset
		self._session._unlink()
		self._session = None
		self.clip_xtra_back.send_value(0)
		self.clip_xtra_back.remove_value_listener(self._activate_mode1)
		self.clip_xtra_back = None
		# transport
		global transport
		self.transport.set_overdub_button(None)
		self.transport = None
		if((hasattr(self, 'clip_xtra')) and (self.clip_xtra is not None)):
			self.clip_xtra.send_value(91)

	def _mode1(self):
		self.show_message("_mode1 is active")
		# mixer
		global mixer
		# session
		global _session
		num_tracks = 8
		num_scenes = 7
# 		self._session = SessionComponent(auto_name=True, is_enabled=False, enable_skinning=True)
		self._session = SessionComponent(num_tracks, num_scenes)
  		clip_color_table = colors.LIVE_COLORS_TO_MIDI_VALUES.copy()
 		clip_color_table[16777215] = 119
 		self._session.set_rgb_mode(colors.LIVE_COLORS_TO_MIDI_VALUES, colors.RGB_COLOR_TABLE)
		track_offset = self.current_track_offset
		scene_offset = self.current_scene_offset
		self._session.set_offsets(track_offset, scene_offset)
		self._session._reassign_scenes()
		self.set_highlighting_session_component(self._session)
		# clip launch buttons
		session_buttons = [60, 61, 62, 63, 92, 93, 94, 95, 56, 57, 58, 59, 88, 89, 90, 91, 52, 53, 54, 55, 84, 85, 86, 87, 48, 49, 50, 51, 80, 81, 82, 83, 44, 45, 46, 47, 76, 77, 78, 79, 40, 41, 42, 43, 72, 73, 74, 75, 36, 37, 38, 39, 68, 69, 70, 71]
		session_channels = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
		session_types = [MIDI_NOTE_TYPE, MIDI_NOTE_TYPE, MIDI_NOTE_TYPE, MIDI_NOTE_TYPE, MIDI_NOTE_TYPE, MIDI_NOTE_TYPE, MIDI_NOTE_TYPE, MIDI_NOTE_TYPE, MIDI_NOTE_TYPE, MIDI_NOTE_TYPE, MIDI_NOTE_TYPE, MIDI_NOTE_TYPE, MIDI_NOTE_TYPE, MIDI_NOTE_TYPE, MIDI_NOTE_TYPE, MIDI_NOTE_TYPE, MIDI_NOTE_TYPE, MIDI_NOTE_TYPE, MIDI_NOTE_TYPE, MIDI_NOTE_TYPE, MIDI_NOTE_TYPE, MIDI_NOTE_TYPE, MIDI_NOTE_TYPE, MIDI_NOTE_TYPE, MIDI_NOTE_TYPE, MIDI_NOTE_TYPE, MIDI_NOTE_TYPE, MIDI_NOTE_TYPE, MIDI_NOTE_TYPE, MIDI_NOTE_TYPE, MIDI_NOTE_TYPE, MIDI_NOTE_TYPE, MIDI_NOTE_TYPE, MIDI_NOTE_TYPE, MIDI_NOTE_TYPE, MIDI_NOTE_TYPE, MIDI_NOTE_TYPE, MIDI_NOTE_TYPE, MIDI_NOTE_TYPE, MIDI_NOTE_TYPE, MIDI_NOTE_TYPE, MIDI_NOTE_TYPE, MIDI_NOTE_TYPE, MIDI_NOTE_TYPE, MIDI_NOTE_TYPE, MIDI_NOTE_TYPE, MIDI_NOTE_TYPE, MIDI_NOTE_TYPE, MIDI_NOTE_TYPE, MIDI_NOTE_TYPE, MIDI_NOTE_TYPE, MIDI_NOTE_TYPE, MIDI_NOTE_TYPE, MIDI_NOTE_TYPE, MIDI_NOTE_TYPE, MIDI_NOTE_TYPE]
		session_is_momentary = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
		self._pads = [ButtonElement(session_is_momentary[index], session_types[index], session_channels[index], session_buttons[index]) for index in range(num_tracks*num_scenes)]
		self._grid = ButtonMatrixElement(rows=[self._pads[(index*num_tracks):(index*num_tracks)+num_tracks] for index in range(num_scenes)])
		self._session.set_clip_launch_buttons(self._grid)
		# LED feedback
		self._session._enable_skinning()
		for scene_index in range(num_scenes):
			scene = self._session.scene(scene_index)
			for track_index in range(num_tracks):
				clip_slot = scene.clip_slot(track_index)
				clip_slot.set_triggered_to_play_value(61)
				clip_slot.set_triggered_to_record_value(13)
				clip_slot.set_record_button_value(19)
				#clip_slot.set_stopped_value(49)
				#clip_slot.set_started_value(127)
				clip_slot.set_recording_value(13)
		# session navigation
		self.session_up = ConfigurableButtonElement(0, MIDI_NOTE_TYPE, 1, 64)
		self.session_up.set_on_off_values(25, 31)
		self._session.set_page_up_button(self.session_up)
		self.session_down = ConfigurableButtonElement(0, MIDI_NOTE_TYPE, 1, 65)
		self.session_down.set_on_off_values(25, 31)
		self._session.set_page_down_button(self.session_down)
		self.session_left = ConfigurableButtonElement(0, MIDI_NOTE_TYPE, 1, 66)
		self.session_left.set_on_off_values(25, 31)
		self._session.set_page_left_button(self.session_left)
		self.session_right = ConfigurableButtonElement(0, MIDI_NOTE_TYPE, 1, 67)
		self.session_right.set_on_off_values(25, 31)
		self._session.set_page_right_button(self.session_right)
		self._session._link()
		self.refresh_state()
		self.clip_xtra = ConfigurableButtonElement(1, MIDI_NOTE_TYPE, 1, 96)
		self.clip_xtra.add_value_listener(self._activate_mode4,identify_sender= False)
		self.clip_xtra.send_value(91)
		if((hasattr(self, 'clip_xtra_back')) and (self.clip_xtra_back is not None)):
			self.clip_xtra_back.send_value(91)

	def _remove_mode1(self):
		# mixer
		global mixer
		# session
		global _session
		# clip launch buttons
		self._session.set_clip_launch_buttons(None)
		self.set_highlighting_session_component(None)
		# session navigation
		self._session.set_page_up_button(None)
		self._session.set_page_down_button(None)
		self._session.set_page_left_button(None)
		self._session.set_page_right_button(None)
		self.current_track_offset = self._session._track_offset
		self.current_scene_offset = self._session._scene_offset
		self._session._unlink()
		self._session = None
		self.clip_xtra.send_value(0)
		self.clip_xtra.remove_value_listener(self._activate_mode4)
		self.clip_xtra = None
		if((hasattr(self, 'clip_xtra_back')) and (self.clip_xtra_back is not None)):
			self.clip_xtra_back.send_value(85)

	def _mode2(self):
		self.show_message("_mode2 is active")
		# mixer
		global mixer
		# session
		global _session
		num_tracks = 8
		num_scenes = 7
		self._session = SessionComponent(num_tracks, num_scenes)
  		clip_color_table = colors.LIVE_COLORS_TO_MIDI_VALUES.copy()
 		clip_color_table[16777215] = 119
 		self._session.set_rgb_mode(colors.LIVE_COLORS_TO_MIDI_VALUES, colors.RGB_COLOR_TABLE)
		track_offset = self.current_track_offset
		scene_offset = self.current_scene_offset
		self._session.set_offsets(track_offset, scene_offset)
		self._session._reassign_scenes()
		self.set_highlighting_session_component(self._session)
		# clip launch buttons
		session_buttons = [60, 61, 62, 63, 92, 93, 94, 121, 56, 57, 58, 59, 88, 89, 90, 122, 52, 53, 54, 55, 84, 85, 86, 123, 48, 49, 50, 51, 80, 81, 82, 124, 44, 45, 46, 47, 76, 77, 78, 125, 40, 41, 42, 43, 72, 73, 74, 126, 36, 37, 38, 39, 68, 69, 70, 127]
		session_channels = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
		session_types = [MIDI_NOTE_TYPE, MIDI_NOTE_TYPE, MIDI_NOTE_TYPE, MIDI_NOTE_TYPE, MIDI_NOTE_TYPE, MIDI_NOTE_TYPE, MIDI_NOTE_TYPE, MIDI_NOTE_TYPE, MIDI_NOTE_TYPE, MIDI_NOTE_TYPE, MIDI_NOTE_TYPE, MIDI_NOTE_TYPE, MIDI_NOTE_TYPE, MIDI_NOTE_TYPE, MIDI_NOTE_TYPE, MIDI_NOTE_TYPE, MIDI_NOTE_TYPE, MIDI_NOTE_TYPE, MIDI_NOTE_TYPE, MIDI_NOTE_TYPE, MIDI_NOTE_TYPE, MIDI_NOTE_TYPE, MIDI_NOTE_TYPE, MIDI_NOTE_TYPE, MIDI_NOTE_TYPE, MIDI_NOTE_TYPE, MIDI_NOTE_TYPE, MIDI_NOTE_TYPE, MIDI_NOTE_TYPE, MIDI_NOTE_TYPE, MIDI_NOTE_TYPE, MIDI_NOTE_TYPE, MIDI_NOTE_TYPE, MIDI_NOTE_TYPE, MIDI_NOTE_TYPE, MIDI_NOTE_TYPE, MIDI_NOTE_TYPE, MIDI_NOTE_TYPE, MIDI_NOTE_TYPE, MIDI_NOTE_TYPE, MIDI_NOTE_TYPE, MIDI_NOTE_TYPE, MIDI_NOTE_TYPE, MIDI_NOTE_TYPE, MIDI_NOTE_TYPE, MIDI_NOTE_TYPE, MIDI_NOTE_TYPE, MIDI_NOTE_TYPE, MIDI_NOTE_TYPE, MIDI_NOTE_TYPE, MIDI_NOTE_TYPE, MIDI_NOTE_TYPE, MIDI_NOTE_TYPE, MIDI_NOTE_TYPE, MIDI_NOTE_TYPE, MIDI_NOTE_TYPE]
		session_is_momentary = [1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 0]
		self._pads = [ButtonElement(session_is_momentary[index], session_types[index], session_channels[index], session_buttons[index]) for index in range(num_tracks*num_scenes)]
		self._grid = ButtonMatrixElement(rows=[self._pads[(index*num_tracks):(index*num_tracks)+num_tracks] for index in range(num_scenes)])
		self._session.set_clip_launch_buttons(self._grid)
		# session scene launch
		scene_buttons = [95, 91, 87, 83, 79, 75, 71]
		scene_channels = [1, 1, 1, 1, 1, 1, 1]
		scene_types = [MIDI_NOTE_TYPE, MIDI_NOTE_TYPE, MIDI_NOTE_TYPE, MIDI_NOTE_TYPE, MIDI_NOTE_TYPE, MIDI_NOTE_TYPE, MIDI_NOTE_TYPE]
		scene_momentarys = [1, 1, 1, 1, 1, 1, 1]
		self._scene_launch_buttons = [ButtonElement(scene_momentarys[index], scene_types[index], scene_channels[index], scene_buttons[index]) for index in range(num_scenes)]
		self._scene_launch_buttons = ButtonMatrixElement(rows=[self._scene_launch_buttons])
		self._session.set_scene_launch_buttons(self._scene_launch_buttons)
		# LED feedback
		self._session._enable_skinning()
		for scene_index in range(num_scenes):
			scene = self._session.scene(scene_index)
			scene.set_scene_value(127)
			scene.set_no_scene_value(0)
			scene.set_triggered_value(61)
			for track_index in range(num_tracks):
				clip_slot = scene.clip_slot(track_index)
				clip_slot.set_triggered_to_play_value(61)
				clip_slot.set_triggered_to_record_value(13)
				clip_slot.set_record_button_value(19)
				#clip_slot.set_stopped_value(49)
				#clip_slot.set_started_value(127)
				clip_slot.set_recording_value(13)
		self._session._link()
		self.refresh_state()
		if((hasattr(self, 'scene_shift')) and (self.scene_shift is not None)):
			self.scene_shift.send_value(127)

	def _remove_mode2(self):
		# mixer
		global mixer
		# session
		global _session
		# clip launch buttons
		self._session.set_clip_launch_buttons(None)
		self.set_highlighting_session_component(None)
		# session scene launch
		self._scene_launch_buttons = None
		self._session.set_scene_launch_buttons(None)
		self.current_track_offset = self._session._track_offset
		self.current_scene_offset = self._session._scene_offset
		self._session._unlink()
		self._session = None
		if((hasattr(self, 'scene_shift')) and (self.scene_shift is not None)):
			self.scene_shift.send_value(66)

	def _mode0(self):
		self.show_message("_mode0 is active")
		# mixer
		global mixer
		self.scene_shift = ConfigurableButtonElement(1, MIDI_NOTE_TYPE, 1, 99)
		self.scene_shift.add_value_listener(self._activate_shift_mode2,identify_sender= False)
		self.scene_shift.send_value(66)
		self.shift_mixer = ConfigurableButtonElement(1, MIDI_NOTE_TYPE, 1, 98)
		self.shift_mixer.add_value_listener(self._activate_shift_mode3,identify_sender= False)
		self.shift_mixer.send_value(37)

	def _remove_mode0(self):
		# mixer
		global mixer
		self.scene_shift.send_value(0)
		self.scene_shift.remove_value_listener(self._activate_shift_mode2)
		self.scene_shift = None
		self.shift_mixer.send_value(0)
		self.shift_mixer.remove_value_listener(self._activate_shift_mode3)
		self.shift_mixer = None

	def _mode3(self):
		self.show_message("_mode3 is active")
		# mixer
		global mixer
		arm_specific_0 = ConfigurableButtonElement(1, MIDI_NOTE_TYPE, 1, 40)
		arm_specific_0.set_on_off_values(13, 19)
		self.mixer.channel_strip(0).set_arm_button(arm_specific_0)
		arm_specific_1 = ConfigurableButtonElement(1, MIDI_NOTE_TYPE, 1, 41)
		arm_specific_1.set_on_off_values(13, 19)
		self.mixer.channel_strip(1).set_arm_button(arm_specific_1)
		arm_specific_2 = ConfigurableButtonElement(1, MIDI_NOTE_TYPE, 1, 42)
		arm_specific_2.set_on_off_values(13, 19)
		self.mixer.channel_strip(2).set_arm_button(arm_specific_2)
		arm_specific_3 = ConfigurableButtonElement(1, MIDI_NOTE_TYPE, 1, 43)
		arm_specific_3.set_on_off_values(13, 19)
		self.mixer.channel_strip(3).set_arm_button(arm_specific_3)
		arm_specific_4 = ConfigurableButtonElement(1, MIDI_NOTE_TYPE, 1, 72)
		arm_specific_4.set_on_off_values(13, 19)
		self.mixer.channel_strip(4).set_arm_button(arm_specific_4)
		arm_specific_5 = ConfigurableButtonElement(1, MIDI_NOTE_TYPE, 1, 73)
		arm_specific_5.set_on_off_values(13, 19)
		self.mixer.channel_strip(5).set_arm_button(arm_specific_5)
		arm_specific_6 = ConfigurableButtonElement(1, MIDI_NOTE_TYPE, 1, 74)
		arm_specific_6.set_on_off_values(13, 19)
		self.mixer.channel_strip(6).set_arm_button(arm_specific_6)
		arm_specific_7 = ConfigurableButtonElement(1, MIDI_NOTE_TYPE, 1, 75)
		arm_specific_7.set_on_off_values(13, 19)
		self.mixer.channel_strip(7).set_arm_button(arm_specific_7)
		solo_specific_0 = ConfigurableButtonElement(1, MIDI_NOTE_TYPE, 1, 44)
		solo_specific_0.set_on_off_values(85, 91)
		self.mixer.channel_strip(0).set_solo_button(solo_specific_0)
		solo_specific_1 = ConfigurableButtonElement(1, MIDI_NOTE_TYPE, 1, 45)
		solo_specific_1.set_on_off_values(85, 91)
		self.mixer.channel_strip(1).set_solo_button(solo_specific_1)
		solo_specific_2 = ConfigurableButtonElement(1, MIDI_NOTE_TYPE, 1, 46)
		solo_specific_2.set_on_off_values(85, 91)
		self.mixer.channel_strip(2).set_solo_button(solo_specific_2)
		solo_specific_3 = ConfigurableButtonElement(1, MIDI_NOTE_TYPE, 1, 47)
		solo_specific_3.set_on_off_values(85, 91)
		self.mixer.channel_strip(3).set_solo_button(solo_specific_3)
		solo_specific_4 = ConfigurableButtonElement(1, MIDI_NOTE_TYPE, 1, 76)
		solo_specific_4.set_on_off_values(85, 91)
		self.mixer.channel_strip(4).set_solo_button(solo_specific_4)
		solo_specific_5 = ConfigurableButtonElement(1, MIDI_NOTE_TYPE, 1, 77)
		solo_specific_5.set_on_off_values(85, 91)
		self.mixer.channel_strip(5).set_solo_button(solo_specific_5)
		solo_specific_6 = ConfigurableButtonElement(1, MIDI_NOTE_TYPE, 1, 78)
		solo_specific_6.set_on_off_values(85, 91)
		self.mixer.channel_strip(6).set_solo_button(solo_specific_6)
		solo_specific_7 = ConfigurableButtonElement(1, MIDI_NOTE_TYPE, 1, 79)
		solo_specific_7.set_on_off_values(85, 91)
		self.mixer.channel_strip(7).set_solo_button(solo_specific_7)
		mute_specific_0 = ConfigurableButtonElement(1, MIDI_NOTE_TYPE, 1, 48)
		mute_specific_0.set_on_off_values(37, 43)
		self.mixer.channel_strip(0).set_mute_button(mute_specific_0)
		self.mixer.channel_strip(0).set_invert_mute_feedback(True)
		mute_specific_1 = ConfigurableButtonElement(1, MIDI_NOTE_TYPE, 1, 49)
		mute_specific_1.set_on_off_values(37, 43)
		self.mixer.channel_strip(1).set_mute_button(mute_specific_1)
		self.mixer.channel_strip(1).set_invert_mute_feedback(True)
		mute_specific_2 = ConfigurableButtonElement(1, MIDI_NOTE_TYPE, 1, 50)
		mute_specific_2.set_on_off_values(37, 43)
		self.mixer.channel_strip(2).set_mute_button(mute_specific_2)
		self.mixer.channel_strip(2).set_invert_mute_feedback(True)
		mute_specific_3 = ConfigurableButtonElement(1, MIDI_NOTE_TYPE, 1, 51)
		mute_specific_3.set_on_off_values(37, 43)
		self.mixer.channel_strip(3).set_mute_button(mute_specific_3)
		self.mixer.channel_strip(3).set_invert_mute_feedback(True)
		mute_specific_4 = ConfigurableButtonElement(1, MIDI_NOTE_TYPE, 1, 80)
		mute_specific_4.set_on_off_values(37, 43)
		self.mixer.channel_strip(4).set_mute_button(mute_specific_4)
		self.mixer.channel_strip(4).set_invert_mute_feedback(True)
		mute_specific_5 = ConfigurableButtonElement(0, MIDI_NOTE_TYPE, 1, 81)
		mute_specific_5.set_on_off_values(37, 43)
		self.mixer.channel_strip(5).set_mute_button(mute_specific_5)
		self.mixer.channel_strip(5).set_invert_mute_feedback(True)
		mute_specific_6 = ConfigurableButtonElement(1, MIDI_NOTE_TYPE, 1, 82)
		mute_specific_6.set_on_off_values(37, 43)
		self.mixer.channel_strip(6).set_mute_button(mute_specific_6)
		self.mixer.channel_strip(6).set_invert_mute_feedback(True)
		mute_specific_7 = ConfigurableButtonElement(1, MIDI_NOTE_TYPE, 1, 83)
		mute_specific_7.set_on_off_values(37, 43)
		self.mixer.channel_strip(7).set_mute_button(mute_specific_7)
		self.mixer.channel_strip(7).set_invert_mute_feedback(True)
		# session
		global _session
		num_tracks = 8
		num_scenes = 7
		self._session = SessionComponent(num_tracks, num_scenes)
  		clip_color_table = colors.LIVE_COLORS_TO_MIDI_VALUES.copy()
 		clip_color_table[16777215] = 119
 		self._session.set_rgb_mode(colors.LIVE_COLORS_TO_MIDI_VALUES, colors.RGB_COLOR_TABLE)
		track_offset = self.current_track_offset
		scene_offset = self.current_scene_offset
		self._session.set_offsets(track_offset, scene_offset)
		self._session._reassign_scenes()
		self.set_highlighting_session_component(self._session)
		# session track stop
		stop_track_buttons = [36, 37, 38, 39, 68, 69, 70, 71]
		stop_track_channels = [1, 1, 1, 1, 1, 1, 1, 1]
		stop_track_types = [MIDI_NOTE_TYPE, MIDI_NOTE_TYPE, MIDI_NOTE_TYPE, MIDI_NOTE_TYPE, MIDI_NOTE_TYPE, MIDI_NOTE_TYPE, MIDI_NOTE_TYPE, MIDI_NOTE_TYPE]
		stop_track_is_momentary = [0, 0, 0, 0, 0, 0, 0, 0]
		self._track_stop_buttons = [ConfigurableButtonElement(stop_track_is_momentary[index], stop_track_types[index], stop_track_channels[index], stop_track_buttons[index]) for index in range(num_tracks)]
		self._session.set_stop_track_clip_buttons(tuple(self._track_stop_buttons))
		# LED feedback
		self._session._enable_skinning()
		self._session.set_stop_clip_triggered_value(61)
		self._session.set_stop_clip_value(127)
		for scene_index in range(num_scenes):
			scene = self._session.scene(scene_index)
			for track_index in range(num_tracks):
				clip_slot = scene.clip_slot(track_index)
		# session navigation
		self.session_left = ConfigurableButtonElement(0, MIDI_NOTE_TYPE, 1, 66)
		self.session_left.set_on_off_values(25, 31)
		self._session.set_page_left_button(self.session_left)
		self.session_right = ConfigurableButtonElement(0, MIDI_NOTE_TYPE, 1, 67)
		self.session_right.set_on_off_values(25, 31)
		self._session.set_page_right_button(self.session_right)
		self._session._link()
		self._session.set_mixer(self.mixer)
		self.refresh_state()
		# select track 1 button
		self.select_1 = ConfigurableButtonElement(1, MIDI_NOTE_TYPE, 1, 52)
		self.select_1.set_on_off_values(73, 79)
		self.select_1.add_value_listener(self.track_select_1, identify_sender=False)
		# select track 2 button
		self.select_2 = ConfigurableButtonElement(1, MIDI_NOTE_TYPE, 1, 53)
		self.select_2.set_on_off_values(73, 79)
		self.select_2.add_value_listener(self.track_select_2, identify_sender=False)
		# select track 3 button
		self.select_3 = ConfigurableButtonElement(1, MIDI_NOTE_TYPE, 1, 54)
		self.select_3.set_on_off_values(73, 79)
		self.select_3.add_value_listener(self.track_select_3, identify_sender=False)
		# select track 4 button
		self.select_4 = ConfigurableButtonElement(1, MIDI_NOTE_TYPE, 1, 55)
		self.select_4.set_on_off_values(73, 79)
		self.select_4.add_value_listener(self.track_select_4, identify_sender=False)
		# select track 5 button
		self.select_5 = ConfigurableButtonElement(1, MIDI_NOTE_TYPE, 1, 84)
		self.select_5.set_on_off_values(73, 79)
		self.select_5.add_value_listener(self.track_select_5, identify_sender=False)
		# select track 6 button
		self.select_6 = ConfigurableButtonElement(1, MIDI_NOTE_TYPE, 1, 85)
		self.select_6.set_on_off_values(73, 79)
		self.select_6.add_value_listener(self.track_select_6, identify_sender=False)
		# select track 7 button
		self.select_7 = ConfigurableButtonElement(1, MIDI_NOTE_TYPE, 1, 86)
		self.select_7.set_on_off_values(73, 79)
		self.select_7.add_value_listener(self.track_select_7, identify_sender=False)
		# select track 8 button
		self.select_8 = ConfigurableButtonElement(1, MIDI_NOTE_TYPE, 1, 87)
		self.select_8.set_on_off_values(73, 79)
		self.select_8.add_value_listener(self.track_select_8, identify_sender=False)
		if((hasattr(self, 'shift_mixer')) and (self.shift_mixer is not None)):
			self.shift_mixer.send_value(127)

	def _remove_mode3(self):
		# mixer
		global mixer
		self.mixer.channel_strip(0).set_arm_button(None)
		self.mixer.channel_strip(1).set_arm_button(None)
		self.mixer.channel_strip(2).set_arm_button(None)
		self.mixer.channel_strip(3).set_arm_button(None)
		self.mixer.channel_strip(4).set_arm_button(None)
		self.mixer.channel_strip(5).set_arm_button(None)
		self.mixer.channel_strip(6).set_arm_button(None)
		self.mixer.channel_strip(7).set_arm_button(None)
		self.mixer.channel_strip(0).set_solo_button(None)
		self.mixer.channel_strip(1).set_solo_button(None)
		self.mixer.channel_strip(2).set_solo_button(None)
		self.mixer.channel_strip(3).set_solo_button(None)
		self.mixer.channel_strip(4).set_solo_button(None)
		self.mixer.channel_strip(5).set_solo_button(None)
		self.mixer.channel_strip(6).set_solo_button(None)
		self.mixer.channel_strip(7).set_solo_button(None)
		self.mixer.channel_strip(0).set_mute_button(None)
		self.mixer.channel_strip(1).set_mute_button(None)
		self.mixer.channel_strip(2).set_mute_button(None)
		self.mixer.channel_strip(3).set_mute_button(None)
		self.mixer.channel_strip(4).set_mute_button(None)
		self.mixer.channel_strip(5).set_mute_button(None)
		self.mixer.channel_strip(6).set_mute_button(None)
		self.mixer.channel_strip(7).set_mute_button(None)
		# session
		global _session
		self.set_highlighting_session_component(None)
		self._session.set_mixer(None)
		# session track stop
		self._track_stop_buttons = None
		self._session.set_stop_track_clip_buttons(None)
		# session navigation
		self._session.set_page_left_button(None)
		self._session.set_page_right_button(None)
		self.current_track_offset = self._session._track_offset
		self.current_scene_offset = self._session._scene_offset
		self._session._unlink()
		self._session = None
		self.select_1.send_value(0)
		self.select_1.remove_value_listener(self.track_select_1)
		self.select_1 = None
		self.select_2.send_value(0)
		self.select_2.remove_value_listener(self.track_select_2)
		self.select_2 = None
		self.select_3.send_value(0)
		self.select_3.remove_value_listener(self.track_select_3)
		self.select_3 = None
		self.select_4.send_value(0)
		self.select_4.remove_value_listener(self.track_select_4)
		self.select_4 = None
		self.select_5.send_value(0)
		self.select_5.remove_value_listener(self.track_select_5)
		self.select_5 = None
		self.select_6.send_value(0)
		self.select_6.remove_value_listener(self.track_select_6)
		self.select_6 = None
		self.select_7.send_value(0)
		self.select_7.remove_value_listener(self.track_select_7)
		self.select_7 = None
		self.select_8.send_value(0)
		self.select_8.remove_value_listener(self.track_select_8)
		self.select_8 = None
		if((hasattr(self, 'shift_mixer')) and (self.shift_mixer is not None)):
			self.shift_mixer.send_value(37)

	def _set_track_select_led(self):
		self._turn_off_track_select_leds()
		# take sessionbox into account if its present
		offset = 0
		if (hasattr(self, '_session')):
			offset = self._session._track_offset
		num_of_tracks = len(self.song().tracks)
		# next is each track select item
		# select_1
		pos = offset + 0
		pos2 = pos + 1
		if num_of_tracks >= pos2:
			if(self.song().view.selected_track == self.song().tracks[pos]):
				if((hasattr(self, 'select_1')) and (self.select_1 is not None)):
					self.select_1.send_value(73)
		# select_2
		pos = offset + 1
		pos2 = pos + 1
		if num_of_tracks >= pos2:
			if(self.song().view.selected_track == self.song().tracks[pos]):
				if((hasattr(self, 'select_2')) and (self.select_2 is not None)):
					self.select_2.send_value(73)
		# select_3
		pos = offset + 2
		pos2 = pos + 1
		if num_of_tracks >= pos2:
			if(self.song().view.selected_track == self.song().tracks[pos]):
				if((hasattr(self, 'select_3')) and (self.select_3 is not None)):
					self.select_3.send_value(73)
		# select_4
		pos = offset + 3
		pos2 = pos + 1
		if num_of_tracks >= pos2:
			if(self.song().view.selected_track == self.song().tracks[pos]):
				if((hasattr(self, 'select_4')) and (self.select_4 is not None)):
					self.select_4.send_value(73)
		# select_5
		pos = offset + 4
		pos2 = pos + 1
		if num_of_tracks >= pos2:
			if(self.song().view.selected_track == self.song().tracks[pos]):
				if((hasattr(self, 'select_5')) and (self.select_5 is not None)):
					self.select_5.send_value(73)
		# select_6
		pos = offset + 5
		pos2 = pos + 1
		if num_of_tracks >= pos2:
			if(self.song().view.selected_track == self.song().tracks[pos]):
				if((hasattr(self, 'select_6')) and (self.select_6 is not None)):
					self.select_6.send_value(73)
		# select_7
		pos = offset + 6
		pos2 = pos + 1
		if num_of_tracks >= pos2:
			if(self.song().view.selected_track == self.song().tracks[pos]):
				if((hasattr(self, 'select_7')) and (self.select_7 is not None)):
					self.select_7.send_value(73)
		# select_8
		pos = offset + 7
		pos2 = pos + 1
		if num_of_tracks >= pos2:
			if(self.song().view.selected_track == self.song().tracks[pos]):
				if((hasattr(self, 'select_8')) and (self.select_8 is not None)):
					self.select_8.send_value(73)

	def _turn_off_track_select_leds(self):
		num_of_tracks = len(self.song().tracks)
		# take sessionbox into account if its present
		offset = 0
		if (hasattr(self, '_session')):
			offset = self._session._track_offset
		# select_1
		pos = offset + 0
		pos2 = pos + 1
		if ((num_of_tracks >= pos2) and (hasattr(self, 'select_1')) and (self.select_1 is not None)):
			self.select_1.send_value(79)
		elif ((num_of_tracks < pos2) and (hasattr(self, 'select_1')) and (self.select_1 is not None)):
			self.select_1.send_value(0)
		# select_2
		pos = offset + 1
		pos2 = pos + 1
		if ((num_of_tracks >= pos2) and (hasattr(self, 'select_2')) and (self.select_2 is not None)):
			self.select_2.send_value(79)
		elif ((num_of_tracks < pos2) and (hasattr(self, 'select_2')) and (self.select_2 is not None)):
			self.select_2.send_value(0)
		# select_3
		pos = offset + 2
		pos2 = pos + 1
		if ((num_of_tracks >= pos2) and (hasattr(self, 'select_3')) and (self.select_3 is not None)):
			self.select_3.send_value(79)
		elif ((num_of_tracks < pos2) and (hasattr(self, 'select_3')) and (self.select_3 is not None)):
			self.select_3.send_value(0)
		# select_4
		pos = offset + 3
		pos2 = pos + 1
		if ((num_of_tracks >= pos2) and (hasattr(self, 'select_4')) and (self.select_4 is not None)):
			self.select_4.send_value(79)
		elif ((num_of_tracks < pos2) and (hasattr(self, 'select_4')) and (self.select_4 is not None)):
			self.select_4.send_value(0)
		# select_5
		pos = offset + 4
		pos2 = pos + 1
		if ((num_of_tracks >= pos2) and (hasattr(self, 'select_5')) and (self.select_5 is not None)):
			self.select_5.send_value(79)
		elif ((num_of_tracks < pos2) and (hasattr(self, 'select_5')) and (self.select_5 is not None)):
			self.select_5.send_value(0)
		# select_6
		pos = offset + 5
		pos2 = pos + 1
		if ((num_of_tracks >= pos2) and (hasattr(self, 'select_6')) and (self.select_6 is not None)):
			self.select_6.send_value(79)
		elif ((num_of_tracks < pos2) and (hasattr(self, 'select_6')) and (self.select_6 is not None)):
			self.select_6.send_value(0)
		# select_7
		pos = offset + 6
		pos2 = pos + 1
		if ((num_of_tracks >= pos2) and (hasattr(self, 'select_7')) and (self.select_7 is not None)):
			self.select_7.send_value(79)
		elif ((num_of_tracks < pos2) and (hasattr(self, 'select_7')) and (self.select_7 is not None)):
			self.select_7.send_value(0)
		# select_8
		pos = offset + 7
		pos2 = pos + 1
		if ((num_of_tracks >= pos2) and (hasattr(self, 'select_8')) and (self.select_8 is not None)):
			self.select_8.send_value(79)
		elif ((num_of_tracks < pos2) and (hasattr(self, 'select_8')) and (self.select_8 is not None)):
			self.select_8.send_value(0)

	def track_select_1(self, value):
		if value > 0:
			if (hasattr(self, '_session')):
				move = self._session._track_offset + 1
			else:
				move = 1
			num_of_tracks = len(self.song().tracks)
			if num_of_tracks >= move:
				move = move - 1
				self.song().view.selected_track = self.song().tracks[move]

	def track_select_2(self, value):
		if value > 0:
			if (hasattr(self, '_session')):
				move = self._session._track_offset + 2
			else:
				move = 2
			num_of_tracks = len(self.song().tracks)
			if num_of_tracks >= move:
				move = move - 1
				self.song().view.selected_track = self.song().tracks[move]

	def track_select_3(self, value):
		if value > 0:
			if (hasattr(self, '_session')):
				move = self._session._track_offset + 3
			else:
				move = 3
			num_of_tracks = len(self.song().tracks)
			if num_of_tracks >= move:
				move = move - 1
				self.song().view.selected_track = self.song().tracks[move]

	def track_select_4(self, value):
		if value > 0:
			if (hasattr(self, '_session')):
				move = self._session._track_offset + 4
			else:
				move = 4
			num_of_tracks = len(self.song().tracks)
			if num_of_tracks >= move:
				move = move - 1
				self.song().view.selected_track = self.song().tracks[move]

	def track_select_5(self, value):
		if value > 0:
			if (hasattr(self, '_session')):
				move = self._session._track_offset + 5
			else:
				move = 5
			num_of_tracks = len(self.song().tracks)
			if num_of_tracks >= move:
				move = move - 1
				self.song().view.selected_track = self.song().tracks[move]

	def track_select_6(self, value):
		if value > 0:
			if (hasattr(self, '_session')):
				move = self._session._track_offset + 6
			else:
				move = 6
			num_of_tracks = len(self.song().tracks)
			if num_of_tracks >= move:
				move = move - 1
				self.song().view.selected_track = self.song().tracks[move]

	def track_select_7(self, value):
		if value > 0:
			if (hasattr(self, '_session')):
				move = self._session._track_offset + 7
			else:
				move = 7
			num_of_tracks = len(self.song().tracks)
			if num_of_tracks >= move:
				move = move - 1
				self.song().view.selected_track = self.song().tracks[move]

	def track_select_8(self, value):
		if value > 0:
			if (hasattr(self, '_session')):
				move = self._session._track_offset + 8
			else:
				move = 8
			num_of_tracks = len(self.song().tracks)
			if num_of_tracks >= move:
				move = move - 1
				self.song().view.selected_track = self.song().tracks[move]

	def _on_selected_track_changed(self):
		ControlSurface._on_selected_track_changed(self)
		self._display_reset_delay = 0
		value = "selected track changed"
		if (hasattr(self, '_set_track_select_led')):
			self._set_track_select_led()
		if (hasattr(self, '_reload_active_devices')):
			self._reload_active_devices(value)
		if (hasattr(self, 'update_all_ab_select_LEDs')):
			self.update_all_ab_select_LEDs(1)

	def _is_prev_device_on_or_off(self):
		self._device = self.song().view.selected_track.view.selected_device
		self._device_position = self.selected_device_idx()
		if (self._device is None) or (self._device_position == 0):
			on_off = "off"
		else:
			on_off = "on"
		return on_off

	def _is_nxt_device_on_or_off(self):
		self._selected_device = self.selected_device_idx() + 1  # add one as this starts from zero
		if (self._device is None) or (self._selected_device == len(self.song().view.selected_track.devices)):
			on_off = "off"
		else:
			on_off = "on"
		return on_off

	def _set_active_mode(self):
		global active_mode
		# activate mode
		if active_mode == "_mode4":
			self._mode4()
		elif active_mode == "_mode1":
			self._mode1()
		elif active_mode == "_mode2":
			self._mode2()
		elif active_mode == "_mode0":
			self._mode0()
		elif active_mode == "_mode3":
			self._mode3()
		if hasattr(self, '_set_track_select_led'):
			self._set_track_select_led()
		if hasattr(self, '_turn_on_device_select_leds'):
			self._turn_off_device_select_leds()
			self._turn_on_device_select_leds()
		if hasattr(self, '_all_prev_device_leds'):
			self._all_prev_device_leds()
		if hasattr(self, '_all_nxt_device_leds'):
			self._all_nxt_device_leds()
		if hasattr(self, 'update_all_ab_select_LEDs'):
			self.update_all_ab_select_LEDs(1)

	def _remove_active_mode(self):
		global active_mode
		# remove activate mode
		if active_mode == "_mode4":
			self._remove_mode4()
		elif active_mode == "_mode1":
			self._remove_mode1()
		elif active_mode == "_mode2":
			self._remove_mode2()
		elif active_mode == "_mode0":
			self._remove_mode0()
		elif active_mode == "_mode3":
			self._remove_mode3()

	def _activate_mode4(self,value):
		global active_mode
		global shift_previous_is_active
		if value > 0:
			shift_previous_is_active = "off"
			self._remove_active_mode()
			active_mode = "_mode4"
			self._set_active_mode()

	def _activate_mode1(self,value):
		global active_mode
		global shift_previous_is_active
		if value > 0:
			shift_previous_is_active = "off"
			self._remove_active_mode()
			active_mode = "_mode1"
			self._set_active_mode()

	def _activate_mode2(self,value):
		global active_mode
		global shift_previous_is_active
		if value > 0:
			shift_previous_is_active = "off"
			self._remove_active_mode()
			active_mode = "_mode2"
			self._set_active_mode()

	def _activate_mode0(self,value):
		global active_mode
		global shift_previous_is_active
		if value > 0:
			shift_previous_is_active = "off"
			self._remove_active_mode()
			active_mode = "_mode0"
			self._set_active_mode()

	def _activate_mode3(self,value):
		global active_mode
		global shift_previous_is_active
		if value > 0:
			shift_previous_is_active = "off"
			self._remove_active_mode()
			active_mode = "_mode3"
			self._set_active_mode()

	def _activate_shift_mode4(self,value):
		global active_mode
		global previous_shift_mode4
		global shift_previous_is_active
		if value > 0:
			shift_previous_is_active = "on"
			previous_shift_mode4 = active_mode
			self._remove_active_mode()
			active_mode = "_mode4"
			self._set_active_mode()
		elif shift_previous_is_active == "on":
			try:
				previous_shift_mode4
			except NameError:
				self.log_message("previous shift mode not defined yet")
			else:
				self._remove_active_mode()
				active_mode = previous_shift_mode4
				self._set_active_mode()

	def _activate_shift_mode1(self,value):
		global active_mode
		global previous_shift_mode1
		global shift_previous_is_active
		if value > 0:
			shift_previous_is_active = "on"
			previous_shift_mode1 = active_mode
			self._remove_active_mode()
			active_mode = "_mode1"
			self._set_active_mode()
		elif shift_previous_is_active == "on":
			try:
				previous_shift_mode1
			except NameError:
				self.log_message("previous shift mode not defined yet")
			else:
				self._remove_active_mode()
				active_mode = previous_shift_mode1
				self._set_active_mode()

	def _activate_shift_mode2(self,value):
		global active_mode
		global previous_shift_mode2
		global shift_previous_is_active
		if value > 0:
			shift_previous_is_active = "on"
			previous_shift_mode2 = active_mode
			self._remove_active_mode()
			active_mode = "_mode2"
			self._set_active_mode()
		elif shift_previous_is_active == "on":
			try:
				previous_shift_mode2
			except NameError:
				self.log_message("previous shift mode not defined yet")
			else:
				self._remove_active_mode()
				active_mode = previous_shift_mode2
				self._set_active_mode()

	def _activate_shift_mode0(self,value):
		global active_mode
		global previous_shift_mode0
		global shift_previous_is_active
		if value > 0:
			shift_previous_is_active = "on"
			previous_shift_mode0 = active_mode
			self._remove_active_mode()
			active_mode = "_mode0"
			self._set_active_mode()
		elif shift_previous_is_active == "on":
			try:
				previous_shift_mode0
			except NameError:
				self.log_message("previous shift mode not defined yet")
			else:
				self._remove_active_mode()
				active_mode = previous_shift_mode0
				self._set_active_mode()

	def _activate_shift_mode3(self,value):
		global active_mode
		global previous_shift_mode3
		global shift_previous_is_active
		if value > 0:
			shift_previous_is_active = "on"
			previous_shift_mode3 = active_mode
			self._remove_active_mode()
			active_mode = "_mode3"
			self._set_active_mode()
		elif shift_previous_is_active == "on":
			try:
				previous_shift_mode3
			except NameError:
				self.log_message("previous shift mode not defined yet")
			else:
				self._remove_active_mode()
				active_mode = previous_shift_mode3
				self._set_active_mode()

	def selected_device_idx(self):
		self._device = self.song().view.selected_track.view.selected_device
		return self.tuple_index(self.song().view.selected_track.devices, self._device)

	def selected_track_idx(self):
		self._track = self.song().view.selected_track
		self._track_num = self.tuple_index(self.song().tracks, self._track)
		self._track_num = self._track_num + 1
		return self._track_num

	def tuple_index(self, tuple, obj):
		for i in xrange(0, len(tuple)):
			if (tuple[i] == obj):
				return i
		return(False)

	def disconnect(self):
		super(Midi_Fighter_64, self).disconnect()
