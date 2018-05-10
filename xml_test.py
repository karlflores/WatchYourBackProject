from XML.xml_helper import xml_helper
weights = [1000, 0, 0, 0, 0, 0, 0,0,0, 0, 15000]
test = xml_helper("./XML","/eval_weights2")
test.save(weights)
w = test.load()
for ws in w:
    print(ws,end=' ')
