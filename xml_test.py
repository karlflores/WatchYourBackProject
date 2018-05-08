from XML.xml_helper import xml_helper
weights = [1000,50,30,-1000,200,1000,200]
test = xml_helper("./XML","/eval_weights")
test.save(weights)
w = test.load()
for ws in w:
    print(ws,end=' ')
