# Identity4python

**Python library for interacting with the ufpIdentity authentication system.**

Read the Getting Started section of the ufpIdentity [Integration Document](http://www.ufp.com/identity/integration.html#getting_started)

Example usage:

     identity_provider = IdentityServiceProvider('example.key.noencrypt.pem', 'example.crt.pem')
     authentication_result = identity_provider.preAuthenticate('guest', '10.10.1.100') 
     print authentication_result.result
     if (authentication_result.result.value != 'FAILURE'):
         for i in authentication_result.display_items:
             print i
     authentication_result2 = identity_provider.authenticate(authentication_result.name, '10.10.1.100', { 'passphrase' : 'guest' })
     print authentication_result2.result
