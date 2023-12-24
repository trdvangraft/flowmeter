from prometheus_client import Counter, Histogram

# Create a counter metric
MESSAGE_SENT = Counter(name='messages_sent', documentation='Number of messages sent', labelnames=['topic'])
MESSAGES_RECIEVED = Counter(name='messages_received', documentation='Number of messages received', labelnames=['topic'])

# App service metrics
REQUEST_TIME = Histogram('request_processing_seconds', 'Time spent processing request', ['method', 'endpoint'])