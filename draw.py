import copy
import pyxel
import maze_for_pyxel
from itertools import zip_longest

FPS = 1000000
MAZE_HT = 125
MAZE_WD = 125
HEIGHT = 125
WIDTH = 125
COLOR_PATH = 6
COLOR_WALL = 1
COLOR_EXPLORED = 10
COLOR_SHORTEST = 10
COLOR_HEAD = 8
COLOR_NEW = 9
REC_SIZE = 1
MODE_SOLVE = 0
MODE_WAIT = 1


class App:
    def __init__(self):
        pyxel.init(WIDTH, HEIGHT, fps=FPS)
        self.maze = maze_for_pyxel.Maze(MAZE_HT, MAZE_WD)
        maze_for_pyxel.DRAW_INIT = 1
        maze_for_pyxel.DRAW_EXPLORE = 1
        pyxel.run(self.update, self.draw)

    def update(self):
        return

    def to_color(self, num):
        if num == self.maze._NUM_EXPLORE:
            return COLOR_EXPLORED
        elif num == self.maze._NUM_HEAD:
            return COLOR_HEAD
        elif num == self.maze._NUM_NEW:
            return COLOR_NEW

    def draw_cell(self, i, j, color):
        pyxel.rect(j*REC_SIZE, i*REC_SIZE, REC_SIZE, REC_SIZE, color)

    def draw_mazed(self):
        for tpl in self.maze.mazed_by_wall():
            self.draw_cell(*tpl, COLOR_WALL)
            pyxel.flip()

    def draw_maze(self):
        for i in range(self.maze._ht):
            for j in range(self.maze._wd):
                if (self.maze._grid[i][j] == self.maze._NUM_WALL):
                    pyxel.rect(j*REC_SIZE, i*REC_SIZE,
                               REC_SIZE, REC_SIZE, COLOR_WALL)
                else:
                    pyxel.rect(j*REC_SIZE, i*REC_SIZE,
                               REC_SIZE, REC_SIZE, COLOR_PATH)
        pyxel.flip()

    def draw_dfs(self):
        bi, bj = -1, -1
        for tpl in self.maze.bfs():
            self.draw_cell(*tpl[:2], self.to_color(tpl[2]))
            if (tpl[2] == self.maze._NUM_HEAD):
                self.draw_cell(bi, bj, COLOR_EXPLORED)
                bi, bj = tpl[:2]
            pyxel.flip()

    def draw_bfs(self):
        st = set()
        lst = []
        for tpl in self.maze.bfs():
            if tpl[:2] in st:
                for t in st:
                    self.draw_cell(*t, COLOR_HEAD)
                for t in lst:
                    self.draw_cell(*t, COLOR_EXPLORED)
                st = set()
            if tpl[2] == self.maze._NUM_NEW:
                st.add(tpl[:2])
            else:
                lst.append(tpl[:2])
            if tpl[2] == self.maze._NUM_NEW:
                self.draw_cell(*tpl[:2], self.to_color(tpl[2]))
                pyxel.flip()

    def draw_a_star(self):
        for tpl in self.maze.a_star():
            if tpl[2] == self.maze._NUM_NEW:
                self.draw_cell(*tpl[:2], COLOR_HEAD)
            else:
                self.draw_cell(*tpl[:2], COLOR_EXPLORED)
                pyxel.flip()

    def draw_comp(self):
        self.maze.wall_init()
        for _ in self.maze.mazed_by_wall():
            continue
        maze_c = copy.deepcopy(self.maze)
        for i in range(maze_c._wd):
            for j in range(maze_c._ht):
                if maze_c._grid[i][j] == maze_c._NUM_WALL:
                    self.draw_cell(i, j+self.maze._wd, COLOR_WALL)
                else:
                    self.draw_cell(i, j+self.maze._wd, COLOR_PATH)
        for i in range(maze_c._wd):
            for j in range(maze_c._ht):
                if maze_c._grid[i][j] == maze_c._NUM_WALL:
                    self.draw_cell(i, j, COLOR_WALL)
                else:
                    self.draw_cell(i, j, COLOR_PATH)
        pyxel.flip()

        for tpl1, tpl2 in zip_longest(self.maze.bfs(), maze_c.a_star()):
            if tpl1 != None:
                if tpl1[2] == self.maze._NUM_NEW:
                    self.draw_cell(tpl1[0], tpl1[1]+self.maze._wd, COLOR_HEAD)
                else:
                    self.draw_cell(tpl1[0], tpl1[1] +
                                   self.maze._wd, COLOR_EXPLORED)
                    pyxel.flip()
            if tpl2 != None:
                if tpl2[2] == self.maze._NUM_NEW:
                    self.draw_cell(*tpl2[:2], COLOR_HEAD)
                else:
                    self.draw_cell(*tpl2[:2], COLOR_EXPLORED)
                    pyxel.flip()

        for i in range(maze_c._wd):
            for j in range(maze_c._ht):
                if maze_c._grid[i][j] == maze_c._NUM_WALL:
                    self.draw_cell(i, j+self.maze._wd, COLOR_WALL)
                else:
                    self.draw_cell(i, j+self.maze._wd, COLOR_PATH)
        for i in range(maze_c._wd):
            for j in range(maze_c._ht):
                if maze_c._grid[i][j] == maze_c._NUM_WALL:
                    self.draw_cell(i, j, COLOR_WALL)
                else:
                    self.draw_cell(i, j, COLOR_PATH)

        pyxel.flip()
        for tpl1, tpl2 in zip_longest(reversed(self.maze.collect_path()), reversed(maze_c.collect_path())):
            self.draw_cell(tpl1[0], tpl1[1]+self.maze._wd, COLOR_EXPLORED)
            self.draw_cell(*tpl2[:2], COLOR_EXPLORED)
            pyxel.flip()
            if tpl1 == None or tpl2 == None:
                print("???")

    def draw(self):
        # 迷路の初期化
        self.maze.wall_init()
        self.draw_maze()

        # 迷路構成の描画
        self.draw_mazed()

        #　完成した迷路のみを描画
        # for _ in self.maze.mazed_by_wall(): continue
        # self.draw_maze()

        # self.draw_bfs()
        self.draw_a_star()

        # self.draw_comp()

        # 探索でゴールにたどり着いたパスの描画
        self.draw_maze()
        lst = self.maze.collect_path()
        lst.reverse()
        for t in lst:
            print(t)
            self.draw_cell(*t, COLOR_EXPLORED)
            pyxel.flip()

        import time
        time.sleep(1)


App()
