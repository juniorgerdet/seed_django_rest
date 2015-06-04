Feature: Users
 	Scenario: Create User
    	Given I have the payload
	    """
	    {
	    	'username':'juniorgerdet',
	    	'email':'juniorgerdet@gmil.com',
	    	'password':'Test10',
	    	'last_name':'Junior',
	    	'first_name':'Gerdet',
	    	'role_alt':'Taxista'
	    }
	    """ 
		When I send a POST request on "http://127.0.0.1:8000/users"
    	Then I get the responde code 201


