from xml.etree import ElementTree

class DisplayItem:
    def __init__(self, element):
        assert element.tag == 'display_item'
        self.name = element.attrib['name']
        self.display_name = element.find('display_name').text
        self.nick_name = element.find('nickname').text
        self.input_element = element.find('form_element').text

    def __str__(self):
        return 'name: %s, display name: %s, nick name: %s, input: %s' % (self.name, self.display_name, self.nick_name, self.input_element)

def main():
    testString = """<display_item name="passphrase">
  <display_name>Password</display_name>
  <form_element>&lt;input id=&quot;AuthParam0&quot; type=&quot;password&quot; name=&quot;passphrase&quot; /&gt;</form_element>
  <nickname>Guest Password</nickname>
</display_item>"""
    di = DisplayItem(ElementTree.XML(testString))
    print di
    
if __name__ == '__main__':
    main()
