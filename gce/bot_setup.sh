#! /bin/bash
# Copyright 2015 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

echo "Start PY"
# preparation: Kill zombie python. It has to add kill conditions if adding new char
kill -9 $(ps aux | grep -e dudleybot.py| awk '{ print $2 }')
kill -9 $(ps aux | grep -e petuniabot.py| awk '{ print $2 }')
# Install app dependencies
virtualenv /opt/app/env
/opt/app/env/bin/pip install -r /opt/app/requirements.txt
source /opt/app/env/bin/activate
pip install slackclient
pip install wit
cd /opt/app
ls -al
/opt/app/env/bin/python /opt/app/main.py

echo "end script"
