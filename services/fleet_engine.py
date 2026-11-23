import math
from dataclasses import dataclass
from datetime import datetime
from data.shuttle_data import ROUTE_WAYPOINTS, STOPS, OPERATIONAL_INFO


@dataclass
class ShuttleUnit:
    unit_id: str
    plate_number: str
    progress: float          # 0.0 s.d. < 1.0 sepanjang lintasan loop
    x: float = 0.0
    y: float = 0.0
    current_segment: str = "RED"
    current_corridor: str = "MAIN_SPINE"
    status: str = "BERJALAN"  # "BERJALAN", "DI HALTE", "JAGA JARAK"
    dwell_timer: float = 0.0
    last_stop_id: str = ""


class FleetEngine:
    def __init__(self):
        self.waypoints = ROUTE_WAYPOINTS
        self.stops = STOPS
        self.segment_lengths = []
        self.cumulative_lengths = [0.0]
        self.total_length = 0.0

        self._build_route_metrics()
        self.stop_progress_map = self._map_stops_to_progress()

        # Inisialisasi 2 shuttle dengan fase berlawanan (0.00 dan 0.50)
        self.shuttles = [
            ShuttleUnit(unit_id="ITB-01", plate_number="D 7011 ITB", progress=0.00),
            ShuttleUnit(unit_id="ITB-02", plate_number="D 7022 ITB", progress=0.50),
        ]
        self.speed_multiplier = 15.0
        self.update(0.0)

    def _build_route_metrics(self):
        n = len(self.waypoints)
        total = 0.0
        for i in range(n):
            p1 = self.waypoints[i]["pos"]
            p2 = self.waypoints[(i + 1) % n]["pos"]
            dist = math.hypot(p2[0] - p1[0], p2[1] - p1[1])
            self.segment_lengths.append(dist)
            total += dist
            self.cumulative_lengths.append(total)
        self.total_length = total

    def _map_stops_to_progress(self) -> dict[str, float]:
        mapping = {}
        for idx, wp in enumerate(self.waypoints):
            if wp["is_stop"]:
                mapping[wp["id"]] = self.cumulative_lengths[idx] / self.total_length
        return mapping

    def _interpolate_position(self, progress: float):
        progress = progress % 1.0
        target_dist = progress * self.total_length
        n = len(self.waypoints)

        for i in range(n):
            start_d = self.cumulative_lengths[i]
            end_d = self.cumulative_lengths[i + 1]
            if start_d <= target_dist <= end_d:
                seg_len = self.segment_lengths[i]
                ratio = (target_dist - start_d) / seg_len if seg_len > 0 else 0.0
                p1 = self.waypoints[i]["pos"]
                p2 = self.waypoints[(i + 1) % n]["pos"]
                x = p1[0] + (p2[0] - p1[0]) * ratio
                y = p1[1] + (p2[1] - p1[1]) * ratio
                return x, y, self.waypoints[i]["segment"], self.waypoints[i]["corridor"]

        first = self.waypoints[0]
        return first["pos"][0], first["pos"][1], first["segment"], first["corridor"]

    def _check_stop_arrival(self, old_prog: float, new_prog: float) -> str | None:
        for stop_id, stop_prog in self.stop_progress_map.items():
            if old_prog <= new_prog:
                if old_prog < stop_prog <= new_prog:
                    return stop_id
            else:
                if stop_prog > old_prog or stop_prog <= new_prog:
                    return stop_id
        return None

    def update(self, dt: float):
        loop_seconds = OPERATIONAL_INFO["loop_duration_minutes"] * 60.0
        base_speed = (1.0 / loop_seconds) * self.speed_multiplier

        s1, s2 = self.shuttles[0], self.shuttles[1]

        for idx, shuttle in enumerate(self.shuttles):
            other = s2 if idx == 0 else s1

            if shuttle.dwell_timer > 0:
                shuttle.dwell_timer = max(0.0, shuttle.dwell_timer - dt * self.speed_multiplier)
                shuttle.status = "DI HALTE"
                continue

            forward_gap = (other.progress - shuttle.progress) % 1.0
            if forward_gap < 0.42:
                shuttle.status = "JAGA JARAK"
                continue

            step = base_speed * dt
            next_prog = (shuttle.progress + step) % 1.0
            _, _, _, next_corridor = self._interpolate_position(next_prog)

            if next_corridor in ("MAIN_SPINE", "NORTH_RING"):
                if other.current_corridor == next_corridor and forward_gap < 0.48:
                    shuttle.status = "JAGA JARAK"
                    continue

            old_prog = shuttle.progress
            shuttle.progress = next_prog
            shuttle.status = "BERJALAN"

            arrived_stop = self._check_stop_arrival(old_prog, shuttle.progress)
            if arrived_stop and arrived_stop != shuttle.last_stop_id:
                shuttle.last_stop_id = arrived_stop
                shuttle.dwell_timer = 12.0
                shuttle.status = "DI HALTE"

        for shuttle in self.shuttles:
            x, y, seg, corr = self._interpolate_position(shuttle.progress)
            shuttle.x = x
            shuttle.y = y
            shuttle.current_segment = seg
            shuttle.current_corridor = corr

    def get_eta_for_stop(self, target_stop_id: str) -> list[dict]:
        target_prog = self.stop_progress_map[target_stop_id]
        loop_minutes = OPERATIONAL_INFO["loop_duration_minutes"]
        results = []

        for shuttle in self.shuttles:
            delta_prog = (target_prog - shuttle.progress) % 1.0

            stops_remaining = 0
            for s_id, s_prog in self.stop_progress_map.items():
                dist_to_s = (s_prog - shuttle.progress) % 1.0
                if 0.002 < dist_to_s <= delta_prog + 0.002:
                    stops_remaining += 1

            eta_minutes = (delta_prog * loop_minutes) + (stops_remaining * 0.2)
            if delta_prog < 0.015 and shuttle.status == "DI HALTE" and shuttle.last_stop_id == target_stop_id:
                eta_minutes = 0.0
                stops_remaining = 0

            results.append({
                "unit_id": shuttle.unit_id,
                "plate_number": shuttle.plate_number,
                "eta_minutes": max(0, round(eta_minutes)),
                "stops_remaining": stops_remaining,
                "status": shuttle.status,
                "segment": shuttle.current_segment,
            })

        results.sort(key=lambda item: item["eta_minutes"])
        return results

    def is_operational_now(self) -> tuple[bool, str]:
        now = datetime.now()
        open_h = OPERATIONAL_INFO["open_hour"]
        close_h = OPERATIONAL_INFO["close_hour"]
        if open_h <= now.hour < close_h:
            return True, "BEROPERASI"
        return False, "DI LUAR JAM OPERASIONAL"