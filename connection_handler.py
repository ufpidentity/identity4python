import resolver
import urllib
import urllib2
import urllib2_ssl

def make_error(name, errorcode):
  xml = '<authentication_context><name>{0}</name><result xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:type="defaultResult" code="{1}" confidence="0.0" level="0" message="Identity Service Failure : {1}">FAILURE</result></authentication_context>'.format(name, errorcode)
  return xml

class IdentityConnectionHandler:
  def __init__(self, key_file, cert_file, ca_certs='truststore.pem'):
      self.opener = urllib2.build_opener(urllib2_ssl.HTTPSHandler(key_file=key_file, cert_file=cert_file, ca_certs=ca_certs))

  def sendMessage(self, path, queryparams):
      xml = None
      url = '{0}/{1}?{2}'.format(resolver.getHost(), path, urllib.urlencode(queryparams))
      try:
        connection = self.opener.open(url)
        print connection.getcode()
        if connection.getcode() == 200:
          xml = connection.read()
        else:
          xml = make_error(queryparams['name'], connection.getcode())
      except urllib2.HTTPError as error:
        xml = make_error(queryparams['name'], error.code)
      return xml

  def checkEnrollStatus(self, path):
    url = '{0}/{1}'.format(resolver.getHost(), path)
    try:
      connection = self.opener.open(url)
      return connection.getcode()
    except urllib2.HTTPError as error:
      return 0
    

"""
  function sendBatched($path, $fp, $readfunction) {
    $url = $this->resolver->getHost() . "/" . $path;
    curl_setopt($this->curl_handle, CURLOPT_URL, $url);
    curl_setopt($this->curl_handle, CURLOPT_HTTPHEADER, array('Content-Type: application/octet-stream'));
    curl_setopt($this->curl_handle, CURLOPT_READFUNCTION, $readfunction);
    curl_setopt($this->curl_handle, CURLOPT_CUSTOMREQUEST, 'POST');
    curl_setopt($this->curl_handle, CURLOPT_INFILE, $fp);
    curl_setopt($this->curl_handle, CURLOPT_UPLOAD, TRUE);
    $message = curl_exec($this->curl_handle);
    $http_code = curl_getinfo($this->curl_handle, CURLINFO_HTTP_CODE);
    error_log('http_code: ' . $http_code);
    return $http_code;
  }

}
"""
def main():
    connection_handler = IdentityConnectionHandler('example.key.noencrypt.pem', 'example.crt.pem')
    xml = connection_handler.sendMessage('preauthenticate', { 'name' : 'guest', 'client_ip' : '192.168.2.105' })
    print xml

if __name__ == '__main__':
    main()
