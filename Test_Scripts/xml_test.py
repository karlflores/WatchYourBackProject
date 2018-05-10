from XML.xml_helper import xml_helper
weights = [1000, 50, 5, -100, 300, 1000, 500,220,100,50]
test = xml_helper("./XML","/eval_weights")
test.save(weights)
w = test.load()
for ws in w:
    print(ws,end=' ')
