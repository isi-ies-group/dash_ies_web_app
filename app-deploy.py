# -*- coding: utf-8 -*-
"""
@author: GuillermoMatas
"""

from waitress import serve
from dash_app import server


serve(server, host='0.0.0.0', port=80)