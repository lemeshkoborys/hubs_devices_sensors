# hubs_devices_sensors API 

**Technologies used:**
  1. Django REST Framework
  2. MongoDB
  
## API Info:

### Hubs:
__Allowed methods: GET, POST, PUT, PATCH, DELETE__
1. #### GET:   
     _/api/tools/hubs/_  
     _/api/tools/hubs/<<int:pk>>/_ - where <<int:pk>> - Hub ID  
     ##### Response data example:   
      **/api/tools/hubs/**
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
     **/api/tools/hubs/<<int:pk>>/ - where <<int:pk>> - Hub ID**
        
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

2. #### POST
    _/api/tools/hubs/create/_

    ##### Request data example:   
    ```JSON
    {
    "hub_title": "My Hub #1",
    "hub_serial_number": "ASKJASD2635WSG"
    }
    ```

    ##### Response data example:
    ```JSON
    {
        "id": 2,
        "hub_title": "My Hub #1",
        "hub_serial_number": "ASKJASD2635WSG",
        "owner": {
            "id": 1,
            "username": "admin",
            "email": "admin@example.com",
            "first_name": "Admin",
            "last_name": "Super"
        }
    }
    ```
3. #### PUT and PATCH
    _/api/tools/hubs/<<int:pk>>/update/_
    ##### Request data example for PUT method:
    ```JSON
    {
        "hub_title": "My Hub #2",
        "hub_serial_number": "ASKJASD2635KEK"
    }
    ```

    ##### Response data example for PUT method:
    ```JSON
    {
        "id": 2,
        "hub_title": "My Hub #2", // Changed
        "hub_serial_number": "ASKJASD2635KEK", //Changed
        "owner": {
            "id": 1,
            "username": "admin",
            "email": "admin@example.com",
            "first_name": "Admin",
            "last_name": "Super"
        }
    }
    ```

    ##### Request data example for PATCH method:
    ```JSON
    {
        "hub_title": "My Hub updated by PATCH method"
    }
    ```

    ##### Response data example for PATCH method:
    ```JSON
    {
        "id": 2,
        "hub_title": "My Hub updated by PATCH method", // Changed
        "hub_serial_number": "ASKJASD2635KEK",
        "owner": {
            "id": 1,
            "username": "admin",
            "email": "",
            "first_name": "",
            "last_name": ""
        }
    }
    ```
4. #### DELETE
    _/api/tools/hubs/<<int:pk>>/delete/_
    ##### Request data: _None_
    ##### Response data: _None_

### Devices

1. #### GET
