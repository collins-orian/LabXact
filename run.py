#!/usr/bin/env python3
"""This file runs the application"""

from labxact import create_app

app = create_app()


if __name__ == "__main__":
    app.run(debug=True)
