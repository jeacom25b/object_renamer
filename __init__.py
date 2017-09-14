import bpy


bl_info = {
    "name": "Object Renamer",
    "description": "",
    "author": "jean Da Costa Machado",
    "version": (0, 0, 1),
    "blender": (2, 78, 0),
    "location": "View3D",
    "warning": "This addon is still in development.",
    "wiki_url": "",
    "category": "Object"}


class RenamePanel (bpy.types.Panel):
    bl_idname = "rennamer.panel"
    bl_label = "rename"
    bl_space_type = "VIEW_3D"
    bl_region_type = "TOOLS"
    bl_category = "Rename"
    
    def draw(self, context):
        layout = self.layout
        layout.label("rename")
        layout.operator("rennamer.get_name")
        layout.prop(context.scene, "renname", "new name")
        layout.prop(context.scene, "repname", "find")
        layout.operator("rennamer.rename")
        layout.operator("rennamer.replace")


class GetName(bpy.types.Operator):
    bl_idname = "rennamer.get_name"
    bl_label = "Get Name"
    bl_description = ""
    bl_options = {"REGISTER", "UNDO"}
    
    @classmethod
    def poll(cls, context):
        return context.active_object
    
    def execute(self, context):
        
        if context.active_bone:
            context.scene.renname = context.active_bone.name
        elif context.active_pose_bone:
            context.scene.renname = context.active_pose_bone.name
        elif context.active_object:
            context.scene.renname = context.active_object.name
        
        return {"FINISHED"}



class ReplaceNames(bpy.types.Operator):
    bl_idname = "rennamer.replace"
    bl_label = "Find and Replace"
    bl_description = ""
    bl_options = {"REGISTER", "UNDO"}
    
    @classmethod
    def poll(cls, context):
        return True
    
    def execute(self, context):
        
        if context.selected_bones:
            for b in context.selected_bones:
                b.name = b.name.replace(context.scene.repname, context.scene.renname)
        elif context.selected_pose_bones:
            for b in context.selected_pose_bones:
                b.name = b.name.replace(context.scene.repname, context.scene.renname)
        elif context.active_object:
            for o in context.selected_objects:
                o.name = o.name.replace(context.scene.repname, context.scene.renname)
        
        return {"FINISHED"}

class RenameNames(bpy.types.Operator):
    bl_idname = "rennamer.rename"
    bl_label = "rename objects"
    bl_description = ""
    bl_options = {"REGISTER", "UNDO"}
    
    x_mirror = bpy.props.BoolProperty(name = "X mirror", description = "Use L\R notation (onlly for bones)", default = True)
    middle_error = bpy.props.FloatProperty(name = "Middle threshold", default = 0.001)
    
    @classmethod
    def poll(cls, context):
        if context.selected_objects:
            return True
    
    def execute(self, context):
        
        if context.selected_bones:
            for b in context.selected_bones:
                pos = b.head + b.tail
                sufix = ""
                
                if pos.x > self.middle_error:
                    sufix = ".L"
                if pos.x < -self.middle_error:
                    sufix = ".R"
                b.name = context.scene.renname + sufix
        elif context.selected_pose_bones:
            for b in context.selected_pose_bones:
                pos = b.head + b.tail

                sufix = ""
                if pos.x > self.middle_error:
                    sufix = ".L"
                if pos.x < -self.middle_error:
                    sufix = ".R"
                b.name = context.scene.renname + sufix
        elif context.active_object:
            for o in context.selected_objects:
                o.name = context.scene.renname
        
        return {"FINISHED"}


def register():
    bpy.utils.register_module(__name__)
    bpy.types.Scene.renname = bpy.props.StringProperty(name = "name", description = "name")
    bpy.types.Scene.repname = bpy.props.StringProperty(name = "find", description = "find")


def unregister():
    bpy.utils.unregister_module(__name__)
    del bpy.types.Scene.renname
    del bpy.types.Scene.repname

if __name__ == "__main__":
    register()
