# Waiting List Service

I spent around 8 hours on the test.

## Presentation

The project is split into two main parts, the Postgres database and the service itself.

### Structure

```text
WaitingList/
├── waiting_list_database/
│   ├── src/
│   │   ├── data/
│   │   └── init.sql
│   ├── Dockerfile
├── waiting_list_service/
│   ├── app/
│   │   ├── managers/
│   │   ├── routers/
│   │   ├── schemas/
│   │   ├── utils/
│   │   └── main
│   ├── tests/
│   ├── Dockerfile
│   └── requirements.txt
├── .env
├── compose.yml
└── README.md
```

To run the project, simply execute the following code and head to [this link](http://0.0.0.0:8000/docs)
```bash
docker compose up
```

## Design decisions

The FastAPI app is split into two routers, one for the organizers and one for the users, potentially opening the door
to authentification flows.

Set PYTHONUNBUFFERED to 1 so that I didn't have to focus on the logging.


The logic behind the waiting list is the key part of the project. Multiple assumptions had to be done :
- Provided inventory table has been altered adding a `waiting_list_open` boolean
- Users can't join the waiting list while there are still tickets available
- Once an off/rep gets to 0 available tickets, the waiting list stays open even if new stocks are added
- Users can leave the waiting list. If they join again, they are placed last
- Users can have 3 status in the waiting list : `waiting` (the user is ... waiting), `ready` (the user can buy tickets), `left` (the user has left the waiting list (either after buying tickets or simply leaving)

## Docker Compose

While in a normal environment, I would not include the `.env` file in the project, it has been left in the repository on purpose.

## Possible improvements

### Testing

Testing is clearly very limited. The app allow the mock of the DB for proper tests.
Tests would include (but not limited to) :
- Joining a waiting list that hasn't open yet
- Joining a waiting list twice
- Joining a waiting list that doesn't exist
- Joining a waiting list with 0 tickets wanted
- Joining a waiting list with more tickets wanted than allowed by the offer
- Leaving a list that a user is not part of
- Leaving a list that doesn't exist
- Leaving a list that isn't open yet
- Leaving a list that a user has already left
- View status for a user that doesn't exist
- View status for and event that doesn't exist
- Add negative stock
- Add stock to an event that doesn't exist
- Add available stock and exceeding total stock 
- Remove more stock than available
- Remove stock to an event that doesn't exist


Same idea goes for buying tickets and filtering.

During development, I used `quicktest.py` to send requests to the app.

### Known issue

There seems to have an issue when buying ticket : the leave_list triggers an update of the waiting list.

This should append because even if a user leaves the list after buying their tickets, the bought tickets are supposed to be removed from the stock hence changing nothing for the other users. 
