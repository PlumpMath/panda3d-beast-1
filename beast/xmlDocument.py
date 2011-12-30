#! /usr/bin/python
#---------------------------------------------------------------------------#
#- Beast - An Panda3d user interface library - See included "License.txt" - #
#---------------------------------------------------------------------------#
#- Beast, xmlDocument.py parses an xml document simply using xml.etree.ElementTree
from xml.etree.ElementTree import ElementTree


class xmlElement:
	def __init__(self, oe):
		self.__attribs = oe.attrib
		self.__tag = oe.tag
		self.__text = oe.text
		self.__children = []
		self.__parent = None

	def ls(self):
		tmp = str()
		for num, i in self._getAllChildren():
			tmp += ('    ' * num) + '%s/\n' % i.getTag()
		return tmp[:-1]

	def __str__(self):
		return '<xmlElement "%s" at %s>' % (self.__tag, hex(id(self)))

	def _getAllChildren(self, depth = 0):
		allChildren = [(depth, self)]
		for child in self.getChildren():
			allChildren += child._getAllChildren(depth + 1)
		return allChildren

	def _addChild(self, child):
		self.__children.append(child)
		child._setParent(self)

	def _setParent(self, parent):
		self.__parent = parent

	def getTag(self):
		return self.__tag

	def getText(self):
		return self.__text

	def getAttrib(self, name):
		return self.__attribs[name]

	def getAttribs(self):
		return self.__attribs

	def getParent(self):
		return self.__parent

	def getChildren(self):
		return self.__children


class xmlDocument:
	def getRootElement(self):
		return self.__rootElement

	def getElementByName(self, name):
		if name in self.__domByName:
			return self.__domByName[name]

	def getElementsByGroup(self, group):
		if group in self.__domByGroup:
			return self.__domByGroup[group]

	def parse(self, filePath):
		self.__domByName = {}
		self.__domByGroup = {}
		self.__tree = ElementTree()
		self.__tree.parse(filePath)
	#	print self.tree.find('include')

		root = self.__tree.getroot()
		self.__rootElement = xmlElement(root)
		self.__handleChildren(self.__rootElement, root)

	def __handleChildren(self, re, elem):
		if 'name' in elem.attrib:
			self.__domByName[elem.attrib['name']] = re
		if 'group' in elem.attrib:
			group = elem.attrib['group']
			if (group in self.__domByGroup) == False:
				self.__domByGroup[group] = []
			self.__domByGroup[group].append(re)

		for child in elem.getchildren():
			cre = xmlElement(child)
			re._addChild(cre)
			self.__handleChildren(cre, child)


if __name__ == '__main__':
	dom = xmlDocument()
	dom.parse('data/test_window.xml')
	print dom.getElementByName('mywindow')
	print dom.getElementByGroup('1')

	dom = xmlDocument()
