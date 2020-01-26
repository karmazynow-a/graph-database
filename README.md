# POC for graph database

Uni project made with Python + Flask + Graphenedb deployed on Heroku.

For database connection: neo4jrestclient

In the app, you can search for the shortest path from one bus stop to another based on travel time. Also, you are able to add own bus stops and connections, modify and delete them - basically crud.

Before running locally remember to set environment variable GRAPHENEDB_URL to your Graphenedb's HTTP REST connection string.

More info in the documentation.
