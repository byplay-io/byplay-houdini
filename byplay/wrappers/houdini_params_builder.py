from byplay.config import Config
from byplay.houdini_interface import get_hou


class HoudiniParamsBuilder:
    @staticmethod
    def byplay_settings_parm_templates(node):
        hou = get_hou()
        return [
            hou.StringParmTemplate(
                "byplay_can_edit_paths",
                "Byplay can edit paths",
                1,
                default_value="",
                is_hidden=True
            ),
            hou.StringParmTemplate(
                "byplay_loaded_recording_id",
                "Loaded recording id",
                1,
                default_value="",
                is_hidden=True
            ),
            hou.StringParmTemplate(
                "byplay_recordings_dir",
                "Recordings directory",
                1,
                help="This is set in Byplay Desktop",
                conditionals={hou.parmCondType.DisableWhen: '{ byplay_can_edit_paths != "yes" }'}
            ),
            hou.MenuParmTemplate(
                "byplay_recording_id",
                "Recording id",
                menu_items=['[click refresh]'],
                join_with_next=True,
                help="These are downloaded & extracted recording ids from Byplay Desktop"
            ),
            hou.ButtonParmTemplate(
                "byplay_reload_recordings",
                "Refresh",
                script_callback="__import__('byplay').ui_callbacks.reload_recordings_list('{}')".format(node.path()),
                script_callback_language=hou.scriptLanguage.Python
            ),
            hou.ButtonParmTemplate(
                "byplay_load_recording",
                "Load",
                script_callback="__import__('byplay').ui_callbacks.load_recording_for_ui('{}')".format(node.path()),
                script_callback_language=hou.scriptLanguage.Python,
                conditionals={hou.parmCondType.DisableWhen: '{ byplay_recording_id == "[click refresh]" }'}
            ),
            hou.SeparatorParmTemplate("byplay_separator"),
            hou.StringParmTemplate(
                "recording_path",
                "Recording path",
                1,
                conditionals={hou.parmCondType.DisableWhen: '{ byplay_can_edit_paths != "yes" }'}
            ),
            hou.StringParmTemplate(
                "video_frames_path",
                "Video frames path",
                1,
                conditionals={hou.parmCondType.DisableWhen: '{ byplay_can_edit_paths != "yes" }'}
            ),
            hou.MenuParmTemplate(
                "exr_name",
                "Environment .exr",
                menu_items=['-'],
                conditionals={hou.parmCondType.DisableWhen: '{ byplay_loaded_recording_id == "" }'}
            ),
        ]

    @staticmethod
    def add_byplay_tab(node):
        hou = get_hou()
        parm_group = node.parmTemplateGroup()

        parm_folder = hou.FolderParmTemplate("byplay_settings", "Byplay")

        for tpl in HoudiniParamsBuilder.byplay_settings_parm_templates(node):
            parm_folder.addParmTemplate(tpl)

        if Config.is_dev():
            parm_folder.addParmTemplate(
                hou.ButtonParmTemplate(
                    "byplay_reload_modules",
                    "[[DEV]] reload Byplay python modules",
                    script_callback="__import__('byplay').ui_callbacks.reload_all_modules()",
                    script_callback_language=hou.scriptLanguage.Python
                )
            )

        parm_group.append(parm_folder)
        node.setParmTemplateGroup(parm_group)

    @staticmethod
    def set_byplay_recording_ids(node, ids):
        if len(ids) == 0:
            get_hou().ui.displayMessage(
                "There are no recordings. Did you try the app and downloaded something in Byplay Desktop?"
            )
            return
        selected_recording_id = node.parm("byplay_loaded_recording_id").evalAsString()
        HoudiniParamsBuilder.set_dropdown_values(
            node,
            "byplay_recording_id",
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
        HoudiniParamsBuilder.set_dropdown_values(node, "exr_name", environment_exr_names)

    @staticmethod
    def update_param(node, param_name, f):
        parm_group = node.parmTemplateGroup()
        tpl = parm_group.find(param_name)
        f(tpl)
        parm_group.replace(param_name, tpl)
        node.setParmTemplateGroup(parm_group)