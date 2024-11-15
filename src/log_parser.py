# src/log_parser.py
import re
import pandas as pd
from typing import List, Dict, Any

class LogParser:
    def __init__(self, file_content: str) -> None:
        self.file_content: str = file_content

    def parse_log(self) -> List[pd.DataFrame]:
        records: List[Dict[str, Any]] = []
        record_section: bool = False
        current_record: Dict[str, Any] = {}

        for line in self.file_content.splitlines():
            if "[Recorded curves]" in line:
                record_section = True
            elif "[Variables]" in line:  # End of recorded curves section
                record_section = False

            # Extract records within "[Recorded curves]"
            if record_section:
                if line.startswith("[Record "):
                    # Start a new record
                    current_record = {"points": []}
                    records.append(current_record)
                elif re.match(r"^\d+;\d+\.\d+;\d+\.\d+;T#\d+m\d+s\d+ms", line):
                    # Parse points within the current record
                    fields: List[str] = line.split(";")
                    point: int = int(fields[0])
                    position: float = float(fields[1])
                    force: float = float(fields[2])
                    time: str = fields[3]
                    current_record["points"].append({"Point": point, "Position": position, "Force": force, "Time": time})

        # Convert records into a list of dataframes
        record_dfs: List[pd.DataFrame] = [pd.DataFrame(record["points"]) for record in records if "points" in record]
        return record_dfs
