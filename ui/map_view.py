import os
import flet as ft
import flet.canvas as cv
from data.shuttle_data import ROUTE_WAYPOINTS, STOPS


SEGMENT_COLORS = {
    "RED": "#E53935",
    "YELLOW": "#FBC02D",
    "BLUE": "#00529B",
}


class InteractiveCampusMap(ft.Container):
    def __init__(self, map_width: int = 400, map_height: int = 330):
        super().__init__()
        self.map_width = map_width
        self.map_height = map_height
        self.width = map_width
        self.height = map_height
        self.bgcolor = "#E8EEF5"
        self.padding = 0

        self.canvas = cv.Canvas(
            width=map_width,
            height=map_height,
            shapes=[],
        )

        asset_file = os.path.join("assets", "peta_itb_jatinangor.png")
        layers = []
        if os.path.exists(asset_file):
            layers.append(
                ft.Image(
                    src="peta_itb_jatinangor.png",
                    width=map_width,
                    height=map_height,
                    fit=ft.BoxFit.CONTAIN,
                )
            )
        else:
            layers.append(
                ft.Container(
                    width=map_width,
                    height=map_height,
                    bgcolor="#DCE8DC",
                    alignment=ft.Alignment(0, -0.85),
                    content=ft.Text(
                        "Peta ITB Jatinangor (Simulasi Rute)",
                        size=11,
                        color="#475569",
                        weight=ft.FontWeight.W_600,
                    ),
                )
            )

        layers.append(self.canvas)
        self.content = ft.Stack(controls=layers, width=map_width, height=map_height)

    def _to_px(self, norm_pos: tuple[float, float]) -> tuple[float, float]:
        img_w = self.map_height / 1.414
        offset_x = (self.map_width - img_w) / 2.0
        return offset_x + norm_pos[0] * img_w, norm_pos[1] * self.map_height

    def render(self, shuttles, origin_stop_id: str, dest_stop_id: str):
        shapes = []
        n = len(ROUTE_WAYPOINTS)

        for i in range(n):
            wp1 = ROUTE_WAYPOINTS[i]
            wp2 = ROUTE_WAYPOINTS[(i + 1) % n]
            x1, y1 = self._to_px(wp1["pos"])
            x2, y2 = self._to_px(wp2["pos"])
            seg_color = SEGMENT_COLORS.get(wp1["segment"], "#00529B")

            shapes.append(
                cv.Line(
                    x1, y1, x2, y2,
                    paint=ft.Paint(
                        color=seg_color,
                        stroke_width=3.5,
                        stroke_cap=ft.StrokeCap.ROUND,
                    ),
                )
            )

        for stop in STOPS:
            sx, sy = self._to_px(stop["pos"])
            is_origin = stop["id"] == origin_stop_id
            is_dest = stop["id"] == dest_stop_id

            if is_origin:
                shapes.append(cv.Circle(sx, sy, 9, paint=ft.Paint(color="#00529B")))
                shapes.append(cv.Circle(sx, sy, 4, paint=ft.Paint(color="#FFFFFF")))
            elif is_dest:
                shapes.append(cv.Circle(sx, sy, 9, paint=ft.Paint(color="#F57C00")))
                shapes.append(cv.Circle(sx, sy, 4, paint=ft.Paint(color="#FFFFFF")))
            else:
                fill_c = "#D32F2F" if stop["is_uturn"] else "#FFFFFF"
                shapes.append(cv.Circle(sx, sy, 5, paint=ft.Paint(color="#00529B")))
                shapes.append(cv.Circle(sx, sy, 3, paint=ft.Paint(color=fill_c)))

        for idx, shuttle in enumerate(shuttles):
            bx, by = self._to_px((shuttle.x, shuttle.y))
            badge_color = "#00529B" if idx == 0 else "#0288D1"

            shapes.append(cv.Circle(bx, by, 12, paint=ft.Paint(color="#4400529B")))
            shapes.append(cv.Circle(bx, by, 8.5, paint=ft.Paint(color=badge_color)))
            shapes.append(
                cv.Circle(
                    bx, by, 8.5,
                    paint=ft.Paint(
                        color="#FFFFFF",
                        style=ft.PaintingStyle.STROKE,
                        stroke_width=2,
                    ),
                )
            )
            shapes.append(
                cv.Text(
                    bx - 6,
                    by - 5,
                    shuttle.unit_id.split("-")[1],
                    style=ft.TextStyle(
                        size=9,
                        weight=ft.FontWeight.BOLD,
                        color="#FFFFFF",
                    ),
                )
            )

        self.canvas.shapes = shapes
        try:
            self.canvas.update()
        except Exception:
            pass