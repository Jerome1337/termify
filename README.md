# Termify

![](https://img.shields.io/github/release/jerome1337/termify.svg)
![](https://api.travis-ci.org/Jerome1337/termify.svg?branch=master)
![](https://img.shields.io/github/downloads/jerome1337/termify/total.svg)
![](https://img.shields.io/github/license/jerome1337/termify.svg)

Terminal Spotify player written in Python :snake:

Manage your Spotify streaming directly from your terminal regardless of streaming output
(phones, web player, home assistants...) No need to download and install Spotify client anymore.

## Requirements

* Linux based OS
* Spotify account
* Terminal emulator

## Usage

Download the latest [release](https://github.com/Jerome1337/termify/releases) then use it as a classic script

```bash
$ ./termify
```

## Development

### Requirements

* Python 3
* Pip
* Spotify account
* Spotify app (used for API credentials)

**Optionnal**

* Docker
* Docker-compose

Create a Spotify new application by following this [link](https://developer.spotify.com/dashboard/applications) then 
replace `client_id`, `client_secret` and `redirect_url` variables by yours inside `authentication.py`.

```bash
$ pip require -r requirements.txt --upgrade
$ python termify.py

# Or using Docker
$ docker-compose up -d
$ docker-compose exec termify python termify.py
```

## Compatibility

Currently Termify is only supported on Linux based OS.

All the development has been done on Arch Linux core.

## Todo

* [ ] Manage token refresh
* [ ] Adapt GUI when terminal size change
* [ ] Select streaming output
* [ ] Add track to a given playlist
* [ ] Save track to Liked Songs
