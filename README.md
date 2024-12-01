# furgopi-client

# Make it work in the Rapsberry Pi

## Activate the GPIO supports

As we're using GPIO connections, some require explicit set up. As a rule of thumb, just run `sudo raspi-config`, go to the *Interface Options* options and activate them there.

### 1-Wire communication

Needed for the temperature sensor, allows having several sensors in the same pin disposal. All of them have a different address.

### I2C communication

Needed for the GPS sensor, allows a kinda serial communication already supported by the Rapsbery Pi on the related pins

## Install Python (Debian)

```
sudo apt update
sudo apt upgrade
sudo apt install python
```

## Install Poetry

Download and install through the official installer.
```
curl -sSL https://install.python-poetry.org | python
```

Add poetry to the PATH in your `.bashrc` file
```
nano .bashrc
```
... and add the following at the end of the file:
```
export PATH="/home/[username]/.local/bin:$PATH"
```
save and exit.

Apply the new environment set up
```
source .bashrc
```

Make sure that Poetry is up and running
```
poetry --version
```

## Install project dependencies

```
make init
```

### Run it

```
make run
```

This is a shortcut that runs the main script set up in Poetry, so it would be like
```
poetry run main
```

Which would be also the same as the following without the environment management from Poetry
```
python

