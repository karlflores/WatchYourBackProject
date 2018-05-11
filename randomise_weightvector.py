from XML.xml_helper import xml_helper
from random import randint
# diff_pieces, dist_cent, num_actions, self_surrounded, opp_surrounded, middle_occupy, num_cluster,
# edge_vuln, next_to_corner, sum_min_man_dist, diff_elim_pattern, diff_root_pieces

# weights = [1000, 300, 5, -100, 300, 2000, 100,220,550, 50, 5000, 3000]
weights = []
# diff_pieces,
weights.append(randint(0,150))
# dist_cent,
weights.append(randint(0,100))
# num_vulnerable,
weights.append(randint(0,100))
# self_surrounded,
weights.append(randint(-100,0))
# opp_surrounded,
weights.append(randint(0,80))
# middle_occupy,
weights.append(randint(0,200))
# num_cluster,
weights.append(randint(0,150))
# edge_vuln,
weights.append(randint(0,100))
# next_to_corner,
weights.append(randint(0,90))
# sum_min_man_dist,
weights.append(randint(0,40))
# diff_elim_pattern,
weights.append(randint(0,80))
# diff_root_pieces
weights.append(randint(0,100))

test = xml_helper("./XML","/randomise")
test.save(weights)
w = test.load()
for ws in w:
    print(ws,end=' ')
