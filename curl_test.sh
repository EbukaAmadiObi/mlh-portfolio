#!/usr/bin/bash

URL="http://127.0.0.1:5000/api/timeline_post"

ID=$RANDOM
NAME="TestUser$ID"
EMAIL="user$ID@test.com"
CONTENT="Test post by user#$ID"

echo "Sending POST for TestUser$ID, user$ID@test.com saying: Test post by user#$ID"
POST_RESPONSE=$(curl -X POST $URL -d "name=$NAME&email=$EMAIL&content=$CONTENT")

echo "Received POST response: $POST_RESPONSE"

echo "Sending GET to check database..."
GET_RESPONSE=$(curl $URL)

if echo "$GET_RESPONSE" | grep -q "$CONTENT"; then
        echo "Post was added successfuly"
else
        echo "Post was not found in GET response!"
        exit 1
fi