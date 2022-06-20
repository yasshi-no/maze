from collections import deque
import heapq
from random import randint, shuffle
import pyxel

REC_SIZE = 1
COLOR_PATH = 6
COLOR_WALL = 1
COLOR_EXPLORED = 10
COLOR_SHORTEST = 10
COLOR_HEAD = 8
NUM_PATH = 0
NUM_WALL = 1
NUM_EXPLORE = 2

START = (1, 1)
DIS = [0, 0, 1, -1]
DJS = [1, -1, 0, 0]
DRAW_INIT = 0
DRAW_EXPLORE = 1
FINISH_DFS = 1

def print_2darry(ary2d):
  ht = len(ary2d)
  for i in range(ht):
    print(*ary2d[i])


class Maze():
  def __init__(self, ht, wd):
    ht = max(5, ht)//2*2+1
    wd = max(5, wd)//2*2+1
    self._ht = ht
    self._wd = wd
    self._grid = [[-1 for _ in range(wd)] for _ in range(ht)]
    self._explored = set()
    self._deq = deque([])
    self._parents = [[-1 for _ in range(wd)] for _ in range(ht)]
    self._parents[1][1] = START
    self._costs = [[1<<30 for _ in range(wd)] for _ in range(ht)]

    
    
    self.DRAW_EXPLORE = DRAW_EXPLORE
    self._NUM_PATH = 0
    self._NUM_WALL = 1
    self._NUM_EXPLORE = 2
    self._NUM_HEAD = 3
    self._NUM_NEW = 4




  def explore_init(self):
    self._costs = [[1<<30 for _ in range(self._wd)] for _ in range(self._ht)]
    self._parents = [[-1 for _ in range(self._wd)] for _ in range(self._ht)]
    self._explored = set()
    self._deq = deque([])

  def wall_init(self):
    self.explore_init()
    for i in range(self._ht):
      for j in range(self._wd):
        if (i==0 or i==self._ht-1): self._grid[i][j] = 1
        elif (j==0 or j==self._wd-1): self._grid[i][j] = 1
        else: self._grid[i][j] = 0
    
  def mazed_by_wall(self):
    self.explore_init()
    start_cells = [(i, j) for i in range(self._ht) for j in range(self._wd) if (i%2 == 0 and j%2 == 0)]
    shuffle(start_cells)
    for i, j in start_cells:
      if (self._grid[i][j] == 1): continue
      st = set()
      stack = deque([])
      st.add((i, j))
      stack.append((i, j))

      while stack:
        y, x = stack[-1]
        can_make = []
        for i in range(4):
          if ((self._grid[y+DIS[i]][x+DJS[i]] == 0) and ((y+DIS[i]*2, x+DJS[i]*2) not in st)):
            can_make.append(i)
        if len(can_make) == 0:
          stack.pop()
          continue
        angle = can_make[randint(0, len(can_make)-1)]
        self._grid[y][x] = NUM_WALL
        self._grid[y+DIS[angle]][x+DJS[angle]] = NUM_WALL
        yield (y, x)
        yield (y+DIS[angle], x+DJS[angle])
        if (self._grid[y+DIS[angle]*2][x+DJS[angle]*2] == 1):
          break
        else:
          self._grid[y+DIS[angle]*2][x+DJS[angle]*2] = NUM_WALL
          stack.append((y+DIS[angle]*2, x+DJS[angle]*2))
          st.add((y+DIS[angle]*2, x+DJS[angle]*2))
          yield (y+DIS[angle]*2, x+DJS[angle]*2)

  def dfs(self):
    self.explore_init()
    self._deq.append(START)
    self._explored.add(START)
    while self._deq:
      i, j = self._deq.pop()
      if (DRAW_EXPLORE == 1): yield (i, j, self._NUM_HEAD)
      for di, dj in zip(DIS, DJS):
        if self._grid[i+di][j+dj] == NUM_WALL: continue
        if (i+di, j+dj) in self._explored: continue
        self._deq.append((i+di, j+dj))
        self._explored.add((i+di, j+dj))
        self._parents[i+di][j+dj] = (i, j)
        if (DRAW_EXPLORE == 1): yield (i+di, j+dj, self._NUM_EXPLORE)
    return

  def bfs(self):
    self.explore_init()
    self._deq.append(START)
    self._explored.add(START)
    self._costs[START[0]][START[1]] = 0
    while self._deq and not ((self._ht-2, self._wd-2) in self._explored and FINISH_DFS) :
      i, j = self._deq.popleft()
      if (DRAW_EXPLORE == 1): yield (i, j, self._NUM_HEAD)
      for di, dj in zip(DIS, DJS):
        if self._grid[i+di][j+dj] == NUM_WALL: continue
        if (i+di, j+dj) in self._explored: continue
        self._deq.append((i+di, j+dj))
        self._explored.add((i+di, j+dj))
        self._parents[i+di][j+dj] = (i, j)
        self._costs[i+di][j+dj] = self._costs[i][j] + 1
        if (DRAW_EXPLORE == 1): yield (i+di, j+dj, self._NUM_NEW)

  def expected_cost(self, i, j):
    return abs(self._ht-i) + abs(self._wd-j)

  def a_star(self):
    self.explore_init()
    h = []
    heapq.heapify(h)
    heapq.heappush(h, (self.expected_cost(*START), *START))
    self._explored.add(START)
    self._costs[START[0]][START[1]] = 0
    while heapq and not ((self._ht-2, self._wd-2) in self._explored and FINISH_DFS) :
      i, j = heapq.heappop(h)[1:]
      yield (i, j, self._NUM_HEAD)
      for di, dj in zip(DIS, DJS):
        if self._grid[i+di][j+dj] == NUM_WALL: continue
        if (i+di, j+dj) in self._explored: continue
        heapq.heappush(h, (self.expected_cost(i+di, j+dj), i+di, j+dj))
        self._explored.add((i+di, j+dj))
        self._parents[i+di][j+dj] = (i, j)
        self._costs[i+di][j+dj] = self._costs[i][j] + 1
        yield (i+di, j+dj, self._NUM_NEW)
      

    
    

  def collect_path(self):
    lst = []
    i, j = self._ht-2, self._wd-2
    lst.append((i, j))
    while not(i==1 and j==1):
      i, j = self._parents[i][j]
      lst.append((i, j))
    return lst

    

  # pyxelへの依存あり
  
  # def set_cell(self, i, j, x):
  #   self._grid[i][j] = x

  #   if DRAW_INIT == 0: return
  #   if   x == NUM_PATH: self.draw_cell(i, j, COLOR_PATH)
  #   elif x == NUM_WALL: self.draw_cell(i, j, COLOR_WALL)
  #   pyxel.flip()

  # def append_deq(self, i, j):
  #   self._deq.append((i, j))

    # self.draw_cell(i, j, COLOR_HEAD)
    # pyxel.flip()

  # @staticmethod
  # def draw_cell(i, j, color):
  #   pyxel.rect(j*REC_SIZE, i*REC_SIZE, REC_SIZE, REC_SIZE, color)

  # @staticmethod
  # def draw_ary2d(ary2d):
  #   for i in range(len(ary2d)):
  #     for j in range(len(ary2d[0])):
  #       if (ary2d[i][j] == NUM_WALL):
  #         pyxel.rect(j*REC_SIZE, i*REC_SIZE, REC_SIZE, REC_SIZE, COLOR_WALL)
  #       else:
  #         pyxel.rect(j*REC_SIZE, i*REC_SIZE, REC_SIZE, REC_SIZE, COLOR_PATH)
  #   pyxel.flip()


    


# def shuffle_2dary(lst):
#   ht = len(lst)
#   wd = len(lst[0])
#   size = ht*wd
#   for i in range(ht):
#     for j in range(wd):
#       idx = randint(0, size-1)
#       temp = lst[i][j]
#       lst[i][j] = lst[idx//wd][idx%wd]
#       lst[idx//wd][idx%wd] = temp
#   return

if __name__ == "__main__":
  maze = Maze(11, 11)
  maze.wall_init()
  print_2darry(maze._grid)