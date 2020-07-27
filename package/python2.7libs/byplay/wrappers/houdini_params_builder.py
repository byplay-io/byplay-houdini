# 
from __future__ import absolute_import
from byplay.config import Config
from byplay.houdini_interface import get_hou


class HoudiniParamsBuilder(object):
    @staticmethod
    def add_byplay_settings_tab(node):
        hou = get_hou()
        parm_group = node.parmTemplateGroup()
        parm_folder = hou.FolderParmTemplate(u"byplay_settings", u"Byplay settings")
        parm_folder.addParmTemplate(hou.StringParmTemplate(u"recording_path", u"Recording path", 1))
        parm_folder.addParmTemplate(hou.StringParmTemplate(u"video_frames_path", u"Video frames path", 1))
        parm_folder.addParmTemplate(
            hou.MenuParmTemplate(
                u"exr_name",
                u"Environment .exr",
                menu_items=[u'-']
            ),
        )
        parm_group.append(parm_folder)
        node.setParmTemplateGroup(parm_group)

    @staticmethod
    def add_byplay_recordings_tab(node):
        hou = get_hou()
        parm_group = node.parmTemplateGroup()
        parm_folder = hou.FolderParmTemplate(u"byplay_recordings", u"Byplay recordings")
        parm_folder.addParmTemplate(
            hou.StringParmTemplate(u"byplay_access_token", u"Byplay access token", 1)
        )
        parm_folder.addParmTemplate(
            hou.StringParmTemplate(
                u"byplay_recordings_dir",
                u"Recordings dir path",
                1,
                file_type=hou.fileType.Directory,
                string_type=hou.stringParmType.FileReference
            )
        )
        parm_folder.addParmTemplate(
            hou.MenuParmTemplate(
                u"byplay_recording_id",
                u"Recording id",
                menu_items=[u'[click refresh]'],
                join_with_next=True
            ),
        )
        parm_folder.addParmTemplate(
            hou.ButtonParmTemplate(
                u"byplay_reload_recordings",
                u"Refresh",
                script_callback=u"__import__('byplay').ui_callbacks.reload_recordings_list('{}')".format(node.path()),
                script_callback_language=hou.scriptLanguage.Python
            )
        )
        parm_folder.addParmTemplate(
            hou.ButtonParmTemplate(
                u"byplay_load_recording",
                u"Load",
                script_callback=u"__import__('byplay').ui_callbacks.load_recording_for_ui('{}')".format(node.path()),
                script_callback_language=hou.scriptLanguage.Python
            )
        )

        if Config.is_dev():
            parm_folder.addParmTemplate(
                hou.ButtonParmTemplate(
                    u"byplay_reload_modules",
                    u"[[DEV]] reload Byplay python modules",
                    script_callback=u"__import__('byplay').ui_callbacks.reload_all_modules()",
                    script_callback_language=hou.scriptLanguage.Python
                )
            )

        parm_group.append(parm_folder)
        node.setParmTemplateGroup(parm_group)

    @staticmethod
    def set_byplay_recording_ids(node, ids):
        if len(ids) == 0:
            get_hou().ui.displayMessage(u"There are no recordings. Did you try the app yet?")
            return
        HoudiniParamsBuilder.set_dropdown_values(node, u"byplay_recording_id", ids)

    @staticmethod
    def set_stored_values(node):
        access_token = Config.api_access_token()
        if access_token is not None:
            node.parm(u"byplay_access_token").set(access_token)
        byplay_recordings_dir = Config.recordings_dir()
        if byplay_recordings_dir is not None:
            node.parm(u"byplay_recordings_dir").set(byplay_recordings_dir)

    @staticmethod
    def set_dropdown_values(node, param_name, values, labels=None):
        parm_group = node.parmTemplateGroup()
        tpl = parm_group.find(param_name)
        tpl.setMenuItems(values)
        tpl.setMenuLabels(labels or values)
        parm_group.replace(param_name, tpl)
        node.setParmTemplateGroup(parm_group)

    @staticmethod
    def set_exr_paths(node, environment_exr_names):
        if len(environment_exr_names) == 0:
            return
        HoudiniParamsBuilder.set_dropdown_values(node, u"exr_name", environment_exr_names)
