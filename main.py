import pygame as pg
import os
import collections
import random
import sys
from math import sqrt

pg.init()
screen = pg.display.set_mode((1920, 1040))
clock = pg.time.Clock()
screen.fill((255, 255, 255))
fps = 60
tile_size = 14

current_path = os.path.dirname(__file__)
OPEN = pg.image.load(os.path.join(current_path, 'open.png')).convert()
CLOSED = pg.image.load(os.path.join(current_path, "closed.png")).convert()  # images for tiles
FRESH = pg.image.load(os.path.join(current_path, "fresh.png")).convert()
INT = pg.image.load(os.path.join(current_path, "int.png")).convert()
SELECTED = pg.image.load(os.path.join(current_path, "selected.png")).convert()
WALL = pg.image.load(os.path.join(current_path, "wall.png")).convert()


class Block():
    def __init__(self, x, y, state):
        self.state = state
        self.x_cordinate = y
        self.y_cordinate = x
        self.neighbours = [(self.x_cordinate - 1, self.y_cordinate), (self.x_cordinate, self.y_cordinate - 1),
                           (self.x_cordinate + 1, self.y_cordinate), (self.x_cordinate, self.y_cordinate + 1)]
        self.cur_state(state)
        pg.display.flip()
        self.prev = (0, 0)
        self.dist = 0
        self.greedy_dist = 0
        self.vis = 0

    def cur_state(self, new_state):
        self.state = new_state
        if new_state == "open":
            screen.blit(OPEN, (self.y_cordinate * tile_size, self.x_cordinate * tile_size))
        if new_state == "closed":
            screen.blit(CLOSED, (self.y_cordinate * tile_size, self.x_cordinate * tile_size))
        if new_state == "fresh":
            screen.blit(FRESH, (self.y_cordinate * tile_size, self.x_cordinate * tile_size))
        if new_state == "intgoal":
            screen.blit(INT, (self.y_cordinate * tile_size, self.x_cordinate * tile_size))
        if new_state == "path":
            screen.blit(INT, (self.y_cordinate * tile_size, self.x_cordinate * tile_size))
        if new_state == "selected":
            screen.blit(SELECTED, (self.y_cordinate * tile_size, self.x_cordinate * tile_size))
        if new_state == "wall":
            screen.blit(WALL, (self.y_cordinate * tile_size, self.x_cordinate * tile_size))
        pg.display.flip()

    def set_state(self, new_state):
        self.state = new_state
        clock.tick(fps)
        self.cur_state(new_state)

    def set_greedy_dist(self, goal):
        self.greedy_dist = sqrt(((goal.x_cordinate - self.x_cordinate) * (goal.x_cordinate - self.x_cordinate)) + (
                    (goal.y_cordinate - self.y_cordinate) * (goal.y_cordinate - self.y_cordinate)))


def load_map(lines, x_start, y_start, x_end, y_end):
    map = []
    i = 0
    j = 0
    for line in lines:
        j = 0
        block_line = []
        for c in line:
            state = ""
            if c == 'X':
                state = "wall"
            if c == ' ':
                state = "fresh"
            if (j == x_start and i == y_start) or (j == x_end and i == y_end):
                state = "intgoal"
            block_line.append(Block(j, i, state))
            j += 1
        map.append(block_line)
        i += 1
    for block_line in map:
        for block in block_line:
            valid_neighbours = []
            for n in block.neighbours:
                if 0 < n[0] < i and 0 < n[1] < j and map[n[0]][n[1]].state != "wall":
                    valid_neighbours.append(n)
            block.neighbours = valid_neighbours
    return map


def bfs(map, start, goal):
    queue = collections.deque([[start]])
    open = {start}
    start.set_state("open")
    y_max = len(map)
    x_max = len(map[0])
    while queue:
        path = queue.popleft()
        cur = path[-1]
        cur.set_state("selected")
        if cur.x_cordinate == goal.x_cordinate and cur.y_cordinate == goal.y_cordinate:
            return goal
        for nei in cur.neighbours:
            if 0 <= nei[0] < y_max and 0 <= nei[1] < x_max and map[nei[0]][nei[1]] not in open:
                map[nei[0]][nei[1]].prev = (cur.x_cordinate, cur.y_cordinate)
                queue.append(path + [map[nei[0]][nei[1]]])
                map[nei[0]][nei[1]].set_state("open")
                open.add(map[nei[0]][nei[1]])
        cur.set_state("closed")


def dfs(map, start, goal):
    open = []
    closed = set()
    open.append(start)
    while open:
        cur = open.pop()
        cur.set_state("selected")
        if cur.x_cordinate == goal.x_cordinate and cur.y_cordinate == goal.y_cordinate:
            return goal
        for n in cur.neighbours:
            if map[n[0]][n[1]] not in open and map[n[0]][n[1]] not in closed:
                map[n[0]][n[1]].set_state("open")
                map[n[0]][n[1]].prev = (cur.x_cordinate, cur.y_cordinate)
                open.append(map[n[0]][n[1]])
        closed.add(cur)
        cur.set_state("closed")


from queue import PriorityQueue


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

    def pop(self):
        min = 0
        for i in range(len(self.queue)):
            if self.queue[i].dist < self.queue[min].dist:
                min = i
        item = self.queue[min]
        del self.queue[min]
        return item

    def new_dist(self, to_find, new_dist):
        self.queue[to_find].dist = new_dist

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

    def pop_random(self):
        i = random.randrange(len(self.queue))
        item = self.queue[i]
        del self.queue[i]
        return item


def dijkstra(map, start, goal):
    open = pqueue()
    open.insert(start)
    closed = set()
    while open:
        cur = open.pop()
        cur.set_state("selected")
        if cur.x_cordinate == goal.x_cordinate and cur.y_cordinate == goal.y_cordinate:
            return goal
        for n in cur.neighbours:
            distance = cur.dist + 1
            if (map[n[0]][n[1]] not in open.queue) or distance < map[n[0]][n[1]].dist:
                if map[n[0]][n[1]] not in open.queue and map[n[0]][n[1]] not in closed:
                    map[n[0]][n[1]].dist = distance
                    map[n[0]][n[1]].set_state("open")
                    map[n[0]][n[1]].prev = (cur.x_cordinate, cur.y_cordinate)
                    open.insert(map[n[0]][n[1]])
                elif map[n[0]][n[1]] not in closed:
                    map[n[0]][n[1]].dist = distance
                    map[n[0]][n[1]].prev = (cur.x_cordinate, cur.y_cordinate)
        cur.set_state("closed")
        closed.add(cur)


def greedy(map, start, goal):
    open = pqueue()
    start.set_greedy_dist(goal)
    open.insert(start)
    closed = set()
    while open:
        cur = open.pop_greedy()
        cur.set_state("selected")
        if cur.x_cordinate == goal.x_cordinate and cur.y_cordinate == goal.y_cordinate:
            return goal
        for n in cur.neighbours:
            if map[n[0]][n[1]] not in open.queue and map[n[0]][n[1]] not in closed:
                map[n[0]][n[1]].set_greedy_dist(goal)
                map[n[0]][n[1]].set_state("open")
                map[n[0]][n[1]].prev = (cur.x_cordinate, cur.y_cordinate)
                open.insert(map[n[0]][n[1]])
        cur.set_state("closed")
        closed.add(cur)


def a_star(map, start, goal):
    open = pqueue()
    start.set_greedy_dist(goal)
    open.insert(start)
    closed = set()
    while open:
        cur = open.pop_star()
        cur.set_state("selected")
        if cur.x_cordinate == goal.x_cordinate and cur.y_cordinate == goal.y_cordinate:
            return goal
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


def random_search(map, start, goal):
    open = pqueue()
    start.set_greedy_dist(goal)
    open.insert(start)
    closed = set()
    while open:
        cur = open.pop_random()
        cur.set_state("selected")
        if cur.x_cordinate == goal.x_cordinate and cur.y_cordinate == goal.y_cordinate:
            return goal
        for n in cur.neighbours:
            if map[n[0]][n[1]] not in open.queue and map[n[0]][n[1]] not in closed:
                map[n[0]][n[1]].set_greedy_dist(goal)
                map[n[0]][n[1]].set_state("open")
                map[n[0]][n[1]].prev = (cur.x_cordinate, cur.y_cordinate)
                open.insert(map[n[0]][n[1]])
        cur.set_state("closed")
        closed.add(cur)


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

    print("Select an algorithm to search a path:")
    print("press:")
    print("1 to Random Serach")
    print("2 to BFS")
    print("3 to DFS")
    print("4 to Dijkstra")
    print("5 to Greedy")
    print("* to A*")
    way = 0
    algo = input()
    if algo == "2":
        way = bfs(MAP, MAP[y_start][x_start], MAP[y_end][x_end])

    elif algo == "3":
        way = dfs(MAP, MAP[y_start][x_start], MAP[y_end][x_end])

    elif algo == "4":
        way = dijkstra(MAP, MAP[y_start][x_start], MAP[y_end][x_end])

    elif algo == "5":
        way = greedy(MAP, MAP[y_start][x_start], MAP[y_end][x_end])

    elif algo == "*":
        way = a_star(MAP, MAP[y_start][x_start], MAP[y_end][x_end])

    elif algo == "1":
        way = random_search(MAP, MAP[y_start][x_start], MAP[y_end][x_end])

    else:
        print("foo")
        exit(1)

    kek = (-1, -1)

    if way == 0:
        print("way doesn't exist")
        input()
        exit(0)

    while kek != (0, 0):
        way.set_state("path")
        way = MAP[way.prev[0]][way.prev[1]]
        kek = (way.x_cordinate, way.y_cordinate)

    input()
    pass
