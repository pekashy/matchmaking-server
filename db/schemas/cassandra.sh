#!/bin/sh

# Wait for Cassandra to start up
while ! cqlsh open-matches-db -e 'describe cluster' ; do
    sleep 1
    echo "Waiting for cassandra...";
done

echo "Cassandra has started"

cqlsh open-matches-db --file '/schemas/matches.cql'

echo "Cassandra has been initialised"

tail -f /dev/null
