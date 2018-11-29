import socket
import threading
import cv2

import validators


class Tello:
    def __init__(self, local_host='0.0.0.0', local_state_port=8890, timeout=.3, tello_host='192.168.10.1', tello_port=8889, tello_video_port=11111):
        self.abort_flag = False
        self.response = None
        self.state = None
        self.frame = []
        self.is_new_frame_to_process = False

        self.timeout = timeout
        self.local_adress = (local_host, tello_port)
        self.local_state_adress = (local_host, local_state_port)
        self.tello_address = (tello_host, tello_port)

        self.socket = socket.socket(
            family=socket.AF_INET, type=socket.SOCK_DGRAM)
        self.socket.bind(self.local_adress)

        self.state_socket = socket.socket(
            family=socket.AF_INET, type=socket.SOCK_DGRAM)
        self.state_socket.bind(self.local_state_adress)

        self.receive_thread = threading.Thread(target=self._receive_thread)
        self.receive_thread.daemon = True
        self.receive_thread.start()

        if self._send_command('command') != 'ok':
            raise RuntimeError('enter_SDK_failure')

        self.state_receive_thread = threading.Thread(
            target=self._state_receive_thread)
        self.state_receive_thread.daemon = True
        self.state_receive_thread.start()

        if self.set_video_stream_on() != 'ok':
            raise RuntimeError('video_stream_on_failure')

        video_stream_url = 'udp://%s:%s' % (tello_host, tello_video_port)

        self.cap = cv2.VideoCapture(video_stream_url)
        if not self.cap.isOpened():
            raise RuntimeError('video_capture_not_opened')

        self.video_receive_thread = threading.Thread(
            target=self._video_receive_thread)
        self.video_receive_thread.daemon = True
        self.video_receive_thread.start()

    def __del__(self):
        self.socket.close()
        self.state_socket()
        self.cap.release()

    def _receive_thread(self):
        while True:
            try:
                receive_buffer_size = 1518
                self.response, _ = self.socket.recvfrom(
                    receive_buffer_size)
            except Exception:
                break

    def _state_receive_thread(self):
        while True:
            try:
                receive_buffer_size = 1518
                self.state, _ = self.state_socket.recvfrom(
                    receive_buffer_size)
            except Exception:
                break

    def _video_receive_thread(self):
        while True:
            try:
                ret, frame = self.cap.read()
                if not ret:
                    break
                self.frame = frame
                self.is_new_frame_to_process = True

            except Exception:
                print(Exception)
                break

    def is_new_frame_ready(self):
        return self.is_new_frame_to_process

    def get_last_frame(self):
        self.is_new_frame_to_process = False
        return self.frame

    def _to_dictionary(self, response_string):
        result = dict()
        params = response_string[:-3].split(';')

        for param in params:
            key_value = param.split(':')
            result[key_value[0]] = float(key_value[1])

        return result

    def _send_command(self, command):
        self.abort_flag = False
        timer = threading.Timer(self.timeout, self._set_abort_flag)
        self.socket.sendto(command.encode('utf-8'), self.tello_address)
        timer.start()

        while self.response is None:
            if self.abort_flag is True:
                raise RuntimeError('no_response_to_command')

        timer.cancel()
        response = self.response.decode('utf-8')
        self.response = None

        return response

    def _set_abort_flag(self):
        self.abort_flag = True

    def takeoff(self):
        return self._send_command('takeoff')

    def land(self):
        return self._send_command('land')

    def set_video_stream_on(self):
        return self._send_command('streamon')

    def set_video_stream_off(self):
        return self._send_command('streamoff')

    def emergency_off(self):
        return self._send_command('emergency')

    def move_backward(self, distance):
        error = validators.validate_move(distance)
        print(error)
        if error:
            return error
        return self._send_command('back %s' % distance)

    def move_down(self, distance):
        error = validators.validate_move(distance)
        if error:
            return error
        return self._send_command('down %s' % distance)

    def move_forward(self, distance):
        error = validators.validate_move(distance)
        if error:
            return error
        return self._send_command('forward %s' % distance)

    def move_left(self, distance):
        error = validators.validate_move(distance)
        if error:
            return error
        return self._send_command('left %s' % distance)

    def move_right(self, distance):
        error = validators.validate_move(distance)
        if error:
            return error
        return self._send_command('right %s' % distance)

    def move_up(self, distance):
        error = validators.validate_move(distance)
        if error:
            return error
        return self._send_command('up %s' % distance)

    def flip(self, direction):
        error = validators.validate_flip(direction)
        if error:
            return error
        return self._send_command('flip %s' % direction)

    def rotate_cw(self, degree):
        error = validators.validate_rotate(degree)
        if error:
            return error
        return self._send_command('cw %s' % degree)

    def rotate_ccw(self, degree):
        error = validators.validate_rotate(degree)
        if error:
            return error
        return self._send_command('ccw %s' % degree)

    def go(self, x, y, z, speed):
        error = validators.validate_go(x, y, z, speed)
        if error:
            return error
        return self._send_command('go %s %s %s %s' % (x, y, z, speed))

    def curve(self, x1, y1, z1, x2, y2, z2, speed):
        error = validators.validate_curve(x1, y1, z1, x2, y2, z2, speed)
        if error:
            return error
        return self._send_command('curve %s %s %s %s %s %s %s' % (x1, y1, z1, x2, y2, z2, speed))

    def send_rc_control(self, a, b, c, d):
        error = validators.validate_rc_control(a, b, c, d)
        if error:
            return error
        return self._send_command('rc %s %s %s %s' % (a, b, c, d))

    def set_wifi(self, ssid, password):
        if(not validators.is_string_valid(ssid)):
            return 'error_invalid_ssid'
        if(not validators.is_string_valid(password)):
            return 'error_invalid_password'
        return self._send_command('wifi %s %s' % (ssid, password))

    def set_speed(self, speed):
        if(not validators.is_speed_valid(speed)):
            return 'error_invalid_speed'
        return self._send_command('speed %s' % speed)

    def get_speed(self):
        return self._send_command('speed?')

    def get_flight_time(self):
        return self._send_command('time?')

    def get_battery(self):
        return self._send_command('battery?')

    def get_height(self):
        return self._send_command('height?')

    def get_temp(self):
        return self._send_command('temp?')

    def get_attitude(self):
        return self._to_dictionary(self._send_command('attitude?'))

    def get_baro(self):
        return self._send_command('baro?')

    def get_tof(self):
        return self._send_command('tof?')

    def get_wifi_snr(self):
        return self._send_command('wifi?')

    def get_state(self):
        if self.state is None:
            return None
        return self._to_dictionary(self.state.decode('utf-8'))
