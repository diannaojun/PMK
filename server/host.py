from http.server import HTTPServer
from http.server import SimpleHTTPRequestHandler
from http.server import BaseHTTPRequestHandler
import urllib.request, tarfile
import json, os, sys, tempfile

fp = open("./applist.json")
jsonData = fp.read()
fp.close()
applist = json.loads(jsonData)
root=os.getcwd()

class HubHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        url = self.path
        if(url=="/" or url==""):
            self.send_response(202)
            self.end_headers()
        elif(url=="/list"):
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            with open("./applist.json") as fp: self.wfile.write(bytes(fp.read(), 'utf-8'))
            print(f"LIST []")
        elif(url.startswith("/get/")):
            pak=url[5:]
            for paks in applist["list"]:
                if(paks["id"]==pak):
                    self.send_response(200)
                    self.send_header('Content-type', 'application/octet-stream')
                    self.end_headers()
                    tmpfn=os.path.join("./temp/",pak+".tar")
                    if(not os.path.exists(tmpfn)):
                        tar = tarfile.open(tmpfn,"w:")
                        workpath=paks["source"]
                        catch=len(workpath)
                        for root,dir,files in os.walk(workpath):
                            for file in files:
                                fullpath = os.path.join(root,file)
                                tar.add(fullpath, os.path.join(root[catch:],file))
                        tar.close()
                    with open(tmpfn,"rb") as fp:
                        self.wfile.write(fp.read())
                    print(f"GET [{pak}]")
                    break
            else:
                self.send_response(404)
                self.end_headers()
        else:
            self.send_response(400)
            self.end_headers()

server=HTTPServer(("localhost",2121), HubHandler)

server.serve_forever()
