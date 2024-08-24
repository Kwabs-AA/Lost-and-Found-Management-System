#!/bin/bash
#!/bin/bash

pip3 install -r requirements.txt  # Use pip3 instead of pip
python3 manage.py collectstatic --noinput  # Use python3 instead of python
python3 manage.py migrate  # Use python3 instead of python
