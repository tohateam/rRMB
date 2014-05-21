# ##### BEGIN GPL LICENSE BLOCK #####
#
#  This program is free software; you can redistribute it and/or
#  modify it under the terms of the GNU General Public License
#  as published by the Free Software Foundation; either version 2
#  of the License, or (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software Foundation,
#  Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
#
# ##### END GPL LICENSE BLOCK #####

bl_info = {
    "name": "rRMB Menu",
    "author": "Paweł Łyczkowski",
    "version": (0.1),
    "blender": (2, 70, 0),
    "location": "View3D > RMB",
    "description": "Adds an RMB menu.",
    "warning": "",
    "wiki_url": "",
    "category": "3D View"}

import bpy
from bpy import *


class rRMB(bpy.types.Menu):
    bl_label = ""
    bl_idname = "VIEW3D_MT_rRMB"

    def draw(self, context):
        
        obj = context.active_object
        mode_string = context.mode
        edit_object = context.edit_object
        layout = self.layout
        
        #Menus in All Modes
        
        layout.operator("view3d.cursor3d", text="Place 3d Cursor", icon="CURSOR")
        
        layout.menu("VIEW3D_MT_rmovecursor")
        
        #Mode Specific Menus
        
        if edit_object:
            
            #Edit Mode
            
            layout.separator()
            
            layout.menu("VIEW3D_MT_edit_mesh_vertices")
            layout.menu("VIEW3D_MT_edit_mesh_edges")
            layout.menu("VIEW3D_MT_edit_mesh_faces")
            
            layout.menu("VIEW3D_MT_edit_mesh_specials")
            
            layout.separator()

            layout.menu("VIEW3D_MT_edit_mesh_showhide")
            
            layout.separator()
            
            layout.menu("VIEW3D_MT_edit_mesh_normals")
            layout.menu("VIEW3D_MT_edit_mesh_clean")
            
            layout.separator()
            
            layout.menu("VIEW3D_MT_uv_map", text="Unwrap")
            
        elif obj:
            
            #Object Mode
            
            if mode_string == 'OBJECT':
                
                layout.separator()
                
                layout.menu("VIEW3D_MT_robjecttransform")
                
                #layout.menu("VIEW3D_MT_transform_object")
                #layout.menu("VIEW3D_MT_mirror")
                #layout.menu("VIEW3D_MT_object_clear")
                #layout.menu("VIEW3D_MT_object_apply")
                #layout.menu("VIEW3D_MT_snap")

                layout.separator()

                layout.menu("VIEW3D_MT_object_showhide")
                layout.operator("object.move_to_layer", text="Move to Layer...")
                layout.menu("VIEW3D_MT_object_group")
                layout.menu("VIEW3D_MT_object_parent")
                
                layout.separator()

                #layout.menu("VIEW3D_MT_object_animation")

                #layout.separator()

                layout.operator("object.join")
                layout.operator("object.duplicate_move", text="Duplicate")
                layout.operator("object.duplicate_move_linked")
                layout.operator("object.delete", text="Delete...")
                
                layout.separator()
                
                layout.operator("object.proxy_make", text="Make Proxy...")
                layout.menu("VIEW3D_MT_make_links", text="Make Links...")
                layout.operator("object.make_dupli_face")
                layout.operator_menu_enum("object.make_local", "type", text="Make Local...")
                layout.menu("VIEW3D_MT_make_single_user")
                layout.operator_menu_enum("object.convert", "target")

                layout.separator()
                
                layout.menu("VIEW3D_MT_object_track")
                layout.menu("VIEW3D_MT_object_constraints")

                #layout.separator()

                #layout.menu("VIEW3D_MT_object_quick_effects")

                #layout.separator()

                #layout.menu("VIEW3D_MT_object_game")

                #layout.separator()
                
                
        
class VIEW3D_MT_robjecttransform(bpy.types.Menu):
    bl_context = "objectmode"
    bl_label = "Transform"

    def draw(self, context):
        
        layout = self.layout
        
        layout.operator("transform.translate", text="Grab/Move")
        layout.operator("transform.rotate", text="Rotate")
        layout.operator("transform.resize", text="Scale")
        
        layout.separator()
        
        layout.menu("VIEW3D_MT_mirror")
        layout.menu("VIEW3D_MT_object_clear")
        layout.menu("VIEW3D_MT_object_apply")
        layout.menu("VIEW3D_MT_snap")
        
        layout.separator()
        
        layout.operator_context = 'EXEC_AREA'
        layout.operator("object.origin_set", text="Geometry to Origin").type = 'GEOMETRY_ORIGIN'
        layout.operator("object.origin_set", text="Origin to Geometry").type = 'ORIGIN_GEOMETRY'
        layout.operator("object.origin_set", text="Origin to 3D Cursor").type = 'ORIGIN_CURSOR'
        
        layout.separator()
        
        layout.operator("transform.tosphere", text="To Sphere")
        layout.operator("transform.shear", text="Shear")
        layout.operator("transform.warp", text="Warp")
        layout.operator("transform.push_pull", text="Push/Pull")
        
        if context.edit_object and context.edit_object.type == 'ARMATURE':
            layout.operator("armature.align")
        else:
            layout.operator_context = 'EXEC_REGION_WIN'
            layout.operator("transform.transform", text="Align to Transform Orientation").mode = 'ALIGN' # XXX see alignmenu() in edit.c of b2.4x to get this working
        
        
            
class VIEW3D_MT_rmovecursor(bpy.types.Menu):
    bl_context = "objectmode"
    bl_label = "Move 3d Cursor"

    def draw(self, context):
        
        layout = self.layout
        
        layout.operator("view3d.snap_cursor_to_selected", text="To Selected")
        layout.operator("view3d.snap_cursor_to_center", text="To Center")
        layout.operator("view3d.snap_cursor_to_grid", text="To Grid")
        layout.operator("view3d.snap_cursor_to_active", text="To Active")
        
        
class VIEW3D_MT_robject(bpy.types.Menu):
    bl_context = "objectmode"
    bl_label = "Object"

    def draw(self, context):
        
        layout = self.layout
        
#------------------- REGISTER ------------------------------     

def register():
    bpy.utils.register_module(__name__)
    
    wm = bpy.context.window_manager
    kc = wm.keyconfigs.addon
    if kc:
        km = kc.keymaps.new(name='3D View', space_type='VIEW_3D')
        kmi = km.keymap_items.new('wm.call_menu', 'ACTIONMOUSE', 'PRESS')
        kmi.properties.name = "VIEW3D_MT_rRMB"
        kmi = km.keymap_items.new('view3d.cursor3d', 'ACTIONMOUSE', 'PRESS', alt=True)

def unregister():
    bpy.utils.unregister_(__name__)
    
    wm = bpy.context.window_manager
    kc = wm.keyconfigs.addon
    if kc:
        km = kc.keymaps['3D View']
        for kmi in km.keymap_items:
            if kmi.idname == 'wm.call_menu':
                if kmi.properties.name == "VIEW3D_MT_rRMB":
                    km.keymap_items.remove(kmi)
                    break

if __name__ == "__main__":
    register()

    #bpy.ops.wm.call_menu(name=rRMB.bl_idname)
    km = bpy.context.window_manager.keyconfigs.default
    



