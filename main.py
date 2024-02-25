import maze
import time
import cProfile

test_maze = maze.Maze(1000, 1000, 0.3)

# test_maze.display()
# exit()

# start_dfs = time.time()
# res_dfs = test_maze.solve_dfs()
# stop_dfs = time.time()
#
# start_bfs = time.time()
# res_bfs = test_maze.solve_bfs()
# stop_bfs = time.time()
#
# start_astar = time.time()
# res_astar = test_maze.solve_astar()
# stop_astar = time.time()
#
# print("::: LOOPS :::")
# print("DFS", res_dfs[2])
# print("BFS", res_bfs[2])
# print("Astar", res_astar[2])
#
# print("::: TIME :::")
# print("DFS",  stop_dfs - start_dfs)
# print("BFS", stop_bfs - start_bfs)
# print("Astar",  stop_astar - start_astar)

# test_maze.display_result(res_dfs[0], res_dfs[1])
# test_maze.display_result(res_bfs[0], res_bfs[1])
# test_maze.display_result(res_astar[0], res_astar[1])

# the maze was generated using dfs and has less branching and longer corridors
# dfs is fastest here
# bfs is slow as it will check all possibilities but always gives shortest path
# astar is worst as priority queue is additional computation which doesn't help as there is only single solution

# heiristics - best is Manhattan + Euclidean

test_maze.display_final()
# # print(res[1])

cProfile.run('test_maze.solve_dfs()')
cProfile.run('test_maze.solve_bfs()')
cProfile.run('test_maze.solve_astar()')
