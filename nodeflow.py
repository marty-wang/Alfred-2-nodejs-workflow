import subprocess, plistlib, os
from os import path
from feedback import Item, feedback

SETTINGS_PATH = 'settings.plist'
NODE_PATH = 'node_path'

class NodeFlow(object):
    """docstring for NodeFlow"""
    def __init__(self):
        super(NodeFlow, self).__init__()

    def has_node(self):
        proc = subprocess.Popen(['which', 'node'], stdout = subprocess.PIPE, stderr = subprocess.PIPE)
        out = proc.stdout.read()
        if out:
            return True
        else:
            return False

    def set_node(self, path):
        self.add_node_to_evn(path)
        self.set(NODE_PATH, path)

    def add_node_to_evn(self, path):
        os.environ["PATH"] = path + ":" + os.environ["PATH"]

    def set(self, key, value, file = SETTINGS_PATH):
        if path.isfile(file):
            obj = plistlib.readPlist(file)
        else:
            obj = dict()

        obj[key] = value
        plistlib.writePlist(obj, file)

    def get(self, key, file = SETTINGS_PATH):
        if not path.isfile(file):
            return None

        obj = plistlib.readPlist(file)
        return obj.get(key)

    def ensure_node(self):
        has_node = self.has_node()

        if has_node:
            return True
        else:
            node_path = self.get(NODE_PATH)
            if node_path == None:
                has_node = False
            else:
                self.add_node_to_evn(node_path)
                has_node = self.has_node()

        return has_node

    def feedback(self, has_node):
        if has_node:
            title = "Node is available!"
        else:
            title = "Node is not found, please set its path!"
        item = Item(uid="node", valid="no", title=title, icon="nodejs.png")
        feedback(item)

    def run(self, args):
        return subprocess.call(args)