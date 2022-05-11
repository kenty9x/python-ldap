import ldap
import getpass
import sys

def adldap():
    name_user = raw_input("Write the name of user: " )
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
        result_set = []
        while 1:
            result_type, result_data = con.result(ldap_result_id, 0)
            if (result_data == []):
                break
            else:
                if result_type == ldap.RES_SEARCH_ENTRY:
                    result_set.append(result_data)
        print result_set
    except ldap.LDAPError, e:
        print e
    con.unbind_s()
        
adldap()
        
