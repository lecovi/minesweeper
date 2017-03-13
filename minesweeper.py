#! /usr/bin/env python
"""
    minesweeper.minesweeper.py
    ~~~~~~~~~~~~~~~~~~~~~~~
    
    Description
    
    :copyright: (c) 2017 by LeCoVi.
    :author: Leandro E. Colombo Viña <colomboleandro at bitson.com.ar>.
    :license: AGPL, see LICENSE for more details.
"""
# Standard lib imports
# Third-party imports
# LeCoVi imports
from app import app

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8000)
