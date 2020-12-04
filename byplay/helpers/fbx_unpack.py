from byplay import get_hou


class FBXUnpack:
    def __init__(self, fbx_path):
        self.fbx_path = fbx_path

    def unpack(self, rename_map={}, parent_node=None, only_in_map=False):
        hou = get_hou()
        if parent_node is None:
            parent_node = hou.node("/obj")
        subn, _ = hou.hipFile.importFBX(
            self.fbx_path,
            convert_into_y_up_coordinate_system=True,
            override_framerate=True,
            framerate=30
        )
        for ch in subn.children():
            name = ch.name()
            if name in rename_map:
                ch.setName(rename_map[name])
            else:
                if only_in_map:
                    ch.destroy()
                    continue
            existing = parent_node.node(ch.name())
            if existing is not None:
                existing.destroy()

        moved = hou.moveNodesTo(subn.children(), parent_node)
        subn.destroy()
        return moved
