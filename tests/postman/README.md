# Postman Tests

## How to Use

### Postman Client

To import the collection into your Postman client, you can click on the "Import" button in the top left of the application and then drag and drop the JSON file(s_ into the popup menu.

At the moment you can right click and select "Run Folder" for these following folders and it will run all of the routes in the folder selected so you can easily test any changes to the routes.

### Command Line

To run from the command line, you can use Newman which is installed in the Docker container.  For example:

```
docker exec -it milestones_api newman run /app/tests/postman/Milestones_Users.postman_collection.json
```

...produces output like:
```
..............
→ Bulk Update Services
  PUT http://127.0.0.1/v1/users/12e5c13d798c97ee378eb1415b28dfd5d0719a9807178dedbc9659f9/services [200 OK, 1.04kB, 49ms]
  ✓  Successful PUT request

┌─────────────────────────┬──────────────────┬──────────────────┐
│                         │         executed │           failed │
├─────────────────────────┼──────────────────┼──────────────────┤
│              iterations │                1 │                0 │
├─────────────────────────┼──────────────────┼──────────────────┤
│                requests │               10 │                0 │
├─────────────────────────┼──────────────────┼──────────────────┤
│            test-scripts │               20 │                0 │
├─────────────────────────┼──────────────────┼──────────────────┤
│      prerequest-scripts │               14 │                0 │
├─────────────────────────┼──────────────────┼──────────────────┤
│              assertions │               17 │                0 │
├─────────────────────────┴──────────────────┴──────────────────┤
│ total run duration: 418ms                                     │
├───────────────────────────────────────────────────────────────┤
│ total data received: 3.79kB (approx)                          │
├───────────────────────────────────────────────────────────────┤
│ average response time: 22ms [min: 3ms, max: 50ms, s.d.: 19ms] │
└───────────────────────────────────────────────────────────────┘
```


## Milestones_in_order.postman_collection.json

Currently the `Milestones_in_order.postman_collection.json` file has multiple folders in it that will eventually be separated for easier upkeep.

- Milestones_in_order
     - v1
        - clients (running this folder will create a client and two client_users, it will get them all and individually, update them both, and then delete everything and check that it has been deleted)
        - placeholder
            - programs (running this folder will create a client, a client_user and a program associated for the client, it will get the program, update it, and then delete the program, the client_user, and the client)
            - budgets (running this folder will create a client and then it will create a static budget, parent budget, and sub budget, it will then run full CRUD checks on all of the budgets and also delete the client in the end)
            - events (running this folder will create a client, client_user, program, program_event and a sub event. It will GET the events and update them and then delete them along with everything else created)
            - admins (running this folder will create a client, client_user, program, and then a program_admin, it will the GET the admin, update the permissions, and then delete them along with everything else)
            - WIP (Work In Progress, has the other routes in it that don't have tests complete yet)

## Milestones_Users.postman_collection.json

This collection is a series of sequential tests regarding users.  In essence:

- Get all users, should 404
- Creates a test user, should succeed
- Gets users again, should get the new user in list of users
- Gets the test user, should get the test user back
- Updates the user, should succeed
- Creates a 2nd service for the test user, should succeed
- Gets the 2nd service for the test user, should get the service back
- Updates the user service, should succeed
- Does a bulk update of services