# Blockdemo

A 150 lines python 3.6 blockchain-node implementation.


## Run Locally 

* Clone repo
* Download and install Python 3.6
* Install dependencies
  * ``` pip install --no-cache-dir -r requirements.txt ```

## Run on Docker

* Clone repo
* Build docker image from dockerfile
  * ``` docker build -t blockdemo . ```
* Run a container publishing any port to container's 5000 port
  * ``` docker run -d -p 666:5000 --name blockdemo blockdemo ```
  
## API 

The postman collection in the repo contains all the methods in order to iteract with the live version
[Postman Published Collection](https://documenter.getpostman.com/view/560342/blackcoin/RW1XKM32#25df755a-a0a4-4f88-bc7f-23f7f9b77f05)

## If running locally is not your thing you play with the live version pointing your requests to ``` 64.137.224.12:666 ```
``` 
curl --request GET \
 --url http://64.137.224.12:666/blocks 
```
```
curl --request POST 
  --url http://64.137.224.12:666/txion \
  --header 'Content-Type: application/json' \
  --data '{
	"from": "dude",
	"to": "duderino",
	"amount": 4
}' 
```
``` 
curl --request GET \
  --url http://64.137.224.12:666/mine 
```

## Future Work
* Implement Multi node
* Implement Wallet
