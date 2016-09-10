"""
  HTTP/2 Server k-push Helper

  For a requested resource 'n', 
  a list with the next 'k' resources to be pushed is created and 
  added to the current response headers.

  Assumptions:
    The resources to be pushed are named sequentially.

  Example: 
    For k = 3, meaning that we want the server to push the next 3 resources after n.

    Client requests http://www.example.com/1.mp4
    Following resources will be pushed
      http://www.example.com/2.mp4
      http://www.example.com/3.mp4
      http://www.example.com/4.mp4

    The client will receive in total the following resources
      http://www.example.com/1.mp4
      http://www.example.com/2.mp4
      http://www.example.com/3.mp4
      http://www.example.com/4.mp4

  Note:
    Intended for use with an HTTP/2 Server.
    As of september 2016 simple_server from wsgiref does not support HTTP/2.
    Thus, this helper is not compatible with it.

    The headers set by this helper signalize the server which resources should be 
    pushed. This alone does not implement the push itself.
"""
#
# Rodrigo Bermudez Schettino
#

from os.path import splitext

def add_push_headers(headers, url, k=3):
    """
    Adds the next 'k' resources to be pushed to the response headers.
    This headers are then processed by the server in order to send
    the corresponding resources.

    Parameters:
      headers
        Response headers
      url
        Client's request url
      k
        Number of segments to be pushed along with the requested resource
    """
    
    # Split url into main components
    processed_url = process_url(url)
    
    try:
        requested_resource_number = int(processed_url['resource_name'])
    except ValueError:
        # Push different resources at the beginning of a streaming session
        if processed_url['resource_name'] == 'Manifest':
            # headers['Link'] = format_header_link( processed_url['base_url'], )
            return

        # Log error
        print '\nHTTP/2 push helper ERROR:'
        print processed_url['resource_name'] + ' cannot be converted to int.'
        print 'Nothing will be pushed for this request.\n'
        return 
    
    
    # Build push headers for the next k segments
    push_headers = ''
    for i in range(k):
        # Add 1 additionally because range starts at 0
        next_resource = requested_resource_number + i + 1
        # Add extension to resource name
        next_resource = str(next_resource) + processed_url['ext']
        push_headers += format_header_link( processed_url['base_url'], next_resource )
        
        # Add comma between push resources
        if i < k-1:
            push_headers += ', '

    # Add push headers to the current headers
    headers['Link'] = push_headers


def process_url(url):
    """
    Process url and return its main parts
      
    Parameters:
      url

    Returns:
      A dictionary with the following attributes

      base_url
        Trimmed url from the beginning until last ocurrence of /, including last / found
      resource_name
        Name of requested resource without extension
      ext
        Extension of requested resource

    Example:
      url = '/1/2/3/4/5.ext'

      base_url           = '/1/2/3/4/'
      resource_name = '5'
      ext                = '.ext'
    """
    path_parts = url.split('/')

    processed_url = {}  
    processed_url['resource_name'] = splitext(path_parts[-1])[0]
    processed_url['base_url'] = '/'.join(path_parts[:-1])+'/'
    processed_url['ext'] = splitext(path_parts[-1])[1]

    return processed_url


def format_header_link(base_url, resource):
    """
    Format push resource for headers
    """
        return '<' + base_url + resource + '>; rel=preload'
