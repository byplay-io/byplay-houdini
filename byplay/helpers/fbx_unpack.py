from byplay import get_hou


class FBXUnpack:
    def __init__(self, fbx_path):
        self.fbx_path = fbx_path

    def unpack(self, rename_map={}):
        hou = get_hou()
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
            existing = hou.node("/obj/{}".format(ch.name()))
            if existing is not None:
                existing.destroy()

        moved = hou.moveNodesTo(subn.children(), hou.node("/obj"))
        subn.destroy()
        return moved
