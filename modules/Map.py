from ursina import *
from helpers.CustomLib import *
from data.WallPositionData import listWallPosition
from data.TreePositionData import listTreePosition
from data.HousePositionData import listHousePosition


class Map:

    def __init__(self):
        self.step = 5
        Entity(model='cube', position=(0, 0, 0), collider='box',
               scale=(3500, 1, 3500), texture='brick', color=color.gray)

        for pos in listWallPosition:
            createWall(pos['x'], pos['z'], pos['width'],
                       pos['height'], pos['color'], pos['corner'])
        for tree in listTreePosition:
            createTree(tree['x'], tree['z'])
        for house in listHousePosition:
            createHouse(house['x'], house['z'], house['corner'])
