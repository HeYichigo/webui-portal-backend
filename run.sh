uvicorn main:app --reload --host 0.0.0.0 --port 7860 --proxy-headers --forwarded-allow-ips='*'