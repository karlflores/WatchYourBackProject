from XML.xml_helper import xml_helper
weights = [0,1.2342342,2,3,4,5]
test = xml_helper("./XML","/test")
test.save(weights)
w = test.load()
for ws in w:
    print(ws,end=' ')
