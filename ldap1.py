import ldap
import getpass
import sys

def adldap():
    name_user = raw_input("Write the name of user: " )
    password_user = raw_input("Write the password of user: " )
    con = ldap.initialize('ldap://ldap.forumsys.com/')
    binddn = "cn=read-only-admin,dc=example,dc=com"
    pw = "password"
    ldap_base = "dc=example,dc=com"
    con.protocol_version = ldap.VERSION3
    searchFilter = "(&(uid="+name_user+"))"
    searchAttribute = ["uid", "ou", "cn", "password"]
    searchScope = ldap.SCOPE_SUBTREE

    try:
        con.simple_bind_s(binddn, pw)
    except ldap.INVALID_CREDENTIALS:
        print "Your username or password is incorrect."
        sys.exit(0)
    except ldap.LDAPError, e:
        if type(e.message) == dict and e.message.has_key('desc'):
            print e.message['desc']
        else: 
            print e
        sys.exit(0)
    try:
        ldap_result_id = con.search(ldap_base, ldap.SCOPE_SUBTREE, searchFilter, searchAttribute)
        result = con.search_s(ldap_base, ldap.SCOPE_SUBTREE, searchFilter)
        con.bind_s(result[0][0], password_user)
        print(result)
        mail = result[0][1]["mail"][0].decode("utf-8")
        name = result[0][1]["cn"][0].decode("utf-8")
        return ["succeeded!", mail, name]

    except ldap.LDAPError:
        return ["failed"]
    con.unbind_s()
        
adldap()
        
