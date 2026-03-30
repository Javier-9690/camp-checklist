"""All room codes organized by building/sector."""

ROOMS = {
    "S18": [f"S18{str(i).zfill(2)}" for i in range(1, 27)],
    "S23": [f"S23{str(i).zfill(2)}" for i in range(1, 27)],
    "S24": [f"S24{str(i).zfill(2)}" for i in range(1, 27)],
    "S25": [f"S25{str(i).zfill(2)}" for i in range(1, 27)],
    "S27": [f"S27{str(i).zfill(2)}" for i in range(1, 27)],
    "S28": [f"S28{str(i).zfill(2)}" for i in range(1, 27)],
    "S29": [f"S29{str(i).zfill(2)}" for i in range(1, 27)],
    "S33": [f"S33{str(i).zfill(2)}" for i in range(1, 37)],
    "S34": [f"S34{str(i).zfill(2)}" for i in range(1, 37)],
    "S35": [f"S35{str(i).zfill(2)}" for i in range(1, 37)],
    "S36": [f"S36{str(i).zfill(2)}" for i in range(1, 37)],
    "S37": [f"S37{str(i).zfill(2)}" for i in range(1, 37)],
    "S38": [f"S38{str(i).zfill(2)}" for i in range(1, 37)],
    "S39": [f"S39{str(i).zfill(2)}" for i in range(1, 37)],
    "S40": [f"S40{str(i).zfill(2)}" for i in range(1, 37)],
    "S20": [f"S20{str(i).zfill(2)}" for i in range(1, 49)],
    "S21": [f"S21{str(i).zfill(2)}" for i in range(1, 49)],
    "S22": [f"S22{str(i).zfill(2)}" for i in range(1, 49)],
    "41G": [f"41G{str(i).zfill(2)}" for i in range(1, 31)],
    "42G": [f"42G{str(i).zfill(2)}" for i in range(1, 31)],
    "43G": [f"43G{str(i).zfill(2)}" for i in range(1, 31)],
    "44G": [f"44G{str(i).zfill(2)}" for i in range(1, 31)],
    "1F": [f"1F{str(i).zfill(2)}" for i in range(1, 49)],
    "2F": [f"2F{str(i).zfill(2)}" for i in range(1, 49)],
    "3F": [f"3F{str(i).zfill(2)}" for i in range(1, 49)],
    "4F": [f"4F{str(i).zfill(2)}" for i in range(1, 49)],
    "5F": [f"5F{str(i).zfill(2)}" for i in range(1, 49)],
    "6F": [f"6F{str(i).zfill(2)}" for i in range(1, 49)],
    "7F": [f"7F{str(i).zfill(2)}" for i in range(1, 49)],
    "8F": [f"8F{str(i).zfill(2)}" for i in range(1, 49)],
    "9F": [f"9F{str(i).zfill(2)}" for i in range(1, 49)],
    "10F": [f"10F{str(i).zfill(2)}" for i in range(1, 49)],
    "11F": [f"11F{str(i).zfill(2)}" for i in range(1, 49)],
    "12F": [f"12F{str(i).zfill(2)}" for i in range(1, 49)],
    "13F": [f"13F{str(i).zfill(2)}" for i in range(1, 49)],
    "14F": [f"14F{str(i).zfill(2)}" for i in range(1, 49)],
}


def get_all_rooms():
    """Return list of (code, building) tuples."""
    result = []
    for building, codes in ROOMS.items():
        for code in codes:
            result.append((code, building))
    return result


def get_buildings():
    """Return sorted list of building names."""
    return sorted(ROOMS.keys())
