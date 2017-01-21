# too-hot

### API Documentation



`GET /api/temps`
Description: Retrieve all temperature records currently stored in the database.
Sample response:
```
{
  "temps": [
    {
      "readingID": 1,
      "sensorID": 2,
      "temp": 32,
      "timestamp": "2017-01-20 23:14:44"
    },
    {
      "readingID": 2,
      "sensorID": 2,
      "temp": 32,
      "timestamp": "2017-01-20 23:15:26"
    },
    {
      "readingID": 3,
      "sensorID": 3,
      "temp": 32,
      "timestamp": "2017-01-20 23:16:58"
    }
  ]
}
```

`POST /api/temps`
Description: Add a new temperature record into the database
Input parameters:
 - temp - temperature recorded by sensor
 - sensorID - integer uniquely identifying the sensor

Sample input:
```
{
	"temp":32,
	"sensorID":2
}
```
Sample response:
```
{
  "reading": {
    "sensorID": 2,
    "temp": 32
  }
}
```