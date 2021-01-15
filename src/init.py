# -*- coding: UTF-8 -*-
import sys

import settings

temp_file = sys.argv[-1]
if temp_file.endswith('.bat'):
    my_settings = settings.load(*sys.argv[1:-1])
    if my_settings:
        with open(temp_file, 'w+') as f:
            f.write(my_settings)



