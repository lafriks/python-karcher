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
  -d, --debug                     Enable debug mode.
  -o, --output [json|json_pretty]
                                  Output format. Default: "json"
  -r, --region [eu|us|cn]         Region of the server to query. Default: "eu"
  --help                          Show this message and exit.

Commands:
  device-properties  Get device properties.
  devices            List all devices.
  login              Get user session tokens.
  urls               Get region information.
```

### From code

```python
from karcher.karcher import KarcherHome

kh = await KarcherHome.create()
await kh.login("user@email", "password")
devices = await hk.get_devices()
```

## License

Distributed under the MIT License. See `LICENSE` for more information.
