from flask import Flask, render_template, send_file, request, make_response

import asyncio;
import websockets;

import base64
import os

import rclpy
from rclpy.node import Node
from std_msgs.msg import String

import json
from flask_cors import CORS

from ament_index_python.packages import get_package_share_directory


app = Flask(__name__,
	template_folder='./static',
	static_folder='./static',
	static_url_path='/'
)

class FlaskPublisher(Node):
    def __init__(self):
        super().__init__('flask_publisher')
        self.publisher_ = self.create_publisher(String, 'flask_msg', 10)
        timer_period = 0.5
        self.timer = self.create_timer(timer_period, self.timer_callback)
        self.i =0

    def timer_callback(self):
        msg = String()
        msg.data = 'Hello World: %d' %self.i
        self.publisher_.publish(msg)
        self.get_logger().info('Publishing: "%s"' % msg.data)
        self.i += 1

def IS_VALID_JSON(STR_JSON):
	try:
		json.loads(STR_JSON)
	except ValueError as e:
		return False
	return True

def JSON_PARSE_RECURSION(args_JSON):
	if (isinstance(args_JSON, dict)):
		OBJ_RESULT = json.loads(json.dumps(args_JSON))
		for KEY in OBJ_RESULT.keys():
			VALUE = OBJ_RESULT[KEY];
			OBJ_RESULT[KEY] = JSON_PARSE_RECURSION(VALUE)
		return OBJ_RESULT
	elif (isinstance(args_JSON, list)):
		ARR_RESULT = []
		for VALUE in args_JSON:
			ARR_RESULT.append(JSON_PARSE_RECURSION(VALUE))
		return ARR_RESULT
	elif (isinstance(args_JSON, str)):
		if (IS_VALID_JSON(args_JSON)):
			TEMP_OBJECT = json.loads(args_JSON)
			if (isinstance(TEMP_OBJECT, dict)):
				return JSON_PARSE_RECURSION(TEMP_OBJECT)
			elif (isinstance(TEMP_OBJECT, list)):
				return JSON_PARSE_RECURSION(TEMP_OBJECT)
			else:
				return args_JSON
		else:
			return args_JSON
	else:
		return args_JSON
	
async def accept(websocket, path):
	while True:
		data = await websocket.recv();
		print("receive : " + data);
		await websocket.send("echo : " + data);

start_server = websockets.serve(accept, "localhost", 5000);
asyncio.get_event_loop().run_until_complete(start_server);
asyncio.get_event_loop().run_forever();

"""
class WebSocket:
	def __init__(self):
		pass

	def handle_open(self):
		print("client is now connected")

	def handle_message(self, message):
		print("receive from client " + message)
		reply_message = "echo " + message
		print("send to client: " + reply_message)
		return reply_message
	
	def handle_close(self):
		print("client is now disconnected...")

	def handle_error(self, error):
		print("Error occurred : ", error)
"""

def API(args_JSON):
	if 'REQ' in args_JSON:
		#if args_JSON['REQ'] == 'TEST':
		rclpy.init()
		flask_publisher = FlaskPublisher()
		rclpy.spin_once(flask_publisher)
		flask_publisher.get_logger().info('\n==== Stop Publishing ====')
		flask_publisher.destroy_node()
		rclpy.shutdown()
		return json.dumps(args_JSON, indent=4)
	else:
		return json.dumps(args_JSON, indent=4)

@app.route('/test', methods = ['POST', 'GET'])
def index():
	if request.method == 'POST':
		args_JSON = request.form;
	else:
		args_JSON = request.args;
	args_JSON = JSON_PARSE_RECURSION(args_JSON)	
	
	if (len(args_JSON.keys())>0):
		return API(args_JSON);
	else:
		return send_file('index.html')

@app.route('/post/data', methods = ['GET', 'POST'])
def postdata():
	jsonData = request.get_json()
	return "hello world"

@app.route('/script.js', methods = ['GET'])
def script():
	return send_file('script.js')

if __name__ == '__main__':
	app.run(debug=True)