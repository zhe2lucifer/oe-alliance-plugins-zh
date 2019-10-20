# -*- coding: utf-8 -*-
from Screens.Screen import Screen
from Components.ConfigList import ConfigListScreen
from Components.config import config, ConfigSubsection, ConfigInteger, ConfigSelection, getConfigListEntry

modelist = {"1": _("Off"), "2": _("On"), "3": _("Auto")}

config.plugins.FanSetup = ConfigSubsection()
config.plugins.FanSetup.mode = ConfigSelection(choices = modelist, default = "3")

class FanSetupScreen(Screen, ConfigListScreen):
	skin = """
	<screen position="center,center" size="400,200" title="Fan setup">
		<widget name="config" position="10,10" size="350,150" />
		<ePixmap pixmap="skin_default/buttons/green.png" position="145,45" zPosition="0" size="140,40" alphatest="on" />
		<ePixmap pixmap="skin_default/buttons/red.png" position="5,45" zPosition="0" size="140,40" alphatest="on" />
		<widget name="ok" position="145,45" size="140,40" valign="center" halign="center" zPosition="1" font="Regular;20" transparent="1" backgroundColor="green" />
		<widget name="cancel" position="5,45" size="140,40" valign="center" halign="center" zPosition="1" font="Regular;20" transparent="1" backgroundColor="red" />
	</screen>"""

	def __init__(self, session):
		Screen.__init__(self, session)
		self.session = session
		self.skinName = "Setup"
		Screen.setTitle(self, _("Fan setup") + "...")

		from Components.ActionMap import ActionMap
		from Components.Sources.StaticText import StaticText

		self["key_red"] = StaticText(_("Cancel"))
		self["key_green"] = StaticText(_("Save"))

		self["actions"] = ActionMap(["OkCancelActions", "ColorActions", "CiSelectionActions"],
		{
			"ok": self.Go,
			"save": self.Go,
			"cancel": self.Cancel,
			"red": self.Cancel,
			"green": self.Go
		}, -2)

		self.list = []
		ConfigListScreen.__init__(self, self.list, session = self.session)

		mode = config.plugins.FanSetup.mode.value

		self.mode = ConfigSelection(choices = modelist, default = mode)
		self.list.append(getConfigListEntry(_("Fan mode"), self.mode))
		self["config"].list = self.list
		self["config"].l.setList(self.list)

	def keyLeft(self):
		ConfigListScreen.keyLeft(self)
		self.setPreviewSettings()

	def keyRight(self):
		ConfigListScreen.keyRight(self)
		self.setPreviewSettings()

	def setPreviewSettings(self):
		applySettings(int(self.mode.value))

	def Go(self):
		config.plugins.FanSetup.mode.value = self.mode.value
		config.plugins.FanSetup.save()
		setConfiguredSettings()
		self.close()

	def Cancel(self):
		setConfiguredSettings()
		self.close()

def applySettings(mode):
	setMode = ""
	if mode == 1:
		setMode = "1"

	elif mode == 2:
		setMode = "2"

	else:
		setMode = "3"
	
	try:
		file = open("/proc/stb/fp/fan", "w")
		file.write('%s' % setMode)
		file.close()
	except:
		return

def setConfiguredSettings():
	applySettings(int(config.plugins.FanSetup.mode.value))

def main(session, **kwargs):
	session.open(FanSetupScreen)

def startup(reason, **kwargs):
	setConfiguredSettings()

def FanMain(session, **kwargs):
	session.open(FanSetupScreen)

def FanSetup(menuid, **kwargs):
	if menuid == "system":
		return [(_("FAN Control"), FanMain, "fan_control", None)]
	else:
		return []
		
def Plugins(**kwargs):
	from os import path
	if path.exists("/proc/stb/fp/fan"):
		from Plugins.Plugin import PluginDescriptor
		return [PluginDescriptor(name = _("Fan Control"), description = _("switch Fan On/Off"), where = PluginDescriptor.WHERE_MENU, fnc = FanSetup),
					PluginDescriptor(name = "Fan Control", description = "", where = PluginDescriptor.WHERE_SESSIONSTART, fnc = startup)]
	return []
