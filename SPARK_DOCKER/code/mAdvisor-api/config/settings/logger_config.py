
LOGGING = {
	'version': 1,
	'disable_existing_loggers': False,
	'filters': {
		'require_debug_false': {
			'()': 'django.utils.log.RequireDebugFalse',
		},
		'require_debug_true': {
			'()': 'django.utils.log.RequireDebugTrue',
		},
	},
	'formatters': {
		'django.server': {
			'()': 'django.utils.log.ServerFormatter',
			'format': '[%(server_time)s] %(message)s',
		}
	},
	'handlers': {
		'db_handler': {
			'level': 'DEBUG',
			'filters': ['require_debug_true'],
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': 'server_log/gunicorn-db.log',
            'backupCount': 10,  # keep at most 10 log files
            'maxBytes': 5242880,  # 5*1024*1024 bytes (5MB)
		},
		'django.server': {
			'level': 'INFO',
			'class': 'logging.FileHandler',
            'filename': 'server_log/gunicorn-console.log',
			'formatter': 'django.server',
		}
	},
	'loggers': {
        # It will log everything error
		'django': {
			'handlers': [ 'django.server'],
			'level': 'INFO',
		},
        # It will log SQL queries on DEBUG=True
        'django.db.backends': {
            'level': 'DEBUG',
            'handlers': ['db_handler'],
        }
	}
}