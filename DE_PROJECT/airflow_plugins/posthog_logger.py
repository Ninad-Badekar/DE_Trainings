import os
import posthog

POSTHOG_API_KEY = os.getenv("POSTHOG_API_KEY", "phc_YOUR_API_KEY")
POSTHOG_HOST = os.getenv("POSTHOG_HOST", "https://app.posthog.com")

posthog.project_api_key = POSTHOG_API_KEY
posthog.host = POSTHOG_HOST

def log_event(event_name, distinct_id="airflow_user", properties=None):
    try:
        posthog.capture(
            distinct_id=distinct_id,
            event=event_name,
            properties=properties or {}
        )
        print(f"✅ Event sent: {event_name}")
    except Exception as e:
        print(f"❌ Failed to send PostHog event: {e}")
