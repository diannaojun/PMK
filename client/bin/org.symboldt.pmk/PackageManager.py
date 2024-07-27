import json, os, requests, tarfile,shutil

class PackageManager:
    def __init__(self):
        self.__load_config()

    def get_installed(self,package_id):
        pkg=self.installed["list"].get(package_id)
        if pkg!=None: return (True,pkg["version"])
        return False

    def install_package(self, package_id, ver=0):
        SCS=False
        pkg=self.get_installed(package_id)
        package_name="[package_name]"
        version="[version]"
        if(pkg!=False):
            print(f"Package \"{package_id}\" ({pkg[1]}) is already installed.")
            if(pkg[1]<ver): self.update_package(package_id,ver)
        else:
            for hub in self.config["source"]:
                if SCS: break
                url=os.path.join(hub,"list")
                try:
                    response = requests.get(url)
                    content=str(response.content,"utf-8")
                    content=json.loads(content)
                    for pak in content["list"]:
                        if(pak["id"]==package_id):
                            if(pak["version"]<ver): break
                            package_name=pak["name"]
                            version=pak["version"]
                            dpdc=pak["dependence"]
                            for dpk in dpdc: self.install_package(dpk["id"])
                            url=os.path.join(hub,"get")
                            url=os.path.join(url,package_id)
                            getr=requests.get(url)
                            workpath=os.path.join("./temp",package_id)
                            wp=os.path.join(self.config["bin_path"],package_id)
                            with open(workpath,"wb") as fp:
                                fp.write(getr.content)
                            with tarfile.open(workpath) as tar:
                                if(not os.path.isdir(wp)): os.mkdir(wp)
                                tar.extractall(wp)
                                tar.close()
                            self.installed["list"][package_id]={"id":package_id,"name":pak["name"],"source":hub,"version":pak["version"],"dependence":pak["dependence"]}
                            os.remove(workpath)
                            SCS=True
                except Exception as ex:
                    print("error",ex)
                    return ()
                else:
                    if SCS: print(f"Package \"{package_name}\" version {version} installed successfully.")
                    else: print("Cannot find the package!")

    def uninstall_package(self, package_id):
        if self.get_installed(package_id)!=False:
            wp=os.path.join(self.config["bin_path"],package_id)
            try: shutil.rmtree(wp)
            except FileNotFoundError as ex: pass
            pak=self.installed["list"][package_id]
            self.installed["list"].pop(package_id)
        else:
            print(f"Package '{package_name}' is not installed.")

    def update_package(self, package_id,ver=0):
        pkg=self.get_installed(package_id)
        if(pkg==False): self.install_package(package_id,ver)
        elif(pkg[1]>=ver): print(f"Package \"{package_id}\" ({pkg[1]}) is already newest.")
        else:
            SCS=False
            pkg=self.installed["list"][package_id]
            for hub in self.config["source"]:
                if SCS:break
                url=os.path.join(hub,"list")
                try:
                    response = requests.get(url)
                    content=str(response.content,"utf-8")
                    content=json.loads(content)
                    for pak in content["list"]:
                        if(pak["id"]==package_id):
                            if(pak["version"]<ver): break
                            pkg["name"]=pak["name"]
                            pkg["version"]=pak["version"]
                            pkg["dependence"]=pak["dependence"]
                            for dpk in pkg["dependence"]: self.install_package(dpk["id"],dpk["version"])
                            url=os.path.join(hub,"get")
                            url=os.path.join(url,package_id)
                            getr=requests.get(url)
                            workpath=os.path.join("./temp",package_id)
                            wp=os.path.join(self.config["bin_path"],package_id)
                            with open(workpath,"wb") as fp:
                                fp.write(getr.content)
                            with tarfile.open(workpath) as tar:
                                if(not os.path.isdir(wp)): os.mkdir(wp)
                                tar.extractall(wp)
                                tar.close()
                            self.installed["list"][package_id]=pkg
                            os.remove(workpath)
                            SCS=True
                except Exception as ex:
                    print("error",ex)
                    return ()
                else:
                    if SCS: print(f"Package \"{pkg["name"]}\" version {pkg["version"]} updated successfully.")
                    else: print("Cannot find the package!")

                

    def list_installed_packages(self):
        print("Packages are installed:")
        for pak in self.installed["list"].values():
            print(f"\t{pak["name"]}\t{pak["version"]}\t{pak["id"]}")

    def list_hubs(self):
        for hub in self.config["source"]:
            print(hub)

    def list_packages(self):
        for hub in self.config["source"]:
            url=os.path.join(hub,"list")
            try:
                response = requests.get(url)
                content=str(response.content,"utf-8")
                content=json.loads(content)
                print(f"{content["name"]}\t{hub} :")
                for pak in content["list"]:
                    print(f"\t{pak["name"]}\t{pak["version"]}\t{pak["id"]}")
            except Exception as ex:
                print(f"{hub} is dead!\n{ex}")

    def __load_config (self):
        if(os.path.exists("./config.json")):
            with open("./config.json") as fp:
                self.config = json.loads(fp.read())
        else:
            raise FileNotFoundError("You lost your config file of pmk!\n"+
                "plase check the file \""+os.path.abspath("./config.json")+"\"")
        if(os.path.exists("./installed.json")):
            with open("./installed.json") as fp:
                self.installed = json.loads(fp.read())
        else:
            raise FileNotFoundError("You lost your config file of pmk!\n"+
                "plase check the file \""+os.path.abspath("./installed.json")+"\"")
    def __del__(self):
        with open("./config.json","w") as fp:
             fp.write(json.dumps(self.config))
        with open("./installed.json","w") as fp:
             fp.write(json.dumps(self.installed))

