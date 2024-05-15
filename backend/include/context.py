import logging 
import sqlite3
import sys

class Context:
    app=None
    def database(self):
        try:
            return self.conn
        except:
            pass

        self.logger.info('Database Connecting.... ')
        try:
            conn = sqlite3.connect("../sqlite3.db")
        except Exception as e:
            self.logger.error("Error: Can't connect to database #"+str(e))
            sys.exit('')
            
        conn.set_session(autocommit=True)
        return conn


    def logger(self):
        try:
            return self.logger_
        except:
            pass
        logger_ = logging.getLogger(__name__)
        logger_.setLevel(logging.DEBUG)
        # initilize logging
        stream_handler = logging.StreamHandler()
        stream_handler.setLevel(logging.INFO)  
        # initilize stream_handler
        file_handler = logging.FileHandler('logs/stdout.log')
        file_handler.setLevel(logging.INFO)  
        # info 
        stderr_handler = logging.StreamHandler(sys.stderr)
        stderr_handler.setLevel(logging.ERROR) 
        # error
        '''save logs to a file'''
        log_format = "%(levelname)s:\t  %(filename)s:%(lineno)d | `%(message)s` | %(asctime)s"
        formatter = logging.Formatter(log_format)
        # set log format

        stream_handler.setFormatter(formatter)
        stderr_handler.setFormatter(formatter)
        file_handler.setFormatter(formatter)
        # set custom format for logginng

        logger_.addHandler(stream_handler)
        logger_.addHandler(file_handler)
        logger_.addHandler(stderr_handler)
        self.logger = logger_
        '''set logger'''
        return logger_