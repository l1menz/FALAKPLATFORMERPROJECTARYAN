from os import walk
import pygame
from csv import reader

def import_csv_layout(path):
    terrain_map = []
    with open(path) as map:
        level = reader(map, delimiter = ',')
        for row in level:
            terrain_map.append(list(row))
        return terrain_map




#def import_folder(path): # Old code for test code
#    surface_list = []

#    for _,__,img_files in walk(path):
#        for image in img_files:
#            full_path = path + '/' + image
#           image_surf = pygame.image.load(full_path).convert_alpha()
#           surface_list.append(image_surf)

#    return surface_list