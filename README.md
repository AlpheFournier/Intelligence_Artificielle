# The Hummus AI

## Test server and setup

A test server is available on this [repository](https://github.com/Succo/twilight)

In order to start it, install `go`, compile the project and run it.

### On MacOS

```bash
$> cd ~
$> brew install go
$> git clone https://github.com/Succo/twilight
$> cd twilight-master
$> go build -o "Binary_file"
$> ./Binary_file -rand
```

### On Windows

- Install go from https://golang.org/doc/install
- Run the following command lines

```bash
$> cd \
$> cd Go\src
$> mkdir twilight
$> cd twilight
$> git clone https://github.com/Succo/twilight
$> go build
$> twilight -rand
```

- If you get an import error during the build about `launch.net\xmlpath`, install bazaar from [here](http://wiki.bazaar.canonical.com/WindowsDownloads), run the command ```go get launchpad.net/xmlpath``` and move this newly created folder (probably located in `Go\src\src`) to `Go\src\vendor`. Then, try `go build` again.

### For all

The server should launch on `localhost:8080`

You can then start the dummy players from The Hummus AI with the following command.

```bash
$> cd /path/to/Hummus
$> python main.py
```

## Fonction de coût

- Taille maximale du groupe adverse
- Tailles de l'adversaire
- Distance en l'adversaire et les humains
- Distances entre nos positions et celles des humains et des adversaires et tailles
- Conversions possibles en n tours pour nous et l'adversaire
