from xml.etree import ElementTree

def parseFormElement(element):
    assert element.tag == 'form_element'
    form_element = FormElement()
    form_element.name = element.attrib['name']
    form_element.display_name = element.attrib['display_name']
    form_element.input_element = element.iter('element').next().text
    return form_element

class FormElement:
    def __str__(self):
        return 'name: %s, display name: %s, input: %s' % (self.name, self.display_name, self.input_element)
"""
<enrollment_pretext>
  <name>richardl@ufp.comt</name>
  <result xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:type="enrollmentResult" level="0" code="0" message="OK">SUCCESS</result>
  <form_element display_name="Password" name="passphrase">
    <element>&lt;input id="EnrollParam0" type="password" name="passphrase" /&gt;</element>
  </form_element>
</enrollment_pretext>
"""
        
def main():
    testString = """<form_element display_name="Password" name="passphrase">
  <element>&lt;input id="EnrollParam0" type="password" name="passphrase" /&gt;</element>
</form_element>"""

    fe = parseFormElement(ElementTree.XML(testString))
    print fe
    
if __name__ == '__main__':
    main()
