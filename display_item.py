from xml.etree import ElementTree

def parseDisplayItem(element):
    assert element.tag == 'display_item'
    display_item = DisplayItem()
    display_item.name = element.attrib['name']
    display_item.display_name = element.iter('display_name').next().text
    display_item.nick_name = element.iter('nickname').next().text
    display_item.input_element = element.iter('form_element').next().text
    return display_item

class DisplayItem:
    def __str__(self):
        return 'name: %s, display name: %s, nick name: %s, input: %s' % (self.name, self.display_name, self.nick_name, self.input_element)

def main():
    testString = """<display_item name="passphrase">
  <display_name>Password</display_name>
  <form_element>&lt;input id=&quot;AuthParam0&quot; type=&quot;password&quot; name=&quot;passphrase&quot; /&gt;</form_element>
  <nickname>Guest Password</nickname>
</display_item>"""
    di = parseDisplayItem(ElementTree.XML(testString))
    print di
    
if __name__ == '__main__':
    main()
