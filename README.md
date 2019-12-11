# POC for graph database

Uni project made with Python + Flask + Graphenedb deployed on heroku.

For database connection: neo4jrestclient

In app you can search for shortest path from one bus stop to other based on travel time.
Also you are able to add own bus stops and connections, modify and delete them - basically crud.

Before running locally remember to set environment variable GRAPHENEDB_URL to your graphenedb's HTTP REST connection string.

More info in documentation.
