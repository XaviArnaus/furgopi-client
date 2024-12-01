# furgopi-client

# Make it work in the Rapsberry Pi

## Activate the GCPIO one drive support

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
export PATH="/home/xavier/.local/bin:$PATH"
```
save and exit.

Apply the new environment set up
```
source .bashrc
```

Make sure that poetry is up and running
```
poetry --version
```

## Install project dependencies

```
make init
```


