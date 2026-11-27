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
    def __init__(self, map_width: int = 400, map_height: int = 310):
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

        # 1. Gambar garis rute Merah -> Kuning -> Biru
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

        # 2. Gambar 10 titik pemberhentian dengan kode angka 1 - 10
        for idx, stop in enumerate(STOPS, start=1):
            sx, sy = self._to_px(stop["pos"])
            is_origin = stop["id"] == origin_stop_id
            is_dest = stop["id"] == dest_stop_id
            num_str = str(idx)

            if is_origin:
                fill_color = "#00529B"
                border_color = "#FFFFFF"
                text_color = "#FFFFFF"
                radius = 9.5
            elif is_dest:
                fill_color = "#F57C00"
                border_color = "#FFFFFF"
                text_color = "#FFFFFF"
                radius = 9.5
            else:
                fill_color = "#FFFFFF"
                border_color = "#D32F2F" if stop["is_uturn"] else "#00529B"
                text_color = "#0F172A"
                radius = 8.5

            # Lingkaran pin halte
            shapes.append(cv.Circle(sx, sy, radius, paint=ft.Paint(color=fill_color)))
            shapes.append(
                cv.Circle(
                    sx, sy, radius,
                    paint=ft.Paint(
                        color=border_color,
                        style=ft.PaintingStyle.STROKE,
                        stroke_width=1.8,
                    ),
                )
            )

            # Angka 1 - 10 tepat di tengah lingkaran
            offset_x = -5.5 if idx >= 10 else -3.0
            shapes.append(
                cv.Text(
                    sx + offset_x,
                    sy - 5.5,
                    num_str,
                    style=ft.TextStyle(
                        size=9,
                        weight=ft.FontWeight.BOLD,
                        color=text_color,
                    ),
                )
            )

        # 3. Gambar ikon 2 armada shuttle aktif (bentuk kapsul persegi membulat)
        for idx, shuttle in enumerate(shuttles):
            bx, by = self._to_px((shuttle.x, shuttle.y))
            badge_color = "#003B73" if idx == 0 else "#0284C7"

            shapes.append(
                cv.Rect(
                    bx - 11,
                    by - 8,
                    22,
                    16,
                    border_radius=5,
                    paint=ft.Paint(color=badge_color),
                )
            )
            shapes.append(
                cv.Rect(
                    bx - 11,
                    by - 8,
                    22,
                    16,
                    border_radius=5,
                    paint=ft.Paint(
                        color="#FFFFFF",
                        style=ft.PaintingStyle.STROKE,
                        stroke_width=1.8,
                    ),
                )
            )
            shapes.append(
                cv.Text(
                    bx - 6,
                    by - 5.5,
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