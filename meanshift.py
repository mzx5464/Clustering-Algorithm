import math
import random
import numpy as np
import matplotlib.pyplot as plt

class meanshift():
    maxn = 1000
    r = 2
    points = np.zeros([maxn, 3], dtype=np.float32)
    ori = np.zeros([maxn, 3],dtype=np.float32)
    points_num = 0
    prefix = "D:\OneDrive\Document\Learning\Crouse\Junior\Pattern Recognition\Clustering\synthetic_data\\%s"

    def load_data(self):
        file_in = open(self.prefix % 'Aggregation.txt')
        c = 0
        for row in file_in:
            row = row.strip('\n')
            point = row.split(",")
            self.points[c][0:2] = point[0:2]
            self.ori[c] = point
            self.points[c][2] = c
            c += 1
        self.points_num = c
        print("There are ", c, " points\n")
        file_in.close()

    def distance(self, x1, y1, x2, y2):
        return math.sqrt((x1 - x2)*(x1 - x2) + (y1 - y2)*(y1 - y2))

    def output(self):
        file_out = open(self.prefix % 'Aggregation_res.txt',"w")
        for i in range(self.points_num):
            file_out.write("{},{},{}\n".format(self.ori[i,0],self.ori[i,1],self.points[i][2]))
        file_out.close()

    def shift(self):
        t = 0
        while True:
            maxmov = 0
            for i in range(self.points_num):
                x = self.points[i][0]
                y = self.points[i][1]
                c = self.points[i][2]
                sumx = sumy = counter = 0
                for j in range(self.points_num):
                    dis = self.distance(x, y, self.points[j][0], self.points[j][1])
                    if dis <= self.r:
                        sumx += (self.points[j][0] - x)
                        sumy += (self.points[j][1] - y)
                        self.points[j][2] = c
                        counter += 1
                self.points[i][0] += sumx * 0.1
                self.points[i][1] += sumy * 0.1
                delta = abs(sumx) + abs(sumy)
                if(maxmov < delta):
                    maxmov = delta
            t += 1
            print(t,"th loop")
            if (maxmov < 100):
                break

    def clear(self):
        print()


if __name__ == "__main__":
    ms = meanshift()
    ms.load_data()
    ms.shift()
    ms.output()

    # a = np.concatenate((ms.ori[:,0:2], ms.points[:,2:3]), axis = 1)
    # for i in range(ms.points_num):
    #     print(a[i])

    fig = plt.figure(figsize=(10,5))
    img0 = fig.add_subplot(121)
    plt.scatter(ms.ori[:,0], ms.ori[:,1], c = ms.ori[:,2])
    img0.set_title("Ori")
    img1 = fig.add_subplot(122)
    plt.scatter(ms.ori[:,0], ms.ori[:,1], c = ms.points[:,2])
    img1.set_title("meanshift")

    plt.show()
