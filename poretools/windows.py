import _winreg
import os

current_version = None

try:
	key = _winreg.OpenKey(_winreg.HKEY_CURRENT_USER, "SOFTWARE\\R-core\\R")
except Exception:
	key = _winreg.OpenKey(_winreg.HKEY_LOCAL_MACHINE, "SOFTWARE\\R-core\\R")

version = _winreg.QueryValueEx(key, "Current Version")[0]
install_path = _winreg.QueryValueEx(key, "InstallPath")[0]

os.environ['R_HOME'] = install_path
os.environ['R_USER'] = os.environ['HOMEPATH'] + '\\Documents'

print "Setting R_HOME to %s" % (install_path,)
print "Setting R_USER to %s" % (os.environ['R_USER'])

