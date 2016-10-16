# DASH-IF DASH Live Source Simulator

This software is intended as a reference that can be customized to provide a reference
for several use cases for live DASH distribution.

It uses VoD content in live profile as a start, and modifies the MPD and the media
segments to provide a live source. All modifications are made on the fly, which allows
for many different options as well as accurate timing testing.

The tool is written in Python and runs as an Apache mod_python plugin or using mod_wsgi.



## Modifications

#### Features

- Waiting for segment availability
- HTTP/2 Server Push
- Accept representations with subsecond segments



### HTTP/2 Parameters

In this section we will go through the parameters available in DLS customize HTTP/2.

#### Requirements

Currently the modifications to support HTTP/2 only work with mod_wsgi. 

The following variables must be set to `True` to enable HTTP/2:

- `WAIT_FOR_SEGMENT_AVAILABILITY` in dashlivesim/dashlib/dash_proxy.py
- `ENABLE_HTTP2` in dashlivesim/mod_wsgi/mod_dashlivesim.py

#### Parameters

- The default number of segments to push additionally is 3 and this is set as the default parameter k for the function  `add_push_headers(headers, url, k=3)` in http2/push_headers.py