# TestDockerCompose

Little project to work on micro services architecture :

## User

Microservice for user management : password hashing, permission management. Persist data in Postgres if in Prod, Sqlite if uat

## Token

Service acting as Authorization server in an OAuth2 scheme.

Cache Token in Redis if available, otherwise in a Python dict

Implicit flow. Create token by polling the user service to see if user exists and if he has enough right. Handle token expiry.

Each service can redirect to authorization url with corresponding client ID to get a token for the user

## Event

Service enabling Event Sourcing for Data consistency across services. 

Services can use the REST Api to spread event in the system.

When an event is published :
* Event data is LPUSH into a Published list for each subscriber for corresponding event
* A notification event is published in an atomic operation. It notifies everyone in the Subscribers list for the corresponding event that an event is available in Published List

A subscriber registers itself in a SUBSCRIBERS Set in Redis. When it receives notification :
  * Uses a RPOPLPUSH atomatic operation to get event data from the Published List into the Processing list of corresponding event. It insures a lot of instances of subscribers can exist and be notified but only one actually processes the event
  * Once completed, the event data is removed from Processing list. If an error occurs, it stays there and can be retried later
  
## Common

Common library for :
* Security : one dependency in order to implement OAuth2 in every services to go through Token service etc
* Token auth : a TokenAuth class, to pass to a requests.Session object. Handles the authorization. Get a token, caches it, put it in every Authorization header as Bearer, when it expires, refresh it
* Event subscriber : Extends the EventSubscriber class, implement the process_event() method, instanciate it with a Channel name and it will process the events automatically as they come
