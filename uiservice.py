
import os, bpy, re
from fnmatch import fnmatch
from .logservice import LogService
from .locationservice import LocationService
from mpfb import VERSION, get_preference

_LOG = LogService.get_logger("services.uiservice")


class _UiService():

    def __init__(self):
        _LOG.debug("Constructing ui service")
        self._state = dict()
        self.set_value("PROPERTYPREFIX", "MPFB_")

        # For beta version. Will change back for the next nightly build
        ui_prefix = "MPFB v%d.%d-b1" % (VERSION[0], VERSION[1])

        # ui_prefix = "MPFB v%d.%d-a%d" % (VERSION[0], VERSION[1], VERSION[2])

        label = get_preference("mpfb_shelf_label")
        _LOG.debug("Shelf label", label)
        if label and not str(label).strip() == "":
            ui_prefix = label

        multi = False  # get_preference("multi_panel")
        _LOG.debug("multi_panel", multi)

        self.set_value("UIPREFIX", ui_prefix)

        if multi:
            self.set_value("MODELCATEGORY", ui_prefix + " Model")
            self.set_value("IMPORTERCATEGORY", ui_prefix + " Import")
            self.set_value("CLOTHESCATEGORY", ui_prefix + " Clothes")
            self.set_value("TARGETSCATEGORY", ui_prefix + " Targets")
            self.set_value("MATERIALSCATEGORY", ui_prefix + " Materials")
            self.set_value("RIGCATEGORY", ui_prefix + " Rig & Pose")
            self.set_value("OPERATIONSCATEGORY", ui_prefix + " Operations")
            self.set_value("DEVELOPERCATEGORY", ui_prefix + " Developer")
            self.set_value("EXPORTCATEGORY", ui_prefix + " Export")
        else:
            for category in ["MODELCATEGORY", "IMPORTERCATEGORY", "CLOTHESCATEGORY", "TARGETSCATEGORY", "MATERIALSCATEGORY", "RIGCATEGORY", "OPERATIONSCATEGORY", "DEVELOPERCATEGORY", "EXPORTCATEGORY"]:
                self.set_value(category, ui_prefix)

    def get_value(self, name):
        _LOG.enter()
        if name in self._state:
            return self._state[name]
        return None

    def set_value(self, name, value):
        _LOG.enter()
        self._state[name] = value

    def _add_presets_to_list(self, presets, current_id):
        for file_name in os.listdir(LocationService.get_user_config()):
            _LOG.trace("file name", file_name)
            if fnmatch(file_name, "importer_presets.*.json"):
                name = str(file_name).replace("importer_presets.", "")
                name = str(name).replace(".json", "")
                _LOG.debug("Found presets file", name)
                if name != "default":
                    presets.append((name, name, "the " + name + " presets", current_id))
                    current_id = current_id + 1

    def rebuild_importer_presets_panel_list(self):
        _LOG.enter()
        _LOG.info("Rebuilding the list of available importer presets (for presets panel)")
        presets = [
            ("default", "default", "the default presets", 0)
        ]
        current_id = 1
        self._add_presets_to_list(presets, current_id)
        self.set_value("importer_presets_panel_list", presets)

    def get_importer_presets_panel_list(self):
        return self.get_value("importer_presets_panel_list")

    def rebuild_importer_panel_list(self):
        _LOG.enter()
        _LOG.info("Rebuilding the list of available importer presets (for importer panel)")
        presets = [
            ("FROM_UI", "Use ui settings", "use the settings currently set in the UI", 0),
            ("default", "Default", "the default presets", 1)
        ]
        current_id = 2
        self._add_presets_to_list(presets, current_id)
        self.set_value("importer_panel_list", presets)

    def get_importer_panel_list(self):
        return self.get_value("importer_panel_list")

    def _add_settings_to_list(self, settings, current_id):
        for file_name in os.listdir(LocationService.get_user_config()):
            _LOG.trace("file name", file_name)
            if fnmatch(file_name, "enhanced_settings.*.json"):
                name = str(file_name).replace("enhanced_settings.", "")
                name = str(name).replace(".json", "")
                _LOG.debug("Found settings file", name)
                if name != "default":
                    settings.append((name, name, "the " + name + " settings", current_id))
                    current_id = current_id + 1

    def rebuild_enhanced_settings_panel_list(self):
        _LOG.enter()
        _LOG.info("Rebuilding the list of available enhanced settings (for enhanced settings panel)")
        settings = [
            ("default", "default", "the default settings", 0)
        ]
        current_id = 1
        self._add_settings_to_list(settings, current_id)
        self.set_value("enhanced_settings_panel_list", settings)

    def get_enhanced_settings_panel_list(self):
        return self.get_value("enhanced_settings_panel_list")

    def rebuild_importer_enhanced_settings_panel_list(self):
        _LOG.enter()
        _LOG.info("Rebuilding the list of available enhanced material settings (for importer panel)")
        presets = [
            ("CHARACTER", "Match character name", "If available, use material settings with the same name as the imported character. Otherwise fall back to default settings.", 0),
            ("default", "Default", "the default presets. This will make fingernails smoother than the skin.", 1),
            ("RAW", "Do not modify", "use the settings currently set in the UI. This will for example leave skin pores on fingernails.", 2),

        ]
        current_id = 3
        self._add_settings_to_list(presets, current_id)
        self.set_value("importer_enhanced_settings_panel_list", presets)

    def get_importer_enhanced_settings_panel_list(self):
        return self.get_value("importer_enhanced_settings_panel_list")

    def _add_eye_settings_to_list(self, settings, current_id):
        for file_name in os.listdir(LocationService.get_user_config()):
            _LOG.trace("file name", file_name)
            if fnmatch(file_name, "eye_settings.*.json"):
                name = str(file_name).replace("eye_settings.", "")
                name = str(name).replace(".json", "")
                _LOG.debug("Found settings file", name)
                if name != "default":
                    settings.append((name, name, "the " + name + " settings", current_id))
                    current_id = current_id + 1

    def rebuild_eye_settings_panel_list(self):
        _LOG.enter()
        _LOG.info("Rebuilding the list of available eye settings (for eye settings panel)")
        settings = [
            ("default", "default", "the default settings", 0)
        ]
        current_id = 1
        self._add_eye_settings_to_list(settings, current_id)
        self.set_value("eye_settings_panel_list", settings)

    def get_eye_settings_panel_list(self):
        return self.get_value("eye_settings_panel_list")

    def rebuild_importer_eye_settings_panel_list(self):
        _LOG.enter()
        _LOG.info("Rebuilding the list of available eye material settings (for importer panel)")
        presets = [
            ("CHARACTER", "Match character name", "If available, use material settings with the same name as the imported character. Otherwise fall back to default settings.", 0),
            ("default", "Default", "the default presets. This will make fingernails smoother than the skin.", 1)
        ]
        current_id = 2
        self._add_eye_settings_to_list(presets, current_id)
        self.set_value("importer_eye_settings_panel_list", presets)

    def get_importer_eye_settings_panel_list(self):
        return self.get_value("importer_eye_settings_panel_list")

    def as_valid_identifier(self, raw_string):
       return re.sub(r'[^a-zA-Z0-9_]', "_", raw_string)


UiService = _UiService()  # pylint: disable=C0103
UiService.rebuild_importer_presets_panel_list()
UiService.rebuild_importer_panel_list()
