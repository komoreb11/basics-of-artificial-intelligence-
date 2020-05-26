import pygame as pg
import os
import random
import sys
import threading
from math import sqrt

pg.init()
screen = pg.display.set_mode((1920, 1040))
clock = pg.time.Clock()
screen.fill((255, 255, 255))
fps = 144
tile_size = 14

current_path = os.path.dirname(__file__)
OPEN = pg.image.load(os.path.join(current_path, './Assets/open.png')).convert()
CLOSED = pg.image.load(os.path.join(current_path, "./Assets/closed.png")).convert()  # images for tiles
FRESH = pg.image.load(os.path.join(current_path, "./Assets/fresh.png")).convert()
INT = pg.image.load(os.path.join(current_path, "./Assets/int.png")).convert()
SELECTED = pg.image.load(os.path.join(current_path, "./Assets/selected.png")).convert()
WALL = pg.image.load(os.path.join(current_path, "./Assets/wall.png")).convert()


class pqueue(object):
    def __init__(self):
        self.queue = []

        # for checking if the queue is empty

    def is_empty(self):
        return len(self.queue) == []

        # for inserting an element in the queue

    def insert(self, data):
        self.queue.append(data)

        # for popping an element based on Priority

    def pop_greedy(self):
        min = 0
        for i in range(len(self.queue)):
            if self.queue[i].greedy_dist < self.queue[min].greedy_dist:
                min = i
        item = self.queue[min]
        del self.queue[min]
        return item

    def pop_star(self):
        min = 0
        for i in range(len(self.queue)):
            if self.queue[i].greedy_dist + self.queue[i].dist < self.queue[min].greedy_dist + self.queue[min].dist:
                min = i
        item = self.queue[min]
        del self.queue[min]
        return item




class Robot(threading.Thread):
    def __init__(self, num, pos, smap, dest):
        super().__init__(None, name="robot" + str(num))
        self.num = num
        self.position = pos
        screen.blit(INT, (self.position[1] * tile_size, self.position[0] * tile_size))
        pg.display.flip()
        self.state = 'init'
        self.simple_map = smap
        self.destination = self.simple_map[dest[1]][dest[0]]

    def a_star(self):
        open = pqueue()
        start = self.simple_map[self.position[0]][self.position[1]]
        start.set_greedy_dist(self.destination)
        open.insert(start)
        closed = set()
        map = self.simple_map.copy()
        while not open.is_empty():
            cur = open.pop_star()
            cur.set_state("selected")
            if cur.x_cordinate == self.destination.x_cordinate and cur.y_cordinate == self.destination.y_cordinate:
                return self.destination, map
            for n in cur.neighbours:
                if map[n[0]][n[1]] not in closed:
                    distance = cur.dist + 1
                    map[n[0]][n[1]].set_greedy_dist(self.destination)
                    if map[n[0]][n[1]] not in open.queue or distance < map[n[0]][n[1]].dist:
                        map[n[0]][n[1]].prev = (cur.x_cordinate, cur.y_cordinate)
                        map[n[0]][n[1]].dist = distance
                        if map[n[0]][n[1]] not in open.queue:
                            map[n[0]][n[1]].set_state("open")
                            open.insert(map[n[0]][n[1]])
            cur.set_state("closed")
            closed.add(cur)

    def path_reconst(self, way, map):
        kek = (-1, -1)

        if way == 0:
            print("way doesn't exist")
            return 0
        path = []
        while kek != (0, 0):
            path.append((way.x_cordinate, way.y_cordinate))
            way = map[way.prev[0]][way.prev[1]]
            kek = (way.x_cordinate, way.y_cordinate)
        path.reverse()
        return path


    def run(self):
        path = []
        while True:
            if self.state == "init":
                print(self.name)
                self.state = "searching"
                continue
            if self.state == "searching":
                way = self.a_star()
                path = self.path_reconst(way[0], way[1])
                print(path)
                self.state = "going"
                continue
            if self.state == "going":
                print(self.name)
                for c in path:
                    clock.tick(12)
                    screen.blit(INT, (c[1] * tile_size, c[0] * tile_size))
                    pg.display.flip()
                self.state = "shut_down"
                continue
            if self.state == "shut_down":
                print(self.name + "shut_down")
                break

class Map_Element():
    def __init__(self, x, y, state):
        self.state = state
        self.x_cordinate = y
        self.y_cordinate = x
        self.neighbours = [(self.x_cordinate - 1, self.y_cordinate), (self.x_cordinate, self.y_cordinate - 1),
                           (self.x_cordinate + 1, self.y_cordinate), (self.x_cordinate, self.y_cordinate + 1)]
        self.set_state(state)

        self.prev = (0, 0)
        self.dist = 0
        self.greedy_dist = 0
        self.vis = 0

    def set_state(self, new_state):
        self.state = new_state

    def set_greedy_dist(self, goal):
        self.greedy_dist = sqrt(((goal.x_cordinate - self.x_cordinate) * (goal.x_cordinate - self.x_cordinate)) + (
                    (goal.y_cordinate - self.y_cordinate) * (goal.y_cordinate - self.y_cordinate)))



class Map_Block(Map_Element):

    def set_state(self, new_state):
        self.state = new_state
        if new_state == "fresh":
            screen.blit(FRESH, (self.y_cordinate * tile_size, self.x_cordinate * tile_size))
        if new_state == "intgoal":
            screen.blit(INT, (self.y_cordinate * tile_size, self.x_cordinate * tile_size))
        if new_state == "path":
            screen.blit(INT, (self.y_cordinate * tile_size, self.x_cordinate * tile_size))
        if new_state == "wall":
            screen.blit(WALL, (self.y_cordinate * tile_size, self.x_cordinate * tile_size))
        pg.display.flip()



def load_map(lines, x_start, y_start, x_end, y_end):
    map = []
    i = 0
    j = 0
    smap = []
    for line in lines:
        j = 0
        block_line = []
        sblock_line = []
        for c in line:
            state = ""
            if c == 'X':
                state = "wall"
            if c == ' ':
                state = "fresh"
            if (j == x_start and i == y_start) or (j == x_end and i == y_end):
                state = "intgoal"
            block_line.append(Map_Block(j, i, state))
            sblock_line.append(Map_Element(j, i, state))
            j += 1
        map.append(block_line)
        smap.append(sblock_line)
        i += 1
    i = 0
    j = 0
    for i in range(len(map)):
        for j in range(len(map[i])):
            valid_neighbours = []
            for n in map[i][j].neighbours:
                if 0 < n[0] < len(map) and 0 < n[1] < len(map[i]) and map[n[0]][n[1]].state != "wall":
                    valid_neighbours.append(n)
            map[i][j].neighbours = valid_neighbours
            smap[i][j].neighbours = valid_neighbours
    return map, smap


if __name__ == '__main__':
    input_lines = []
    if len(sys.argv) > 1:
        for line in open(sys.argv[1]):
            input_lines.append(line)
    else:
        while True:
            user_input = input()
            if user_input.strip() == "":  # empty line signals stop
                break
            input_lines.append(user_input)
            if user_input[0] == 'e':
                break

    st = input_lines[-2].split(" ")
    en = input_lines[-1].split(" ")

    x_start = int(st[1].replace(",", ""))
    y_start = int(st[2])

    x_end = int(en[1].replace(",", ""))
    y_end = int(en[2])

    input_lines.pop()
    input_lines.pop()

    MAP = load_map(input_lines, x_start, y_start, x_end, y_end)
    r1 = Robot(1, (5, 5), MAP[1].copy(), (17, 17))
    r2 = Robot(2, (3, 3), MAP[1].copy(), (3, 25))
    r3 = Robot(3, (43, 1), MAP[1].copy(), (21, 47))
    r1.start()
    r2.start()
    r3.start()
    r1.join()
    r2.join()
    r3.join()
    input()
    pass
