LOGGING_CONF = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'simple': {
            'format': '{asctime} {levelname} {message}',
            'style' : '{',
        },
        'mediumPath': {
            'format': '{asctime} {levelname} {pathname} {message}',
            'style' : '{',
        },
        'mediumModule': {
            'format': '{asctime} {levelname} {module} {message}',
            'style' : '{',
        },
        'detail': {
            'format': '{asctime} {levelname} {message} {pathname} {exc_info}',
            'style' : '{',
        },
    },
    'filters': {
        'require_debug_true': {
            '()': 'django.utils.log.RequireDebugTrue',
        },
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse',
        },
    },
    'handlers': {
        'consoleDebug': {
            'level': 'DEBUG',
            'filters': ['require_debug_true'],
            'class': 'logging.StreamHandler',
            'formatter': 'simple'
        },
        'consoleWarning': {
            'level': 'WARNING',
            'filters': ['require_debug_true'],
            'class': 'logging.StreamHandler',
            'formatter': 'mediumPath'
        },
        'consoleError': {
            'level': 'ERROR',
            'filters': ['require_debug_true'],
            'class': 'logging.StreamHandler',
            'formatter': 'detail'
        },
        'fileGeneral': {
            'level': 'INFO',
            'filters': ['require_debug_false'],
            'class': 'logging.FileHandler',
            'formatter': 'mediumModule',
            'filename': 'log_files/general.log'
        },
        'fileErrors': {
            'level': 'ERROR',
            'class': 'logging.FileHandler',
            'formatter': 'detail',
            'filename': 'log_files/errors.log'
        },
        'fileSecurity': {
            'class': 'logging.FileHandler',
            'formatter': 'mediumModule',
            'filename': 'log_files/security.log'
        },
        'mailAdmins': {
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler',
            'formatter': 'mediumPath',
        }
    },
    'loggers': {
        'django': {
            'handlers': ['consoleDebug', 'consoleWarning', 'consoleError', 'fileGeneral'],
            'propagate': True,
        },
        'django.request': {
            'handlers': ['fileErrors', 'mailAdmins'],
            'propagate': False,
        },
        'django.server': {
            'handlers': ['fileErrors', 'mailAdmins'],
            'propagate': False,
        },
        'django.template': {
            'handlers': ['fileErrors'],
            'propagate': False,
        },
        'django.db.backends': {
            'handlers': ['fileErrors'],
            'propagate': False,
        },
        'django.security': {
            'handlers': ['fileSecurity'],
            'propagate': False,
        },
        'testLogger': {
            'handlers': ['consoleDebug', 'fileGeneral'],
            'level': 'INFO',
            'propagate': False,
        }
    }
}
