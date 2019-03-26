#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import os.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))
import qencode
import time
import json



API_KEY = '5a5db6fa5b4c5'
TRANSCODING_PROFILEID = '5a5db6fa5b8ac'
VIDO_URL = 'https://qa.qencode.com/static/1.mp4'

line = "-" * 80 + "\n"

def my_callback(e):
  try:
    print_status(e)
  except BaseException as e:
    print str(e)


def my_callback2(e):
  try:
    print_status(e)
  except BaseException as e:
    print str(e)

def print_status(status):
  if not status['error'] and status['status'] != 'error':
    print "Status: {0} {1}%".format(status.get('status'), status.get('percent'))
  elif status['error'] or status['status'] == 'error':
    print "Error: %s\n" % (status.get('error_description'))
  if status['status'] == 'completed':
    print line
    for video in status['videos']:
      meta = json.loads(video['meta'])
      print 'Resolution: %s' % meta.get('resolution')
      print 'Url: %s' % video.get('url')
    print line

def start_encode():
  """
    Create encoder object
    :param api_key: string
    :param api_url: string. not required
    :return: encode object
  """
  client = qencode.client(API_KEY)
  if client.error:
   print 'Error: %s\n' % client.message
   raise SystemExit

  """
    Create task
    :param access_token: string. access_token from encoder object
    :param connect: string. connect object from encoder object
    :return: task object
  """
  task = client.create_task()
  task.start(TRANSCODING_PROFILEID, VIDO_URL)
  if task.error:
    print 'Error: %s\n' % task.message
    raise SystemExit

  task.progress_changed(my_callback)
  task.task_completed(my_callback2)




if __name__ == '__main__':
   start_encode()