import xml.etree.ElementTree as ET
from xml.etree.ElementTree import Element
from xml.etree.ElementTree import ElementTree

class xml_helper(object):

    def __init__(self,path,file_name,name="Eval 1.0"):
        self.path = path
        self.filename = file_name
        self.name = name
        self.weight_count = 0

    # LOAD IN THE XML FILE AND RETURN THE WEIGHTS
    def load(self):
        weights = []
        # load the xml file
        tree = ET.parse(self.path + self.filename + ".xml")
        if tree is None:
            # could not open the xml file
            return None

        # get the root of the tree
        root = tree.getroot()

        # get the name of the xml file
        base_path = "./Parameters/"

        # get the name of the evaluation function
        name = root.findall(base_path+"Name")
        # set the name of the xml file to this
        for text in name:
            self.name = text.text
            # print(text.text)

        # get the weights count
        weight_num = root.findall(base_path+"NumWeights")
        for text in weight_num:
            self.weight_count = int(text.text)
            # print(text.text)

        base_path = "./Weights"

        for weight_index in range(self.weight_count):
            # print(weight_index)
            weight_path = (base_path + "/Weight/[@Index='{}']".format(str(weight_index)))
            w_i = root.findall(weight_path)

            weight_val = 0
            for weight in w_i:
                weight_val = float(weight.text)
                break

            weights.append(float(weight_val))

        # print(weights)

        # return the weights
        return weights

    # SAVE WEIGHTS TO THE XML FILE
    def save(self, weights):

        # create the root of the xml file
        xml_root = Element("EvaluationWeights")
        tree = ElementTree(xml_root)

        #
        xml_root = Element("EvaluationWeights")
        xml_root.set("ML-Type","TD-Leaf-Lambda")
        tree = ElementTree(xml_root)
        # create the Parameters Tag
        parameters = Element("Parameters")
        xml_root.append(parameters)

        # name of the evaluation function
        name = Element("Name")
        name.text = self.name
        parameters.append(name)

        # length of the weights
        weight_len = Element("NumWeights")
        weight_len.text = str(len(weights))
        parameters.append(weight_len)

        # Weight element
        weight_entry = Element("Weights")
        xml_root.append(weight_entry)

        for i in range(len(weights)):
            weight = Element("Weight")
            weight.set("Index", str(i))
            weight.text = str(weights[i])
            weight_entry.append(weight)

        tree.write(self.path+self.filename+".xml")
        return
