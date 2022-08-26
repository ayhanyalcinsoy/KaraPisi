#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Licensed under the GNU General Public License, version 3.
# See the file http://www.gnu.org/licenses/gpl.txt

from pisi.actionsapi import cmaketools
from pisi.actionsapi import shelltools
from pisi.actionsapi import autotools
from pisi.actionsapi import pisitools
from pisi.actionsapi import get

shelltools.export("JOBS", get.makeJOBS().replace("-j5", "-j4"))

def setup():
    shelltools.system("sed '/cond_add_subdirectory(capstone/d' -i ./deps/CMakeLists.txt")
    shelltools.system("sed '/cond_add_subdirectory(keystone/d' -i ./deps/CMakeLists.txt")
    shelltools.system("sed '/cond_add_subdirectory(llvm/d' -i ./deps/CMakeLists.txt")
    shelltools.system("sed '/cond_add_subdirectory(rapidjson/d' -i ./deps/CMakeLists.txt")
    shelltools.system("sed '/cond_add_subdirectory(tinyxml2/d' -i ./deps/CMakeLists.txt")
    shelltools.system("sed '/cond_add_subdirectory(openssl/d' -i ./deps/CMakeLists.txt")
    #shelltools.system("sed '/cond_add_subdirectory(yara/d' -i ./deps/CMakeLists.txt")
    #shelltools.system("sed '/cond_add_subdirectory(yaramod/d' -i ./deps/CMakeLists.txt")
    shelltools.system('sed "s|get_install_path(sys.argv)| \"${D}\" + get_install_path(sys.argv)|g" -i ./support/install-share.py')
    #shelltools.system('sed "s|output = os.path.join|output = \"${D}\" + os.path.join|g" -i ./support/install-yara.py')
    shelltools.makedirs("build")
    shelltools.cd("build")
    cmaketools.configure("-DCMAKE_INSTALL_PREFIX=/usr" \
                          , sourceDir="..")
#-DCMAKE_SKIP_RPATH=True \
def build():
    shelltools.cd("build")
    autotools.make()

def install():
    # 2020-02-27: BlueDeviL's Note: while installing, CMakeLists execute a python script.
    # that script downloads a file from github and copies under /usr/share
    # so, to avoid sandbox violations we will do this process by modifying CMakeLists.txt
    shelltools.cd("build")
    cmaketools.rawInstall("DESTDIR=%s" % get.installDIR())
    shelltools.cd("..")
    pisitools.dodoc("README*", "LICENSE*")
    
    # retdec 4.0 creates static lib files under lib64, i move them:
    pisitools.domove("/usr/lib64/libretdec-*", "/usr/lib/retdec/static")
    pisitools.removeDir("/usr/lib64")
