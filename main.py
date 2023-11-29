import random
import curses
from curses import wrapper
import time

#create playing field
size = 20
obstracle_ratio = 0.3


class Graph:
    def __init__(self, size, obstracle_ratio):
        self.size = size

        # create adjacancy matrix
        self.graph = [[0]*size*size for i in range(size*size)]
        for i in range(0,size*size):
            for j in range(0,size*size):
                if (j-1 == i and j%size!=0) or (j-size == i):
                    self.graph[i][j] = 1
                if (i-1 == j and i%size!=0) or (i-size == j):
                    self.graph[i][j] = 1
        
        #set obstracles
        self.obstracles = random.sample(range(0,size*size),int(size*size*obstracle_ratio))
        for i in self.obstracles:
            for j in range(0,size*size):
                self.graph[i][j] = 0
                self.graph[j][i] = 0
        
        #choos start and goal
        self.start = self.obstracles[0]
        self.goal = self.obstracles[0]
        while self.start in self.obstracles:
            self.start = random.sample(range(size*size), 1)[0]
        while self.goal in self.obstracles or self.goal == self.start:
            self.goal = random.sample(range(size*size), 1)[0]
    
    # update playing field
    def update_field(self, win, visited=[], path=[]):
        
        #build field
        field = [[0]*self.size for i in range(self.size)]
        for i, row in enumerate(self.graph):
            if all(v == 0 for v in row):
                field[int(i/self.size)][i%self.size] = 1
        for n in visited:
            field[int(n/self.size)][n%self.size] = 5    
        field[int(self.start/self.size)][self.start%self.size] = 7
        for n in path:
            field[int(n/self.size)][n%self.size] = 6    
        field[int(self.start/self.size)][self.start%self.size] = 7
        if self.goal not in visited:
            field[int(self.goal/self.size)][self.goal%self.size] = 8
        else:
            field[int(self.goal/self.size)][self.goal%self.size] = 9
 
        #visualize field
        for r,row in enumerate(field):
            for c, character in enumerate(row):
                if character == 7:
                    win.addch(c,r, 'o', curses.color_pair(1)|curses.A_BOLD)
                elif character == 8:
                    win.addch(c,r, '!', curses.color_pair(2)|curses.A_BOLD)
                elif character == 9:
                    win.addch(c,r, '!', curses.color_pair(5)|curses.A_BOLD)
                elif character == 6:
                    win.addch(c,r, ' ', curses.color_pair(6))
                elif character == 1:
                    win.addch(c,r, ' ', curses.color_pair(3))
                elif character == 5:
                    win.addch(c,r, ' ', curses.color_pair(5))
                else:
                    win.addch(c,r, ' ', curses.color_pair(4))
        win.refresh()
    
    #update multible fields
    def update_fields(self,wins):
        for win in wins:
            self.update_field(win)
    
    #update header element
    def update_header(self, win, count, error=False):
        win.addstr(1,14,str(count))
        if error == True:
            win.addstr(2,4,'Not Solvable',curses.color_pair(2))
        win.refresh()

    #greedy backtrack shortest way
    def find_shortest_path(self, paths):
        shortest_path = [self.goal]
        while shortest_path[-1] != self.start:
            for start, end in paths:
                if end == shortest_path[-1]:
                    shortest_path.append(start)
                    break
        return shortest_path



    #Breth first Search
    def bfs(self, win, header):
        visited = [self.start]
        queue = [self.start]
        paths = []
        while self.goal not in visited:

            #find naighbors
            s = queue.pop(0)
            neighbors = [i for i, v in enumerate(self.graph[s]) if v == 1]

            #add neighbors to path and queue
            for n in neighbors:
                paths.append((s,n))
                if n not in visited:
                    visited.append(n)
                    queue.append(n)

                    #update window
                    self.update_field(win,visited)
                    self.update_header(header,len(visited))

                    #break if goal is reached
                    if n == self.goal:
                        break

                    #timeout for visualization
                    time.sleep(0.01)
            
            #Handle Error
            if queue == []:
                self.update_header(header,len(visited),True)
                break
        
        #Display shortest path
        if self.goal in visited:
            self.update_field(win, visited, self.find_shortest_path(paths))


    #Depth First Search
    def dfs(self, win, header):
        visited = [self.start]
        stack = [self.start]
        paths = []

        while self.goal not in visited:

            # pop top node
            s = stack.pop(0)

            #find neighbors of top node
            neighbors = [i for i, v in enumerate(self.graph[s]) if v == 1]


            #add neighbors to stack
            for n in neighbors:
                if (s,n) not in paths:
                    paths.append((s,n))
                if n in visited:
                    continue
                if n in stack:
                    stack.remove(n)
                stack.insert(0,n)

            #break loop if stack is empty (error) and update header
            if stack == []:
                self.update_header(header,len(visited),True)
                break

            #visite top node
            visited.append(stack[0])

            #update window
            self.update_field(win, visited)
            self.update_header(header,len(visited))

            #timeout for visualization
            time.sleep(0.01)
        
        #Display shortest path
        if self.goal in visited:
            self.update_field(win, visited, self.find_shortest_path(paths))
    
    #A* Algorithm

    # utility function for calculation L1 Norm
    def calc_distance(self, node):
        start =[int(self.start/self.size), self.start%self.size]
        goal = [int(self.goal/self.size), self.goal%self.size]
        n = [int(node/self.size), node%self.size]
        n_goal = sum([abs(a - b) for a, b in zip(goal, n)])
        n_start = sum([abs(a - b) for a, b in zip(start, n)])
        n_total = n_start + n_goal
        return  [n_total, n_goal]

    # A* Search algorithm
    def a_star(self, win, header):
        visited = [self.start]
        neighbors = []
        paths = []

        while self.goal not in visited:

            #find neignor nodes of last visited and add them to neighbors list
            neighbor_nodes = [i for i, v in enumerate(self.graph[visited[-1]]) if v == 1]
            for node in neighbor_nodes:
                if node not in [n[0] for n in neighbors] and node not in visited:
                    neighbors.append([node] + self.calc_distance(node))
                if (visited[-1],node) not in paths:
                    paths.append((visited[-1],node))

            #choose node with lowest score
            index = 0
            for i, node in enumerate(neighbors):
                n = neighbors[index]
                if node[1]<n[1] or (node[1]==n[1] and node[2]<n[2]):
                    index = i
            if neighbors == []:
                self.update_header(header, len(visited), True)
                break

            # delete chosen node form neighbors and append to visited
            n = neighbors.pop(index)
            visited.append(n[0])

            #update window
            self.update_field(win, visited)
            self.update_header(header,len(visited))

            #timeout for visualization
            time.sleep(0.01)

        #Display shortest path
        if self.goal in visited:
            self.update_field(win, visited, self.find_shortest_path(paths))






            

g = Graph(size,obstracle_ratio)


#Visualization with curses

# crate visualisation environment
def main(stdscr):
    # Clear screen
    stdscr.clear()

    #colors
    curses.init_pair(1, curses.COLOR_BLUE, curses.COLOR_YELLOW)
    curses. init_pair(2, curses.COLOR_RED, curses.COLOR_WHITE)
    curses.init_pair(3, curses.COLOR_BLACK, curses.COLOR_BLACK)
    curses.init_pair(4, curses.COLOR_WHITE, curses.COLOR_WHITE)
    curses.init_pair(5, curses.COLOR_RED, curses.COLOR_YELLOW)
    curses.init_pair(6, curses.COLOR_RED, curses.COLOR_CYAN)


    #create windows & header

    #Depth First Search
    win_dfs_head = curses.newwin(3, 20, 16, 60)
    win_dfs_head.addstr(0,1,'Depth First Search',curses.A_BOLD)
    win_dfs_head.addstr(1,4,'Stepcount: 0')
    win_dfs_head.refresh()
    win_dfs = curses.newwin(21,20,20,60)

    # Breath First search
    win_bfs_head = curses.newwin(3, 20, 16, 90)
    win_bfs_head.addstr(0,0,'Breath First Search',curses.A_BOLD)
    win_bfs_head.addstr(1,4,'Stepcount: 0')
    win_bfs_head.refresh()
    win_bfs = curses.newwin(21,20,20,90)

    # A* search
    win_a_star_head = curses.newwin(3, 20, 16, 120)
    win_a_star_head.addstr(0,6,'A* Search',curses.A_BOLD)
    win_a_star_head.addstr(1,4,'Stepcount: 0')
    win_a_star_head.refresh()
    win_a_star = curses.newwin(21,20,20,120)


    # initial update
    g.update_fields([win_bfs,win_dfs,win_a_star])

    #execute Searching algorithm
    g.dfs(win_dfs,win_dfs_head)
    g.bfs(win_bfs,win_bfs_head)
    g.a_star(win_a_star,win_a_star_head)

    # listen for keystroke for exit
    win_dfs.getch()


#start visualization
wrapper(main)
