from collections import deque
from random import randint, shuffle

DIS = [0, 0, 1, -1]
DJS = [1, -1, 0, 0]

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

  def make_wall(self, i, j):
    
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

      self._grid[y][x] = 1
      self._grid[y+DIS[angle]][x+DJS[angle]] = 1
      if (self._grid[y+DIS[angle]*2][x+DJS[angle]*2] == 1):
        break
      else:
        self._grid[y+DIS[angle]*2][x+DJS[angle]*2] = 1
        st.add((y+DIS[angle]*2, x+DJS[angle]*2))
        stack.append((y+DIS[angle]*2, x+DJS[angle]*2))

  def wall_init(self):
    start_cells = [(i, j) for i in range(self._ht) for j in range(self._wd) if (i%2 == 0 and j%2 == 0)]
    shuffle(start_cells)
    for i in range(self._ht):
      for j in range(self._wd):
        if (i==0 or i==self._ht-1): self._grid[i][j] = 1
        elif (j==0 or j==self._wd-1): self._grid[i][j] = 1
        else: self._grid[i][j] = 0

    for i, j in start_cells:
      if (self._grid[i][j] == 1): continue
      self.make_wall(i, j)



    


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