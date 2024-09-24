accesslog_schema = {
    "type": "record",
    "name": "AccessLog",
    "fields": [
        {
            "name": "timestamp",
            "type": [
                "null",
                {
                    "type": "long",
                    "logicalType": "timestamp-micros"
                }
            ],
            "default": None
        },
        {
            "name": "id",
            "type": [
                "null",
                "string"
            ]
        },
        {
            "name": "traceId",
            "type": [
                "null",
                "string"
            ]
        },
        {
            "name": "ip",
            "type": [
                "null",
                "string"
            ]
        },
        {
            "name": "userAgent",
            "type": [
                "null",
                "string"
            ]
        },
        {
            "name": "method",
            "type": [
                "null",
                "string"
            ]
        },
        {
            "name": "path",
            "type": [
                "null",
                "string"
            ]
        },
        {
            "name": "query",
            "type": [
                "null",
                "string"
            ]
        },
        {
            "name": "status",
            "type": [
                "null",
                "long"
            ]
        },
        {
            "name": "duration",
            "type": [
                "null",
                "long"
            ]
        },
        {
            "name": "requestSize",
            "type": [
                "null",
                "long"
            ]
        },
        {
            "name": "responseSize",
            "type": [
                "null",
                "long"
            ]
        }
    ]
}
