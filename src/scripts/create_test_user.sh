if ! command -v curl &> /dev/null
then
    echo "curl could not be found"
    exit
fi

curl -X 'POST' \
  'http://localhost:8000/users/' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "username": "dash",
  "email": "ds@sd.com",
  "password": "password"
}'