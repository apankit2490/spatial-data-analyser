"""
Utility Module to serve common utility functions
"""
import logging

logger = logging.getLogger('spatial-data-analyser')


def celery_logger_handler(message, success):
    """
    Closure Function for celery log handler to dynamically obtain success and failure log handlers
     as per the specified message.
    :param message: Message to be logged in success and failure logs
    :param success: Boolean value denoting task status
    :return: log handler function
    """

    def log_handler(self, exec, task_id, args, kwargs, einfo=''):
        if success:
            logger.info(f'Successful! {message} \nTask: {self.__qualname__} \nTask id: {task_id}\nJob result: {exec}')
        else:
            logger.error(f'Failed {message} Task: {self.__qualname__}'
                         f'\ntask id: {task_id} \nargs: {args}\nkwargs: {kwargs}\neinfo: {einfo}')

    return log_handler
