#!/usr/bin/env python3
"""Generate and solve mazes using DFS, BFS, and A*."""
import sys,random,heapq,math
from collections import deque

def generate(w,h,seed=42):
    random.seed(seed);grid=[[1]*(2*w+1) for _ in range(2*h+1)]
    for y in range(h):
        for x in range(w):grid[2*y+1][2*x+1]=0
    visited=set();stack=[(0,0)];visited.add((0,0))
    while stack:
        x,y=stack[-1];neighbors=[]
        for dx,dy in [(0,-1),(0,1),(-1,0),(1,0)]:
            nx,ny=x+dx,y+dy
            if 0<=nx<w and 0<=ny<h and (nx,ny) not in visited:neighbors.append((nx,ny,dx,dy))
        if neighbors:
            nx,ny,dx,dy=random.choice(neighbors);visited.add((nx,ny))
            grid[2*y+1+dy][2*x+1+dx]=0;stack.append((nx,ny))
        else:stack.pop()
    return grid

def solve_bfs(grid,start,end):
    q=deque([start]);visited={start};parent={}
    while q:
        x,y=q.popleft()
        if (x,y)==end:
            path=[];n=end
            while n in parent:path.append(n);n=parent[n]
            path.append(start);return list(reversed(path))
        for dx,dy in [(-1,0),(1,0),(0,-1),(0,1)]:
            nx,ny=x+dx,y+dy
            if 0<=nx<len(grid[0]) and 0<=ny<len(grid) and grid[ny][nx]==0 and (nx,ny) not in visited:
                visited.add((nx,ny));parent[(nx,ny)]=(x,y);q.append((nx,ny))
    return None

def render(grid,path=None):
    ps=set(path) if path else set()
    chars={0:" ",1:"█"}
    for y,row in enumerate(grid):
        line=""
        for x,cell in enumerate(row):
            if (x,y) in ps:line+="·"
            else:line+=chars.get(cell,"?")
        print(line)

def main():
    import argparse
    p=argparse.ArgumentParser(description="Maze generator and solver")
    p.add_argument("-w","--width",type=int,default=20)
    p.add_argument("-H","--height",type=int,default=10)
    p.add_argument("--seed",type=int,default=42)
    args=p.parse_args()
    grid=generate(args.width,args.height,args.seed)
    start=(1,1);end=(2*args.width-1,2*args.height-1)
    path=solve_bfs(grid,start,end)
    print(f"=== Maze {args.width}x{args.height} ===")
    render(grid,path)
    if path:print(f"\nPath length: {len(path)}")

if __name__=="__main__":main()
