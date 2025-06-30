FROM mongo:6.0

CMD bash -c "\
  mongod --replSet rs0 --bind_ip_all & \
  sleep 5 && \
  mongosh --eval 'rs.initiate({_id: \"rs0\", members: [{ _id: 0, host: \"localhost:27017\" }]})' && \
  fg"