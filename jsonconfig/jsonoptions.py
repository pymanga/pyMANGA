''' Helper script for the pyManga.json notation.
    def parse_jsontemplate: returns a python dictionary with the resolved
    dependencies.
    def buildXML(option): returns xml string for a option object.
'''
import json
from xml.etree import ElementTree as ET
from xml.dom import minidom
import copy


def dict_updateNew(data, add):
    ''' Goes recursively throug dict "add" and adds
        all entries that are missing in dict "data".'''
    for k, v in add.items():
        if k not in data:
            data[k] = add[k]
        if isinstance(v, dict):
            subdict = data[k]
            data[k] = dict_updateNew(subdict, v)

    return data


def option_resolveReferences(option, optionMap, baseOptions):
    # Replace ref with option if neccessary
    if "$ref" in option:
        ref = option["$ref"]
        option.update(optionMap[ref])
        del option["$ref"]

    # Insert missing parameters from base option if neccesary
    if "$base" in option:
        basetype = baseOptions[option["$base"]]
        option = dict_updateNew(option, basetype)
        del option["$base"]

    # Recursively go through suboptions in case of complex type
    if option["typedict"]["type"] == "complex":
        for subOption in option["value"]:
            subOption = option_resolveReferences(subOption, optionMap,
                                                 baseOptions)

    if option["typedict"]["type"] == "alternative":
        for subOption in option["typedict"]["alternatives"]:
            subOption = option_resolveReferences(subOption, optionMap,
                                                 baseOptions)

    if "$namespace" in option:
        del option["$namespace"]
    return option


def fqn(option):
    namespace = "{}:".format(
        option["$namespace"]) if "$namespace" in option else ""
    return "{}{}".format(namespace, option["name"])


def parse_jsontemplate(path):
    ''' Parses json file and returns the options with resolved dependencies'''
    with open(path) as jsonFile:
        d = dict(json.load(jsonFile))
        # Transform array to dict to make basetypes accesible by name
        baseOptions = {data["name"]: data for data in d["base"]}
        optionMap = {fqn(data): data for data in d["options"]}

        for name, option in optionMap.items():
            option = option_resolveReferences(option, optionMap, baseOptions)

    return optionMap


def buildNode(option):
    ''' Transform option in xml tree.
        option.name becomes a xml element tag.
        option.value becomes element entry if the option is of type "integer",
        "float" or "string".
        option.value holds suboptions if option is of type "complex"
        if option is of type "alternative", option.value is the index of the
        chosen alternative.
    '''
    name = option["name"]
    if option["typedict"]["type"] == "complex":
        node = ET.Element(name)
        subnodes = list()
        for subOption in option["value"]:
            subnodes.append(buildNode(subOption))

        node.extend(subnodes)

    elif option["typedict"]["type"] == "alternative":
        index = option["value"]
        alternative = option["typedict"]["alternatives"][index]
        alternative["name"] = option["name"]
        node = buildNode(alternative)

    else:
        node = ET.Element(name)
        node.text = str(option["value"])

    return node


def buildXML(option):
    root = buildNode(option)
    xmlstr = minidom.parseString(ET.tostring(root)).toprettyxml(indent="   ")
    return xmlstr


if __name__ == "__main__":
    path = "./pyManga.json"
    options = parse_jsontemplate(path)
    xml = buildXML(options["MangaProject"])
