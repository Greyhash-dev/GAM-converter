import numpy as np
from stl import mesh
mesh = mesh.Mesh.from_file('ok.stl')
vectors = mesh.vectors
points = []
mult = float(input("Multiplier: "))

if 0:
    for triangle in vectors:
        for point in triangle:
            if point.tolist() not in points:
                points.append([int(i*mult) for i in point.tolist()])

    connections = []
    for triangle in vectors:
        for i in range(0, len(triangle)):
            point = triangle[i]
            point_2 = triangle[i-1]
            con = [points.index([int(i*mult) for i in point.tolist()]), points.index([int(i*mult) for i in point_2.tolist()])]
            if not (con in connections or [con[1], con[0]] in connections):
                connections.append(con)

# print("=".join([".".join([str(t) for t in i]) for i in points])+"|"+"=".join([".".join([str(t) for t in i]) for i in connections]))

out = "int data["+str(len(vectors))+"][3][3] = {\n"
cnt_2 = 0
min_vals = [1000, 1000, 1000]
max_vals = [-1000,-10000,-10000]
for triangle in vectors:
    for point in triangle:
        if min_vals[0] > point[0]:
            min_vals[0] = point[0]
        if min_vals[1] > point[1]:
            min_vals[1] = point[1]
        if min_vals[2] > point[2]:
            min_vals[2] = point[2]
        if max_vals[0] < point[0]:
            max_vals[0] = point[0]
        if max_vals[1] < point[1]:
            max_vals[1] = point[1]
        if max_vals[2] < point[2]:
            max_vals[2] = point[2]
sub = [(max_vals[0] - min_vals[0])/2, (max_vals[1] - min_vals[1])/2, (max_vals[2] - min_vals[2])/2]

out = "~7341891 schwarz,2,Projekt\n"
out += "~7341891 erzeugt von GAMV19e - Demo\n"
out += "nichtkonvex nichtmodelliert\n"
out += "0.0  0.0  0.0\n"
out += str(len(vectors)*3)+"\n"
connections = []
tr = []
cnt = 1
for triangle in vectors:
    for i in range(0,3):
        out += f"{format(triangle[i][0], '.8f')}  {format(triangle[i][1], '.8f')}  {format(triangle[i][2], '.8f')}\n"
    connections.append(f"{cnt} {cnt+1}\n{cnt+1} {cnt+2}\n{cnt+2} {cnt}")
    cnt += 3
out += str(len(connections)*3)+"\n"
out += "\n".join(connections)+"\n"
out += str(len(vectors))+ " schwarz\n"
cnt = 1
for triangle in vectors:
    out += "3 schwarz\n"
    for _ in range(0,3):
        out += str(cnt)+"\n"
        cnt += 1

with open("data.gap", "w") as f:
    f.write(out)
