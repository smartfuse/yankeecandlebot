# yankeecandlebot
Bot that replies with a comment that links to the Yankee Candle store listing.

### Setup

Install Python3. Then create a virtualenv with `virtualenv env`. Enter it using `source env/bin/activate`. Install dependencies with `pip3 install -r dependencies.txt`.

### Running

Create a new Reddit app of type script. Open candle.py and add your Reddit credentials. Then run `python3 candle.py`.

### Usage

Whenever `🕯️(<candle scent name>)` is detected in a comment or post on r/NYYankees, this script will post a reply with the name, Yankee Candle link, and price of the candle (it uses the first search result on yankeecandle.com).
