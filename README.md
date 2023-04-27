# Kärcher Home Robots client

Python library and cli to authorize into Karcher Home Robots account and fetch device information.

## Usage

To download `karcher-home` cli run:

```sh
pip3 install karcher-home
```

### From console

```console
Usage: karcher-home [OPTIONS] COMMAND [ARGS]...

  Tool for connectiong and getting information from Kärcher Home Robots.

Options:
  -d, --debug
  -o, --output [json|json_pretty]
  -r, --region [eu|us|cn]         Region of the server to query. Default: 'eu'
  --help                          Show this message and exit.

Commands:
  devices   List all devices.
  get-urls  Get region information.
  login     Get user session tokens.
```

### From code

```python
from karcher.karcher import KarcherHome

kh = KarcherHome()
kh.login("user@email", "password")
devices = hk.get_devices()
```

## License

Distributed under the MIT License. See `LICENSE` for more information.
