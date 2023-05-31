# Postman Tests

## Milestones_in_order.postman_collection.json

Currently the `Milestones_in_order.postman_collection.json` file has multiple folders in it that will eventually be separated for easier upkeep.

To import the collection into your postman you can click on the "Import" button in the top left of the application and then drag and drop the `Milestones_in_order.postman_collection.json` file into the popup menu.

At the moment you can right click and select "Run Folder" for these following folders and it will run all of the routes in the folder selected so you can easily test any changes to the routes.

- Milestones_in_order
     - v1
        - clients (running this folder will create a client and two client_users, it will get them all and individually, update them both, and then delete everything and check that it has been deleted)
        - placeholder
            - programs (running this folder will create a client, a client_user and a program associated for the client, it will get the program, update it, and then delete the program, the client_user, and the client)
            - budgets (running this folder will create a client and then it will create a static budget, parent budget, and sub budget, it will then run full CRUD checks on all of the budgets and also delete the client in the end)

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