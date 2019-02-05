# hubs_devices_sensors API 

**Technologies used:**
  1. Django REST Framework
  2. MongoDB
  
## API Info:

### Hubs:
__Allowed methods: GET, POST, PUT, PATCH, DELETE__
  1. ### GET:   
     _/api/tools/hubs/_  
     _/api/tools/hubs/<<int:pk>>/_ - where <<int:pk>> - Hub ID  
     #### Response data example:   
     ##### /api/tools/hubs/
     ```JSON
     [
      {
          "id": 1,
          "hub_title": "Admin Hub #1",
          "hub_serial_number": "XXZZVVDD2233",
          "owner": {
              "id": 1,
              "username": "admin",
              "email": "admin@example.com",
              "first_name": "Admin",
              "last_name": "Super"
          }
      }
     ]
     ```
     ##### /api/tools/hubs/<<int:pk>>/ - where <<int:pk>> - Hub ID 
        
     ```JSON
     [
      {
          "id": 1,
          "hub_title": "Admin Hub #1",
          "hub_serial_number": "XXZZVVDD2233",
          "owner": {
              "id": 1,
              "username": "admin",
              "email": "admin@example.com",
              "first_name": "Admin",
              "last_name": "Super"
          }
      }
     ]
     ```
  2. ### POST:     
    /api/tools/hubs/create/    
    __Request data example:__ 
