import logging

LOGGING = {
	'version': 1,
	'disable_existing_loggers': False,
	'formatters': {
		'standard': {
			'format': '%(asctime)s %(levelname)s %(name)s %(message)s'  # Added '%' at the end
		},
	},

	'handlers': {
		'console': {
			'level': 'INFO',
			'class': 'logging.StreamHandler',
			'formatter': 'standard',
			'filters': [],
		},
	},

	'loggers': {
		'django': {
			'level': 'WARNING',
			'propagate': True,
		},
		'django.request': {
			'level': 'WARNING',
			'propagate': True,
		},
		'django.db.backends': {
			'level': 'WARNING',
			'propagate': True,
		},
		'django.template': {
			'level': 'WARNING',
			'propagate': True,
		},
		'tuxedo.core': {
			'level': 'WARNING',
			'propagate': True,
		},
	},

	'root': {
		'level': 'DEBUG',
		'handlers': ['console'],
	},

	# 'loggers': {
	# 	logger_name: {
	# 		'level': 'WARNING',
	# 		'propagate': True,
	# 	},
	# } for logger_name in ('django', 'django.request', 'django.db.backends', 'django.template', 'tuxedo.core')
}

logger = logging.getLogger(__name__)