# LIFEDATA Sample View

You can use this directory to create your own custom view of your sample
data. This is useful if you want to present your samples in a specific way to
the annotators or have a media format that is not supported by the LIFEDATA
framework out-of-the-box.

## Getting started

Change to the the sampleview directory (the one containing this README) and
run:

```bash
cd lifedata_api/sampleview/
yarn install    # Install npm dependencies
yarn run start  # Start the Webpack dev server
```

Configure in `lifedata_api.py`:

```python
from lifedata.lifedata_api.sample_view import SampleView

def get_sample_view():
    return SampleView(
        url="http://localhost:3010",
        # Optional arguments for the frontend component. Use this to provide
        # static configuration.
        args={
            "brandName": "my-widget-forge",
        },
    )
```

Then run the lifedata dev server as you would always do in your project root:

```bash
lifedata start --dev
```

You can now see the component in use when opening the dev server in the
browser at [`http://localhost:3000`](http://localhost:3000).
