from XML.xml_helper import xml_helper
weights = [100,100,10,-100,20,100,20]
test = xml_helper("./XML","/eval_weights")
test.save(weights)
w = test.load()
for ws in w:
    print(ws,end=' ')
