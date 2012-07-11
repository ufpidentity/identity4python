from xml.etree import ElementTree

class Result:
    def __init__(self, element):
        assert element.tag == 'result'
        self.code = element.attrib['code']
        self.confidence = element.attrib['confidence']
        self.level = element.attrib['level']
        self.message = element.attrib['message']
        self.value = element.text

    def __str__(self):
        return 'code: %s, message: %s, value: %s' % (self.code, self.message, self.value)

def main():
    testString = '<result xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:type="authenticationResult" confidence="0.0" level="0" code="0" message="OK">SUCCESS</result>'
    r = Result(ElementTree.XML(testString))
    print r

if __name__ == '__main__':
    main()
