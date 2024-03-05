# a-maze
Code for CS7IS2 Artificial Intelligence Assignment 1 at Trinity College Dublin

## Example commands

### 1. test different algos
```
python main.py -a dfs -s 20
python main.py -a bfs -s 20
python main.py -a astar -s 20
python main.py -a mdppit -s 20
python main.py -a mdpvit -s 20
```

### 2. compare astar heuristics
python compare_astar_heuristic.py

### 3. compare mdp params
#### 3.1 large value of theta
```
python main.py -a mdpvit -s 20 -g 0.99 -t 0.01
```

#### 3.2 smaller value of df
```
python main.py -a mdpvit -s 20 -g 0.9 -t 0.001
```

### 4. comparison
```
python compare.py
Enter algos: dfs bfs astar
Enter sample size: 1
Enter test maze size range: 500 551 50
Enter result file name (results.csv): test.csv
Testing maze size = 500
```

### 5. plotting comparison
```
python plot_results.py
Enter result file name (results.csv): test.csv
```