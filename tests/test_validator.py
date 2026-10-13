from app.validator.validator import determine_status
from datetime import datetime, timedelta

def test_validator_expired():
    now = datetime.utcnow()
    n = {'start_at': None, 'end_at': now - timedelta(days=1), 'raw_evidence': 'x'}
    s = determine_status(n)
    assert s == 'EXPIRED'
