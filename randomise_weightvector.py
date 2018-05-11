from XML.xml_helper import xml_helper
from random import randint
# diff_pieces, dist_cent, num_actions, self_surrounded, opp_surrounded, middle_occupy, num_cluster,
# edge_vuln, next_to_corner, sum_min_man_dist, diff_elim_pattern, diff_root_pieces

# weights = [1000, 300, 5, -100, 300, 2000, 100,220,550, 50, 5000, 3000]
weights = []
for i in range(12):
    weights.append(randint(-100,100))
test = xml_helper("./XML","/randomise")
test.save(weights)
w = test.load()
for ws in w:
    print(ws,end=' ')
