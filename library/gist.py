#!/usr/bin/python
# -*- coding: utf-8 -*-

DOCUMENTATION = '''
---
module: gist
author: "Xavi S.B. @xsb"
short_description: create Github Gists
description:
  - Copy files to Github Gist
options:
  src:
    description:
      - File Path
    required: true
  public:
    description:
      - Is this Gist public or not?
    required: false
    default: false
    choices: [ "true", "false" ]
'''

EXAMPLES = '''
# Say hello
- gist: src=/etc/pacman.conf public=false
'''

RETURN = '''
url:
  description: gist url
  returned: success
  type: string
  sample: https://gist.github.com/anonymous/4124f3e2d5441c141796
'''

import urllib2
import json

def copy_to_gist(public, filename, content):
    data = {"public":public,'files':{filename:{'content':content}}}

    req = urllib2.Request('https://api.github.com/gists')
    req.add_header('Content-Type', 'application/json')
    response = urllib2.urlopen(req, json.dumps(data))
    return response

def main():

    module = AnsibleModule(
        argument_spec = dict(
            src    = dict(required=True, type='str'),
            public = dict(required=False, default='false', choices=['true', 'false']),
        ),
        supports_check_mode = False
    )

    src = module.params['src']
    filename = os.path.basename(src)
    public = module.params['public']
    f = open(os.path.expanduser(src))
    content = f.read()

    result = {}
    result['changed'] = False
    result['filename'] = filename

    try:
        response = copy_to_gist(public, filename, content)
        j = json.load(response)
        result['url'] = j['html_url']
        result['changed'] = True
    except Exception as e:
        module.fail_json(msg=str(e), changed=False)

    module.exit_json(**result)

# import module snippets
from ansible.module_utils.basic import *

if __name__ == '__main__':
    main()
