
import os.path
import xml.etree.ElementTree as et

CONF_FOLDER = "conf"
EDGES_XML = None


def loadEdges():
   xmlfile = f"{CONF_FOLDER}/edges.xml"
   if not os.path.exists(xmlfile):
      return False
   # -- else --
   global EDGES_XML
   tree = et.parse(xmlfile)
   EDGES_XML = tree.getroot()
   for elmt in EDGES_XML:
      check(elmt)


def check(elmt: et.Element):
   print(elmt.attrib["hostname"])


def main():
   pass


# -- entry point --
if __name__ == "__main__":
   loadEdges()
   main()
