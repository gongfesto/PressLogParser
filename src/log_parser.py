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
                elif re.match(r"^\d+;\d+\.\d+;\d+\.\d+;T#.*", line):
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

def parse_time(time_str: str) -> int:
    match = re.match(r'T#(?:(\d+)d)?(?:(\d+)h)?(?:(\d+)m)?(?:(\d+)s)?(\d+)ms', time_str)
    if not match:
        match = re.match(r'T#(?:(\d+)m)?(?:(\d+)s)?(\d+)ms', time_str)
    if match:
        days = int(match.group(1)) if match.lastindex >= 1 and match.group(1) else 0
        hours = int(match.group(2)) if match.lastindex >= 2 and match.group(2) else 0
        minutes = int(match.group(3)) if match.lastindex >= 3 and match.group(3) else 0
        seconds = int(match.group(4)) if match.lastindex >= 4 and match.group(4) else 0
        milliseconds = int(match.group(match.lastindex))
        return (days * 24 * 60 * 60 * 1000) + (hours * 60 * 60 * 1000) + (minutes * 60 * 1000) + (seconds * 1000) + milliseconds
    return 0
