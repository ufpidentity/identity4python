import connection_handler
import display_item
import result
from xml.etree import ElementTree

"""
     <?xml version="1.0" encoding="UTF-8" standalone="yes"?>
     <enrollment_pretext>
       <name>test</name>
       <result code="0" message="OK">SUCCESS</result>
       <form_element display_name="Password" name="passphrase">
         <element>&lt;input id=&quot;EnrollParam0&quot; type=&quot;password&quot; name=&quot;passphrase&quot; /&gt;</element>
       </form_element>
     </enrollment_pretext>
"""
class PreEnrollmentResult:
    pass

def parsePreEnrollmentResult(xml):
    element = ElementTree.XML(xml)
    assert element.tag == 'enrollment_pretext'
    pre_enrollment_result = PreEnrollmentResult()
    pre_enrollment_result.result = result.parseResult(element.find('result'))
    pre_enrollment_result.name = element.find('name').text
    if pre_enrollment_result.result.value == 'SUCCESS':
        pre_enrollment_result.form_elements = []
        for fe in element.findall('form_element'):
            pre_enrollment_result.form_elements.append(FormElement.parseFormElement(fe))
    return pre_enrollment_result

class EnrollmentResult:
    pass

def parseEnrollmentResult(xml):
    element = ElementTree.XML(xml)
    print element.tag
    enrollment_result = EnrollmentResult() 
    enrollment_result.result = result.parseResult(element.find('result'))
    enrollment_result.name = element.find('name').text
    return enrollment_result

"""
     <?xml version="1.0" encoding="UTF-8" standalone="yes"?>
     <authentication_pretext>
       <name>richardl@ufp.com</name>
       <result xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:type="authenticationResult" confidence="0.0" level="0" code="0" message="OK">SUCCESS</result>
       <display_item name="secret">
         <display_name>Enter Secret</display_name>
         <form_element>&lt;input id=&quot;AuthParam0&quot; type=&quot;text&quot; name=&quot;secret&quot; /&gt;</form_element>
         <nickname>SAW (w/email)</nickname>
       </display_item>
     </authentication_pretext>
"""
class AuthenticationResult:
    pass

def parseAuthenticationResult(xml):
    print xml
    element = ElementTree.XML(xml)
    assert element.tag == 'authentication_pretext' or element.tag == 'authentication_context'
    authentication_result = AuthenticationResult()
    authentication_result.result = result.parseResult(element.find('result'))
    authentication_result.name = element.find('name').text
    if authentication_result.result.value == 'SUCCESS' or authentication_result.result.value == 'CONTINUE':
        authentication_result.display_items = []
        for di in element.findall('display_item'):
            authentication_result.display_items.append(display_item.parseDisplayItem(di))
    return authentication_result

    
class IdentityServiceProvider:
    def __init__(self, key_file, cert_file):
        self.connection_handler = connection_handler.IdentityConnectionHandler(key_file, cert_file)

    def preAuthenticate(self, name, host):
        data = { 'name': name, 'client_ip' : host }
        xml = self.connection_handler.sendMessage('preauthenticate', data)
        return parseAuthenticationResult(xml)

    def authenticate(self, name, host, params):
        xml = self.makeRequest(name, host, params, 'authenticate')
        return parseAuthenticationResult(xml)

    def preEnroll(self, name, host):
        data = { 'name' : name, 'client_ip' : host}
        xml = self.connection_handler.sendMessage("preenroll", data)
        return parsePreEnrollmentResult(xml)

    def enroll(self, name, host, params):
        xml = self.makeRequest(name, host, params, 'enroll')
        return parseEnrollmentResult(xml)

    def reenroll(self, name, host, params):
        xml = self.makeRequest(name, host, params, 'reenroll')
        return parseEnrollmentResult(xml)

    def makeRequest(self, name, host, params, method):
        data = { 'name' : name, 'client_ip' : host }
        for key, value in  params.iteritems():
            data[key] = value
        return self.connection_handler.sendMessage(method, data)

    def checkEnrollStatus(self):
        status = False
        http_status = self.connection_handler.checkEnrollStatus('enroll/status')
        if http_status == 200:
            status = True
        return status



"""

  function batchEnroll($fp, $readfunction) {
    $status = FALSE;
    error_log('batch enroll with readfunction: ' . $readfunction);
    $http_status = $this->connection_handler->sendBatched('enroll', $fp, $readfunction);
    if ($http_status == 204) {
      $status = TRUE;
    }
    return $status;
  }
  
"""

def main():
    identity_provider = IdentityServiceProvider('example.key.noencrypt.pem', 'example.crt.pem')
    authentication_result = identity_provider.preAuthenticate('guest', '10.10.1.100') 
    print authentication_result.result
    if (authentication_result.result.value != 'FAILURE'):
        for i in authentication_result.display_items:
            print i
    authentication_result2 = identity_provider.authenticate(authentication_result.name, '10.10.1.100', { 'passphrase' : 'guest' })
    print authentication_result2.result
    print identity_provider.checkEnrollStatus()

if __name__ == '__main__':
    main()

