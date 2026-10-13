import csv
import json
from typing import List, Dict, Any
from app.collectors.base import BaseCollector

class GenericCollector(BaseCollector):
    def __init__(self, source: Dict[str, Any], file_path: str = None, file_bytes: bytes = None):
        super().__init__(source)
        self.file_path = file_path
        self.file_bytes = file_bytes

    def collect(self) -> List[Dict[str, Any]]:
        # Support CSV or JSON file intake (local path or uploaded bytes)
        content = None
        if self.file_bytes:
            content = self.file_bytes.decode('utf-8', errors='ignore')
        elif self.file_path:
            with open(self.file_path, 'r', encoding='utf-8') as f:
                content = f.read()
        else:
            raise ValueError("No file provided to GenericCollector")

        # Try JSON
        try:
            data = json.loads(content)
            if isinstance(data, list):
                return data
            if isinstance(data, dict) and 'coupons' in data:
                return data['coupons']
            # wrap single record
            return [data]
        except Exception:
            pass

        # Try CSV
        try:
            rows = []
            reader = csv.DictReader(content.splitlines())
            for r in reader:
                rows.append({k: (v if v != '' else None) for k,v in r.items()})
            return rows
        except Exception as e:
            raise ValueError("Unsupported file format or parse error: " + str(e))
