import pygame as pg
import os
import random
import sys
import threading
from math import sqrt
import operator

pg.init()
screen = pg.display.set_mode((1920, 1040))
clock = pg.time.Clock()
screen.fill((255, 255, 255))
fps = 144
tile_size = 14

current_path = os.path.dirname(__file__)
GREEN = pg.image.load(os.path.join(current_path, './Assets/open.png')).convert()
PURPLE = pg.image.load(os.path.join(current_path, "./Assets/closed.png")).convert()  # images for tiles
FRESH = pg.image.load(os.path.join(current_path, "./Assets/fresh.png")).convert()
YELLOW = pg.image.load(os.path.join(current_path, "./Assets/int.png")).convert()
RED = pg.image.load(os.path.join(current_path, "./Assets/selected.png")).convert()
WALL = pg.image.load(os.path.join(current_path, "./Assets/wall.png")).convert()
TARGET = pg.image.load(os.path.join(current_path, "./Assets/point.png")).convert()
BASE = pg.image.load(os.path.join(current_path, "./Assets/base.png")).convert()
PINK = pg.image.load(os.path.join(current_path, "./Assets/pink.png")).convert()
BLUE = pg.image.load(os.path.join(current_path, "./Assets/blue.png")).convert()
CYAN = pg.image.load(os.path.join(current_path, "./Assets/cyan.png")).convert()


class Base():
    def __init__(self, pos):
        self.position = pos
        self.MODEL = BASE
        screen.blit(self.MODEL, ((self.position[1] * tile_size), self.position[0] * tile_size))
        pg.display.flip()
    def draw(self):
            screen.blit(self.MODEL, ((self.position[1] * tile_size), self.position[0] * tile_size))



class Target():
    def __init__(self, pos):
        self.position = pos
        self.MODEL = TARGET
        screen.blit(self.MODEL, ((self.position[1] * tile_size) + 4, self.position[0] * tile_size + 4))
        pg.display.flip()
    def draw(self):
        screen.blit(self.MODEL, ((self.position[1] * tile_size) + 4, self.position[0] * tile_size + 4))
        


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
    def __init__(self, num, pos, smap, home):
        super().__init__(None, name="robot" + str(num))
        self.num = num
        self.position = pos
        self.home = home
        self.MODEL = FRESH
        if num == 1:
            self.MODEL = RED
        if num == 2:    
            self.MODEL = GREEN
        if num == 3:
            self.MODEL = PURPLE
        if num == 4:
            self.MODEL = PINK
        if num == 5:
            self.MODEL = CYAN
        if num == 6:
            self.MODEL = BLUE
        screen.blit(self.MODEL, (self.position[1] * tile_size, self.position[0] * tile_size))
        pg.display.flip()
        self.state = 'init'
        self.simple_map = smap
        self.paths = []

    def a_star(self, goal):
        open = pqueue()
        start = self.simple_map[self.position[0]][self.position[1]]
        start.set_greedy_dist(goal)
        open.insert(start)
        closed = set()
        map = self.simple_map.copy()
        while not open.is_empty():
            cur = open.pop_star()
            cur.set_state("selected")
            if cur.x_cordinate == goal[0] and cur.y_cordinate == goal[1]:
                return goal, map
            for n in cur.neighbours:
                if map[n[0]][n[1]] not in closed:
                    distance = cur.dist + 1
                    map[n[0]][n[1]].set_greedy_dist(goal)
                    if map[n[0]][n[1]] not in open.queue or distance < map[n[0]][n[1]].dist:
                        map[n[0]][n[1]].prev = (cur.x_cordinate, cur.y_cordinate)
                        map[n[0]][n[1]].dist = distance
                        if map[n[0]][n[1]] not in open.queue:
                            map[n[0]][n[1]].set_state("open")
                            open.insert(map[n[0]][n[1]])
            cur.set_state("closed")
            closed.add(cur)
        return 0

    def path_reconst(self, way, map):
        kek = (-1, -1)

        if way == 0:
            print("way doesn't exist")
            return 0
        path = []
        while kek != self.position:
            path.append(way)
            way = map[way[0]][way[1]].prev
            kek = way
        path.append(self.position)
        path.reverse()
        return path

    
    def run(self):
        path = []
        while True:
            if self.state == "init":
                self.state = "searching"
                continue
            if self.state == "searching":
                threadLock.acquire()
                if(len(targets) < 1):
                    self.state = "shut_down"
                    threadLock.release()
                    continue
                for t in targets:
                    way = self.a_star(t.position)
                    path = self.path_reconst(way[0], way[1])
                    self.paths.append((len(path), t, path))
                target = min(self.paths, key=operator.itemgetter(0))
                print("hey guys! i going for ", target[1].position , " ", self.name)
                targets.remove(target[1])
                self.state = "going_target"
                threadLock.release()
                self.paths.clear()
                continue
            if self.state == "going_target":
                print(self.name)
                prev_b = 0
                for c in target[2]:
                    if(prev_b):
                        clock.tick(90)
                        pg.display.flip()
                        pos = (prev_b[1] * tile_size, prev_b[0]*tile_size)
                        offset = (c[1] - prev_b[1], c[0] - prev_b[0])
                        while (pos[1] / tile_size, pos[0] / tile_size) != c:
                            clock.tick(144)
                            screen.blit(FRESH, (c[1] * tile_size, c[0] * tile_size))
                            screen.blit(FRESH, (prev_b[1] * tile_size, prev_b[0] * tile_size))
                            pos = (pos[0]+offset[0], pos[1]+offset[1])
                            target[1].draw()
                            screen.blit(self.MODEL, (pos[0], pos[1]))
                            base.draw()
                            pg.display.flip()
                        self.position = c
                    prev_b = c
                self.state = "taking"
                print(self.position, "i m here " + self.name )
                continue
            if self.state == "taking":
                clock.tick(2)
                target[1].draw()
                pg.display.flip()
                self.state = "going_home"
                continue
            if self.state == "going_home":
                way = self.a_star(self.home.position)
                path = self.path_reconst(way[0], way[1])
                prev_b = 0
                for c in path:
                    if (prev_b):
                        clock.tick(90)
                        pg.display.flip()
                        pos = (prev_b[1] * tile_size, prev_b[0] * tile_size)
                        offset = (c[1] - prev_b[1], c[0] - prev_b[0])
                        while (pos[1] / tile_size, pos[0] / tile_size) != c:
                            clock.tick(144)
                            screen.blit(FRESH, (c[1] * tile_size, c[0] * tile_size))
                            screen.blit(FRESH, (prev_b[1] * tile_size, prev_b[0] * tile_size))
                            pos = (pos[0] + offset[0], pos[1] + offset[1])
                            screen.blit(self.MODEL, (pos[0], pos[1]))
                            screen.blit(target[1].MODEL, (pos[0]+4, pos[1]+4))
                            base.draw()
                            pg.display.flip()
                        self.position = c
                    prev_b = c
                self.state = "put"
                continue
            if self.state == "put":
                clock.tick(2)
                screen.blit(self.MODEL, (self.position[1] * tile_size, self.position[0]*tile_size))
                pg.display.flip()
                self.state = "searching"
                continue
            if self.state == "shut_down":
                threadLock.acquire()
                print("work_is_done ", self.name)
                threadLock.release()
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
        self.greedy_dist = sqrt(((goal[0] - self.x_cordinate) * (goal[0] - self.x_cordinate)) + (
                    (goal[1] - self.y_cordinate) * (goal[1] - self.y_cordinate)))



class Map_Block(Map_Element):

    def set_state(self, new_state):
        self.state = new_state
        if new_state == "fresh":
            screen.blit(FRESH, (self.y_cordinate * tile_size, self.x_cordinate * tile_size))
        if new_state == "intgoal":
            screen.blit(YELLOW, (self.y_cordinate * tile_size, self.x_cordinate * tile_size))
        if new_state == "path":
            screen.blit(YELLOW, (self.y_cordinate * tile_size, self.x_cordinate * tile_size))
        if new_state == "wall":
            screen.blit(WALL, (self.y_cordinate * tile_size, self.x_cordinate * tile_size))



def load_map(lines):
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

    b = input_lines[-3].split(" ")
    r = input_lines[-2].split(" ")
    t = input_lines[-1].split(" ")

    x_b = int(b[1].replace(",", ""))
    y_b = int(b[2])
    

    input_lines.pop()
    input_lines.pop()
    input_lines.pop()
    
    MAP = load_map(input_lines)
    threadLock = threading.Lock()
    i = 1
    targets = []
    while i < len(t):
        t_pos = t[i].replace(",", " ").replace(")", "").replace("(", "").split(" ")
        targets.append(Target((int(t_pos[0]), int(t_pos[1]))))
        i += 1
    base = Base((x_b, y_b))
    i = 1
    robots = []
    while i < len(r):
        r_pos = r[i].replace(",", " ").replace(")", "").replace("(", "").split(" ")
        robots.append(Robot(i, (int(r_pos[0]), int(r_pos[1])), MAP[1].copy(), base))
        i+=1
    input()
    for r in robots:
        r.start()
    
    pass
