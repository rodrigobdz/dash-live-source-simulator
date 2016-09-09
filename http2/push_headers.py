"""
  HTTP/2 Push Helper

  Given a requested resource named 'n', 
  a list with the next 'k' resources to be pushed is created and 
  added to the current response headers.

  Example: 
    Given k = 3, meaning that we want the server to push the next 3 segments.

    Client requests http://www.example.com/1.mp4
    Following resources will be pushed
      /2.mp4
      /3.mp4
      /4.mp4

    The client will receive in total the following resources
      /1.mp4
      /2.mp4
      /3.mp4
      /4.mp4

  Assumptions:
    The resources to be pushed are named sequentially.

  Note:
    Intended for use with an HTTP/2 Server.
    As of september 2016 simple_server from wsgiref does not support HTTP/2.
    Thus, this helper is not compatible with it.
"""
#
# Rodrigo Bermudez Schettino
#

from os.path import splitext

def add_push_headers(headers, url, k=3):
    # Get base url
    # Trim url from the beginning until last ocurrence of /, including last / found
    # Example:
    # Given url = '/1/2/3/4/5.ext'
    # Base url = '/1/2/3/4/'
    path_parts = url.split('/')
    base_url = '/'.join(path_parts[:-1])+'/'

    # Analyze requested resource's name and extension
    requested_resource = splitext(path_parts[-1])[0]
    
    try:
        requested_resource_number = int(requested_resource)
    except ValueError:
        print 'HTTP/2 push helper ERROR:'
        print requested_resource + ' cannot be converted to int.'
        print 'Nothing will be pushed for this request.'
        return 
    
    ext = splitext(path_parts[-1])[1]
    # Build push headers for the next k segments
    push_headers = ''
    for i in range(k):
        # Add 1 additionally because range starts at 0
        next_resource = requested_resource_number + i + 1
        push_headers += '<' + base_url + str(next_resource) + ext  + '>;rel=preload'
        if i < k-1:
            push_headers += ', '

    # Add push headers to the current headers
    headers['Link'] = push_headers

