## Project Configurations
There are two main manual steps/configurations to be done,
**Proxy IP** configuration and **Crawling Links** configuration.

### Crawling Links
Follow the following steps:
1. Navigate to the config file [here](../src/common/config/urls.py)
2. You will see links in the following structure
```python
Products = {
    'NewReleases': {
        'Sports & OutDoors': 'https://www.amazon.com/gp/new-releases/sporting-goods/',
        ......
    }
}
```
Now you can add new links in the similar fashion belongs to **New Releases** or 
If it belongs to some other major category you can add a new dictionary like this:
```python
Products = {
    'NewReleases': {
        'Sports & OutDoors': 'https://www.amazon.com/gp/new-releases/sporting-goods/',
        ......
    },
    'VideoGames': {
        'link1': 'blah blah blah',
        'link2': 'blah blah blah',
        ......
    }
}
```
Crawler will automatically crawl and scrap the pages indicated by the links.

### Proxy IP Configuration
For add new proxy ips to the ip rotator, follow the following steps:
1. Obtain proxy ips from any source like [Proxy Bonanza](https://proxybonanza.com/en)
2. Download the csv file (if you are in proxy bonanza)
3. Navigate to the [Rotator configuration file](../assets/Proxies.txt)
4. After opening the file, you will see something like this:
```bash
107.175.98.242	60099	61336	multitested	4Lpgj5R8
107.175.98.205	60099	61336	multitested	4Lpgj5R8
107.175.98.232	60099	61336	multitested	4Lpgj5R8
107.175.98.218	60099	61336	multitested	4Lpgj5R8
107.175.98.227	60099	61336	multitested	4Lpgj5R8

# here the first number indicates the proxy ip
# the 2nd number indicates the http port
# the 3rd number indicated the https port
# the 4th place indicates the user name
# the 5th place indicates the password
```
5. Copy and paste the ips in similar fashion, rotator will automatically
use them
