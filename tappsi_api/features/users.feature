Feature: Users
 	# Scenario: Create User
  #   	Given I have the payload
	 #    """
	 #    {
	 #    	'username':'juniorgerdet',
	 #    	'email':'juniorgerdet@gmil.com',
	 #    	'password':'Test10',
	 #    	'last_name':'Junior',
	 #    	'first_name':'Gerdet',
	 #    	'role_alt':'Taxista'
	 #    }
	 #    """ 
		# When I send a POST request on "http://127.0.0.1:8000/api/v1/users/"
  #   	Then I get the responde code 201


 	Scenario: * Get taxi drivers available 
 		Given Register the app
 	    | name       |  client_id   						     | client_secret  																													|
 	    | tappsi_api |  Sa1VfLX3knpNnh6q92HVLOvloe4CmOQki65NceHU | 28hlYWNGkhCvRHuDN14d1Zpau0hSW0KabGDmyI9ENwwhZ4Zmu9VGpm6ymPTbowALrDjoJb2AlCiPPTQXV5ccqGMpZ1zpAebBgJAWH5LnUErCui02lqNbZsH5HRA3BXfy | 
 		
 		Given The following data on "User"
 	    | id | username     | password | email                  | first_name | last_name | role_alt   |
 	    | 1  | juniorgerdet | Test10   | juniorgerdet@gmail.com | Junior     | Gerdet    | taxi_drive | 
 	    | 2  | amartinez    | Test10   | amartinez@email.com    | Alexis     | Martinez  | client     | 
 	    | 3  | jlopez       | Test10   | jlopez@email.com       | Jesus      | Lopez     | taxi_drive | 
 	    | 4  | mherrera     | Test10   | mherrera@email.com     | Miguel     | Herrera   | taxi_drive | 
 	    | 5  | fhernandez   | Test10   | fhernandez@email.com   | Felix      | Hernandez | taxi_drive | 
 	    | 6  | sgarcia      | Test10   | sgarcia@email.com      | Samuel     | Gracia    | taxi_drive | 
 	    | 7  | dmartinez    | Test10   | dmartinez@email.com    | Diego      | Martinez  | taxi_drive | 
 	    | 8  | agerdet      | Test10   | agerdet@email.com      | Alex       | Gerdet    | taxi_drive | 
 	    | 9  | mcastillo    | Test10   | mcastillo@email.com    | Maria      | Castillo  | client     | 
 	    | 10 | jsilva       | Test10   | jsilva@email.com       | Jennifer   | Silva     | client     | 
 	    | 11 | sbarreto     | Test10   | sbarreto@email.com     | Sofia      | Barreto   | client     | 
 	    | 12 | jpaz         | Test10   | jpaz@email.com         | Jessica    | Paz       | client     | 
 	    | 13 | lhurtado     | Test10   | lhurtado@email.com     | Luisa      | Hurtado   | client     | 
		
		Given The following data on "Ride"
	 	    | taxi_drive_id | client_id | origin                  | destiny               | active |
	 	    | 8             | 12        | Cruz del perdon         | Casco central         | True   |
	 	    | 3             | 10        | Centro, carrera 12      | La salida de calabozo | False  |
	 	    | 1             | 9         | La hoyada, torre 5      | La california         | False  |
	 	    | 7             | 2 	    | Miranda, parque central | Hosp. El llanito      | False  |
	 	    | 4             | 11        | Los samanes             | Chaparral             | False  |
		
		# Given I authenticate as user "lhurtado"
		# When I send a GET request on "http://127.0.0.1:8000/api/v1/taxis/availables/"
  #   	Then i get the responde code 201
