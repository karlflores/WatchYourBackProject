'''
this file originally was used to test the xml-helper class, but now it has been repurposed to write the different
weights the white and black pieces

'''
from XML.xml_helper import xml_helper
# diff_pieces, dist_cent, num_vulnerable, self_surrounded, opp_surrounded, middle_occupy, num_cluster,
# edge_vuln, next_to_corner, sum_min_man_dist, diff_elim_pattern, diff_root_pieces

# weights = [1000, 300, 5, -100, 300, 2000, 100,220,550, 50, 5000, 3000]
weights = [300, 80, 95, -50, 60, 170, -90, 95, 80, 10, 50, 90]
# weights = [100,0,0,0,0,0,0,0,0,0,0,0]
test = xml_helper("./XML","/white_weights")
test.save(weights)
w = test.load()
for ws in w:
    print(ws,end=' ')

weights = [500, 40, 120, -50, 100, 30, -130, 95, 80, 4, 50, 150]
test = xml_helper("./XML","/black_weights")
test.save(weights)
w = test.load()
for ws in w:
    print(ws,end=' ')
