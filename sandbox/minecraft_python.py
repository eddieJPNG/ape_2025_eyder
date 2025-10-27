# ...existing code...
from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController

app = Ursina()

SIZE = 10        # raio do piso (cria um grid SIZE x SIZE)
BLOCK_COLOR = color.rgb(120,200,100)

voxels = {}

# cria um piso simples de cubos
for x in range(-SIZE//2, SIZE//2):
    for z in range(-SIZE//2, SIZE//2):
        e = Entity(model='cube', color=BLOCK_COLOR, position=(x, 0, z), collider='box', scale=1)
        voxels[(x, 0, z)] = e

# jogador
player = FirstPersonController(y=2)
player.cursor.visible = False
player.speed = 6

# mira simples
reticle = Entity(parent=camera.ui, model='quad', scale=.01, color=color.white)

def input(key):
    # clique esquerdo: quebrar; clique direito: colocar bloco na face atingida
    if key in ('left mouse down', 'right mouse down'):
        hit = raycast(camera.world_position, camera.forward, distance=6, ignore=(player,))
        if not hit.hit:
            return

        ent = hit.entity
        # coordenadas inteiras da grade
        gx, gy, gz = round(ent.x), round(ent.y), round(ent.z)

        if key == 'left mouse down':
            # destruir bloco
            if (gx, gy, gz) in voxels:
                destroy(voxels.pop((gx, gy, gz)))
        else:
            # colocar bloco na face atingida
            nx, ny, nz = hit.world_normal
            ox, oy, oz = int(round(nx)), int(round(ny)), int(round(nz))
            place = (gx + ox, gy + oy, gz + oz)
            if place not in voxels:
                e = Entity(model='cube', color=color.rgb(200,180,140), position=place, collider='box', scale=1)
                voxels[place] = e

print("Script Ursina minimal iniciado. WASD + mouse. LMB para quebrar, RMB para colocar.")
app.run()
# ...existing code...