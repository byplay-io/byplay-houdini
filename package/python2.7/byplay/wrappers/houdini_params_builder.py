from __future__ import absolute_import
from byplay.config import Config
from byplay.houdini_interface import get_hou


class HoudiniParamsBuilder(object):
    @staticmethod
    def byplay_settings_parm_templates(node):
        hou = get_hou()
        return [
            hou.StringParmTemplate(
                u"byplay_can_edit_paths",
                u"Byplay can edit paths",
                1,
                default_value=u"",
                is_hidden=True
            ),
            hou.StringParmTemplate(
                u"byplay_loaded_recording_id",
                u"Loaded recording id",
                1,
                default_value=u"",
                is_hidden=True
            ),
            hou.StringParmTemplate(
                u"byplay_recordings_dir",
                u"Recordings directory",
                1,
                help=u"This is set in Byplay Desktop",
                conditionals={hou.parmCondType.DisableWhen: u'{ byplay_can_edit_paths != "yes" }'}
            ),
            hou.MenuParmTemplate(
                u"byplay_recording_id",
                u"Recording id",
                menu_items=[u'[click refresh]'],
                join_with_next=True,
                help=u"These are downloaded & extracted recording ids from Byplay Desktop"
            ),
            hou.ButtonParmTemplate(
                u"byplay_reload_recordings",
                u"Refresh",
                script_callback=u"__import__('byplay').ui_callbacks.reload_recordings_list('{}')".format(node.path()),
                script_callback_language=hou.scriptLanguage.Python
            ),
            hou.ButtonParmTemplate(
                u"byplay_load_recording",
                u"Load",
                script_callback=u"__import__('byplay').ui_callbacks.load_recording_for_ui('{}')".format(node.path()),
                script_callback_language=hou.scriptLanguage.Python,
                conditionals={hou.parmCondType.DisableWhen: u'{ byplay_recording_id == "[click refresh]" }'}
            ),
            hou.SeparatorParmTemplate(u"byplay_separator"),
            hou.StringParmTemplate(
                u"recording_path",
                u"Recording path",
                1,
                conditionals={hou.parmCondType.DisableWhen: u'{ byplay_can_edit_paths != "yes" }'}
            ),
            hou.StringParmTemplate(
                u"video_frames_path",
                u"Video frames path",
                1,
                conditionals={hou.parmCondType.DisableWhen: u'{ byplay_can_edit_paths != "yes" }'}
            ),
            hou.MenuParmTemplate(
                u"exr_name",
                u"Environment .exr",
                menu_items=[u'-'],
                conditionals={hou.parmCondType.DisableWhen: u'{ byplay_loaded_recording_id == "" }'}
            ),
        ]

    @staticmethod
    def add_byplay_tab(node):
        hou = get_hou()
        parm_group = node.parmTemplateGroup()

        parm_folder = hou.FolderParmTemplate(u"byplay_settings", u"Byplay")

        for tpl in HoudiniParamsBuilder.byplay_settings_parm_templates(node):
            parm_folder.addParmTemplate(tpl)

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
            get_hou().ui.displayMessage(
                u"There are no recordings. Did you try the app and downloaded something in Byplay Desktop?"
            )
            return
        selected_recording_id = node.parm(u"byplay_loaded_recording_id").evalAsString()
        HoudiniParamsBuilder.set_dropdown_values(
            node,
            u"byplay_recording_id",
            ids,
            labels=None,
            current_value=selected_recording_id
        )

    @staticmethod
    def set_dropdown_values(node, param_name, values, labels=None, current_value=None):
        def set_items(tpl):
            tpl.setMenuItems(values)
            tpl.setMenuLabels(labels or values)
        HoudiniParamsBuilder.update_param(node, param_name, set_items)
        if current_value in values:
            node.parm(param_name).set(current_value)

    @staticmethod
    def set_exr_paths(node, environment_exr_names):
        if len(environment_exr_names) == 0:
            return
        HoudiniParamsBuilder.set_dropdown_values(node, u"exr_name", environment_exr_names)

    @staticmethod
    def update_param(node, param_name, f):
        parm_group = node.parmTemplateGroup()
        tpl = parm_group.find(param_name)
        f(tpl)
        parm_group.replace(param_name, tpl)
        node.setParmTemplateGroup(parm_group)