
class PySparkLoggerAdapter():
    def __init__(self, spark):
        spark.sparkContext.setLogLevel("INFO")
        # get spark app details with which to prefix all messages
        conf = spark.sparkContext.getConf()
        app_id = conf.get('spark.app.id')
        app_name = conf.get('spark.app.name')
        log4j = spark._jvm.org.apache.log4j
        message_prefix = "{} {}".format(app_name, app_id)
        self.logger = log4j.LogManager.getLogger("")
        self.log_prefix = message_prefix


class PythonLoggerAdapter():
    def __init__(self):
        import logging
        MSG_FORMAT = '%(asctime)s %(levelname)s %(name)s: %(message)s'
        DATETIME_FORMAT = '%Y-%m-%d %H:%M:%S'
        logging.basicConfig(format=MSG_FORMAT, datefmt=DATETIME_FORMAT)
        self.logger = logging.getLogger("<logger-name-here>")
        self.logger.setLevel(logging.INFO)


class JobLogger():
    def __init__(self, loggerAdapter):
        self.logger = loggerAdapter.logger
        self.log_prefix = loggerAdapter.log_prefix

    def error(self, message):
        self.logger.error("< {} > {}".format(self.log_prefix, message))
        return None

    def warn(self, message):
        self.logger.warn("< {} > {}".format(self.log_prefix, message))
        return None

    def info(self, message):
        self.logger.info("< {} > {}".format(self.log_prefix, message))
        return None
