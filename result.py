from xml.etree import ElementTree

def parseResult(element):
    assert element.tag == 'result'
    result = Result()
    result.code = element.attrib['code']
    result.confidence = element.attrib['confidence']
    result.level = element.attrib['level']
    result.message = element.attrib['message']
    result.value = element.text
    return result

class Result:
    def __str__(self):
        return 'code: %s, message: %s, value: %s' % (self.code, self.message, self.value)

def main():
    testString = '<result xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:type="authenticationResult" confidence="0.0" level="0" code="0" message="OK">SUCCESS</result>'
    r = parseResult(ElementTree.XML(testString))
    print r
    
if __name__ == '__main__':
    main()


        
