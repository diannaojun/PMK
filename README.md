# PackageManagerKi
一個軟件包管理器（客戶機、伺服器）

# 如何使用PackageManagerKi？
***PMK***是一個簡單的軟件包管理器，由***Python3.12***編寫。你可以使用它進行一些管理操作。
首先你需要一個軟件源服務器——這裏已經在`/hub`目錄搭建好了，使用"host.py"運行。
然後，你需要配置本地設置——`/bin/org.symboldt.pmk`（PMK目錄）下的`config.json`已經包含默認本地測試源（上文的測試服務器）。

現在你可以使用PMK了。請進入PMK目錄，指令行運行main.py，按照其提示進行操作。
：）


---以下爲舊版
PMK是一個簡單的軟件包管理器，由Python3.12編寫。你可以使用牠進行一些管理操作。

首先你需要一個軟件源服務器——這裏已經在“/hub”目錄搭建好了，使用"host.py"運行。

然後，你需要配置本地設置——“/bin/org.symboldt.pmk”（PMK目錄）下的"config.json"已經包含默認本地測試源（上文的測試服務器）。

然後你可以運行PMK。在PMK目錄下打開python3指令行，引入pmk。新建一個“PackageManager”對象。可以使用以下指令：
- pmk.get_installed(package_id)		獲取是否安裝有id爲package_id的包
- pmk.install_package(package_id)	按照順序在設置的軟件源裏尋找並安裝id爲package_id的包
- pmk.uninstall_package(package_id)	卸載id爲package_id的包
- pmk.update_package()				目前不可用
- pmk.list_installed_packages()		列出當前安裝過的包[名稱，版本，id]
- pmk.list_hubs()					列出當前設置的源
- pmk.list_packages()				按照順序在設置的軟件源列出其擁有的包[名稱，版本，id]

記得在退出前使用del pmk保存設置。
