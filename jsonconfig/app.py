from flask import Flask, jsonify, request,redirect, Response,send_from_directory
from flask_cors import CORS
import json
import jsonoptions
import copy

app = Flask(__name__,static_url_path='')
CORS(app)

global option
global optionMap

path = "./pyManga.json"
optionMap = jsonoptions.parse_jsontemplate(path)
option = optionMap["MangaProject"]

def renameMultiOccur(option):
    def rename (option):
        option["name"] = option["name"].split("#")[0]

    return jsonoptions.forEachOptionApply(option,rename)



@app.route("/")
def frontend():
    return redirect("/fe")

@app.route('/fe', defaults={'path': 'index.html'})
@app.route('/fe/<path:path>')
def send_js(path):
    return send_from_directory('static/build',path)


@app.route('/api/optionTemplate')
def defaultTemplate():
    global option
    
    path = "./pyManga.json"
    defaultTemplate = jsonoptions.parse_jsontemplate(path)["MangaProject"]
    # Remove visualisation and tree_output
    defaultTemplate["value"] = [ item for item in defaultTemplate["value"] if item["name"] not in ["visualization","tree_output"] ]

    option = defaultTemplate
    return defaultTemplate


@app.route('/api/syncOption', methods=['POST'])
def sync():
    global option 
    option = request.json
    return "OK"


@app.route('/api/XML')
def getXML():
    global option
    global optionMap
    
    visualization = copy.deepcopy(optionMap["default:visualization"])
    output = copy.deepcopy(optionMap["webui:tree_output"])
    
    clone = copy.deepcopy(option)
    clone["value"].append(visualization)
    clone["value"].append(output)

    renameMultiOccur(clone)

    xml = jsonoptions.buildXML(clone)
    return Response(xml, mimetype='text/xml')






if __name__=="__main__":
    app.run()
