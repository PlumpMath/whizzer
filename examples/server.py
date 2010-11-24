# -*- coding: utf-8 -*-
# Copyright (c) 2010 Tom Burdick <thomas.burdick@gmail.com>
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

import sys
import time
import signal
import logbook
from logbook.more import ColorizedStderrHandler

import pyev
import cProfile
import pstats

sys.path.insert(0, '..')

import whizzer

logger = logbook.Logger('echo server')

class EchoProtocol(whizzer.Protocol):
    def data(self, data):
        logger.info("got data, returning it")
        self.transport.write(data)

def main():
    loop = pyev.default_loop()
    
    signal_handler = whizzer.signal_handler(loop)
   
    factory = whizzer.ProtocolFactory()
    factory.protocol = EchoProtocol

    server = whizzer.TcpServer(loop, factory, "127.0.0.1", 2000, 256)

    signal_handler.start()
    server.start()
    loop.loop()

if __name__ == "__main__":
    stderr_handler = ColorizedStderrHandler(level='DEBUG')
    with stderr_handler.applicationbound():
        main()
