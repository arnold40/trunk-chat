#!/usr/bin/env bash

start_time=$(date +%s)

for i in {1..100}; do
  curl -X POST http://trunk-chat-dev.eu-west-1.elasticbeanstalk.com/api/users/ \
       -u {username}:{password} \
       -H "Content-Type: application/json" \
       -d '{}' &
done

wait

end_time=$(date +%s)
elapsed=$((end_time - start_time))

echo "Script took $elapsed seconds to run."
