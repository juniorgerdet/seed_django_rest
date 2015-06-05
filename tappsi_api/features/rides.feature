Feature: Rides

 	Scenario: Register ride
 		Given Register the app
 	    | name       |  client_id   						     | client_secret  																													|
 	    | tappsi_api |  Sa1VfLX3knpNnh6q92HVLOvloe4CmOQki65NceHU | 28hlYWNGkhCvRHuDN14d1Zpau0hSW0KabGDmyI9ENwwhZ4Zmu9VGpm6ymPTbowALrDjoJb2AlCiPPTQXV5ccqGMpZ1zpAebBgJAWH5LnUErCui02lqNbZsH5HRA3BXfy | 
 		
 		
 		Given The following data on "User"
 	    | id | username     | password | email                  | first_name | last_name | role_alt   |
 	    | 1  | juniorgerdet | Test10   | juniorgerdet@gmail.com | Junior     | Gerdet    | taxi_drive | 
 	    | 2  | amartinez    | Test10   | amartinez@email.com    | Alexis     | Martinez  | client     | 
		
		Given I authenticate as user "juniorgerdet"
		
		Given I have the payload
	    """
	    {
	    	'client': 2,
	    	'origin':'juniorgerdet@gmil.com',
	    	'destiny':'Test10',
	    	'active': 1
	    }
	    """ 
		When I send a POST request on "http://127.0.0.1:8000/api/v1/rides/"
    	Then i get the responde code 201
