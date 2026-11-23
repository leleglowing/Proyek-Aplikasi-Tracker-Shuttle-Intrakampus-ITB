import flet as ft
from data.shuttle_data import STOPS, OPERATIONAL_INFO
from ui.map_view import InteractiveCampusMap


ITB_BLUE = "#00529B"
ITB_LIGHT_BLUE = "#EBF3FA"
TEXT_DARK = "#1E293B"
TEXT_MUTED = "#64748B"


class HomeView(ft.Column):
    def __init__(self, engine, page: ft.Page):
        super().__init__()
        self.engine = engine
        self.app_page = page
        self.spacing = 0
        self.expand = True

        self.origin_stop_id = STOPS[0]["id"]
        self.dest_stop_id = STOPS[4]["id"]

        # 1. Peta Interaktif
        self.map_view = InteractiveCampusMap(map_width=400, map_height=310)

        self.speed_label = ft.Text(
            "Simulasi 15x", size=11, weight=ft.FontWeight.W_600, color=ITB_BLUE
        )
        self.speed_btn = ft.Container(
            bgcolor="#FFFFFF",
            border=ft.Border.all(1, "#CBD5E1"),
            border_radius=20,
            padding=ft.Padding.symmetric(horizontal=12, vertical=6),
            on_click=self._toggle_sim_speed,
            content=ft.Row(
                spacing=4,
                tight=True,
                controls=[
                    ft.Icon(ft.Icons.SPEED, size=15, color=ITB_BLUE),
                    self.speed_label,
                ],
            ),
        )

        self.legend_chip = ft.Container(
            bgcolor="#FFFFFF",
            border=ft.Border.all(1, "#CBD5E1"),
            border_radius=20,
            padding=ft.Padding.symmetric(horizontal=10, vertical=6),
            content=ft.Row(
                spacing=5,
                tight=True,
                controls=[
                    ft.Container(width=8, height=8, border_radius=4, bgcolor="#E53935"),
                    ft.Text("Merah", size=10, color=TEXT_DARK),
                    ft.Container(width=8, height=8, border_radius=4, bgcolor="#FBC02D"),
                    ft.Text("Kuning", size=10, color=TEXT_DARK),
                    ft.Container(width=8, height=8, border_radius=4, bgcolor=ITB_BLUE),
                    ft.Text("Biru", size=10, color=TEXT_DARK),
                ],
            ),
        )

        map_stack = ft.Stack(
            width=400,
            height=310,
            controls=[
                self.map_view,
                ft.Container(left=12, top=12, content=self.legend_chip),
                ft.Container(right=12, top=12, content=self.speed_btn),
            ],
        )

        # 2. Header Biru ITB & Jam Operasional
        is_open, op_label = self.engine.is_operational_now()
        status_pill_color = "#16A34A" if is_open else "#F59E0B"

        self.hours_banner = ft.Container(
            bgcolor=ITB_BLUE,
            padding=ft.Padding.symmetric(horizontal=16, vertical=12),
            on_click=self._show_operational_dialog,
            content=ft.Column(
                spacing=4,
                tight=True,
                controls=[
                    ft.Row(
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                        controls=[
                            ft.Row(
                                spacing=8,
                                controls=[
                                    ft.Icon(ft.Icons.DIRECTIONS_BUS, color="#FFFFFF", size=18),
                                    ft.Text(
                                        f"ROUTE • {OPERATIONAL_INFO['corridor_code']}",
                                        color="#FFFFFF",
                                        size=13,
                                        weight=ft.FontWeight.BOLD,
                                    ),
                                ],
                            ),
                            ft.Container(
                                bgcolor=status_pill_color,
                                border_radius=10,
                                padding=ft.Padding.symmetric(horizontal=8, vertical=2),
                                content=ft.Text(
                                    op_label,
                                    color="#FFFFFF",
                                    size=9,
                                    weight=ft.FontWeight.BOLD,
                                ),
                            ),
                        ],
                    ),
                    ft.Row(
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                        controls=[
                            ft.Row(
                                spacing=8,
                                controls=[
                                    ft.Icon(ft.Icons.ACCESS_TIME, color="#FFFFFF", size=16),
                                    ft.Text(
                                        f"OPERATIONAL • {OPERATIONAL_INFO['hours_display']}",
                                        color="#FFFFFF",
                                        size=12,
                                        weight=ft.FontWeight.W_500,
                                    ),
                                ],
                            ),
                            ft.Icon(ft.Icons.INFO_OUTLINE, color="#CBE3FA", size=16),
                        ],
                    ),
                ],
            ),
        )

        # 3. Kartu Titik Jemput & Tujuan
        stop_options = [
            ft.dropdown.Option(key=s["id"], text=s["name"]) for s in STOPS
        ]

        self.origin_dropdown = ft.Dropdown(
            value=self.origin_stop_id,
            options=stop_options,
            text_size=12,
            color=TEXT_DARK,
            border=ft.InputBorder.NONE,
            dense=True,
            content_padding=ft.Padding.symmetric(horizontal=4, vertical=0),
            on_select=self._on_route_selection_change,
            expand=True,
        )

        self.dest_dropdown = ft.Dropdown(
            value=self.dest_stop_id,
            options=stop_options,
            text_size=12,
            color=TEXT_DARK,
            border=ft.InputBorder.NONE,
            dense=True,
            content_padding=ft.Padding.symmetric(horizontal=4, vertical=0),
            on_select=self._on_route_selection_change,
            expand=True,
        )

        od_card = ft.Container(
            bgcolor="#FFFFFF",
            margin=ft.Margin.symmetric(horizontal=14, vertical=8),
            padding=ft.Padding.all(10),
            border_radius=12,
            border=ft.Border.all(1, "#CBD5E1"),
            content=ft.Row(
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                controls=[
                    ft.Column(
                        expand=True,
                        spacing=2,
                        tight=True,
                        controls=[
                            ft.Row(
                                spacing=8,
                                controls=[
                                    ft.Icon(ft.Icons.MY_LOCATION, color=ITB_BLUE, size=18),
                                    self.origin_dropdown,
                                ],
                            ),
                            ft.Divider(height=1, color="#E2E8F0"),
                            ft.Row(
                                spacing=8,
                                controls=[
                                    ft.Icon(ft.Icons.PLACE, color="#F57C00", size=18),
                                    self.dest_dropdown,
                                ],
                            ),
                        ],
                    ),
                    ft.Container(
                        bgcolor=ITB_LIGHT_BLUE,
                        border_radius=10,
                        padding=8,
                        on_click=self._swap_stops,
                        content=ft.Icon(ft.Icons.SWAP_VERT, color=ITB_BLUE, size=20),
                    ),
                ],
            ),
        )

        # 4. Pil Estimasi Waktu Penjemputan 2 Shuttle
        self.shuttle_chips_row = ft.Row(spacing=8, scroll=ft.ScrollMode.AUTO)
        shuttle_strip = ft.Container(
            padding=ft.Padding.symmetric(horizontal=14, vertical=2),
            content=self.shuttle_chips_row,
        )

        # 5. Daftar Halte (Menggunakan ListView agar tinggi terukur rapi)
        self.stops_timeline = ft.ListView(
            spacing=2,
            padding=ft.Padding.symmetric(horizontal=14, vertical=4),
            expand=True,
        )

        bottom_panel = ft.Container(
            bgcolor="#FFFFFF",
            expand=True,
            content=ft.Column(
                spacing=0,
                expand=True,
                controls=[
                    self.hours_banner,
                    od_card,
                    shuttle_strip,
                    ft.Container(
                        padding=ft.Padding.only(left=16, top=6, bottom=2),
                        content=ft.Text(
                            "DAFTAR TITIK PEMBERHENTIAN (KLIK UNTUK PILIH JEMPUT)",
                            size=10,
                            weight=ft.FontWeight.BOLD,
                            color=TEXT_MUTED,
                        ),
                    ),
                    self.stops_timeline,
                ],
            ),
        )

        self.controls = [map_stack, bottom_panel]

    def _toggle_sim_speed(self, e):
        if self.engine.speed_multiplier > 1.0:
            self.engine.speed_multiplier = 1.0
            self.speed_label.value = "Real-time 1x"
        else:
            self.engine.speed_multiplier = 15.0
            self.speed_label.value = "Simulasi 15x"
        self.app_page.update()

    def _on_route_selection_change(self, e):
        self.origin_stop_id = self.origin_dropdown.value
        self.dest_stop_id = self.dest_dropdown.value
        self.refresh_ui()

    def _swap_stops(self, e):
        self.origin_stop_id, self.dest_stop_id = self.dest_stop_id, self.origin_stop_id
        self.origin_dropdown.value = self.origin_stop_id
        self.dest_dropdown.value = self.dest_stop_id
        self.refresh_ui()

    def _select_origin_from_list(self, stop_id: str):
        self.origin_stop_id = stop_id
        self.origin_dropdown.value = stop_id
        self.refresh_ui()

    def _show_operational_dialog(self, e):
        dlg = ft.AlertDialog(
            title=ft.Text("Jam Operasional Shuttle ITB", weight=ft.FontWeight.BOLD, color=ITB_BLUE),
            content=ft.Column(
                tight=True,
                spacing=8,
                controls=[
                    ft.Text(f"Koridor: {OPERATIONAL_INFO['corridor_name']}", size=13),
                    ft.Text(f"Jam Layanan: {OPERATIONAL_INFO['hours_display']}", size=13, weight=ft.FontWeight.BOLD),
                    ft.Text(f"Headway Antar Shuttle: ±{OPERATIONAL_INFO['headway_minutes']} menit", size=13),
                    ft.Text("Armada Aktif: 2 Unit (ITB-01 & ITB-02) dengan sistem anti-berpapasan.", size=13),
                    ft.Divider(),
                    ft.Text(OPERATIONAL_INFO["notes"], size=12, color=TEXT_MUTED),
                ],
            ),
            actions=[
                ft.TextButton("Tutup", on_click=lambda _: self.app_page.pop_dialog()),
            ],
        )
        self.app_page.show_dialog(dlg)

    def refresh_ui(self):
        self.map_view.render(self.engine.shuttles, self.origin_stop_id, self.dest_stop_id)
        etas = self.engine.get_eta_for_stop(self.origin_stop_id)

        chips = []
        for idx, info in enumerate(etas):
            is_nearest = idx == 0
            eta_text = (
                "Tiba Sekarang"
                if info["eta_minutes"] == 0
                else f"±{info['eta_minutes']} mnt ({info['stops_remaining']} halte)"
            )
            chips.append(
                ft.Container(
                    bgcolor=ITB_BLUE if is_nearest else "#FFFFFF",
                    border=ft.Border.all(1.5, ITB_BLUE if is_nearest else "#CBD5E1"),
                    border_radius=12,
                    padding=ft.Padding.symmetric(horizontal=12, vertical=6),
                    content=ft.Row(
                        spacing=6,
                        tight=True,
                        controls=[
                            ft.Icon(
                                ft.Icons.DIRECTIONS_BUS,
                                size=16,
                                color="#FFFFFF" if is_nearest else ITB_BLUE,
                            ),
                            ft.Column(
                                spacing=1,
                                tight=True,
                                controls=[
                                    ft.Text(
                                        f"{info['unit_id']} • {eta_text}",
                                        size=11,
                                        weight=ft.FontWeight.BOLD,
                                        color="#FFFFFF" if is_nearest else TEXT_DARK,
                                    ),
                                    ft.Text(
                                        f"Status: {info['status']}",
                                        size=9,
                                        color="#DCEBFA" if is_nearest else TEXT_MUTED,
                                    ),
                                ],
                            ),
                        ],
                    ),
                )
            )
        self.shuttle_chips_row.controls = chips

        seg_badge_colors = {
            "RED": ("#FEE2E2", "#B91C1C", "Merah"),
            "YELLOW": ("#FEF3C7", "#B45309", "Kuning"),
            "BLUE": ("#DBEAFE", "#1D4ED8", "Biru"),
        }

        timeline_items = []
        for stop in STOPS:
            is_origin = stop["id"] == self.origin_stop_id
            is_dest = stop["id"] == self.dest_stop_id
            bg_seg, fg_seg, seg_name = seg_badge_colors[stop["segment"]]

            active_bus_label = ""
            for s in self.engine.shuttles:
                if s.last_stop_id == stop["id"]:
                    active_bus_label = f"🚌 {s.unit_id}"

            dot_color = ITB_BLUE if is_origin else ("#F57C00" if is_dest else "#94A3B8")

            timeline_items.append(
                ft.Container(
                    padding=ft.Padding.symmetric(vertical=7, horizontal=8),
                    border_radius=8,
                    bgcolor=ITB_LIGHT_BLUE if is_origin else ft.Colors.TRANSPARENT,
                    on_click=lambda e, sid=stop["id"]: self._select_origin_from_list(sid),
                    content=ft.Row(
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                        controls=[
                            ft.Row(
                                spacing=10,
                                expand=True,
                                controls=[
                                    ft.Container(
                                        width=12,
                                        height=12,
                                        border_radius=6,
                                        bgcolor="#FFFFFF",
                                        border=ft.Border.all(3, dot_color),
                                    ),
                                    ft.Column(
                                        spacing=1,
                                        expand=True,
                                        tight=True,
                                        controls=[
                                            ft.Text(
                                                stop["name"],
                                                size=12,
                                                weight=ft.FontWeight.BOLD if (is_origin or is_dest) else ft.FontWeight.W_500,
                                                color=ITB_BLUE if is_origin else TEXT_DARK,
                                            ),
                                            ft.Text(
                                                stop["building_ref"],
                                                size=10,
                                                color=TEXT_MUTED,
                                            ),
                                        ],
                                    ),
                                ],
                            ),
                            ft.Row(
                                spacing=4,
                                tight=True,
                                controls=[
                                    ft.Container(
                                        bgcolor="#DCFCE7",
                                        border_radius=6,
                                        padding=ft.Padding.symmetric(horizontal=6, vertical=2),
                                        visible=bool(active_bus_label),
                                        content=ft.Text(
                                            active_bus_label,
                                            size=9,
                                            weight=ft.FontWeight.BOLD,
                                            color="#15803D",
                                        ),
                                    ),
                                    ft.Container(
                                        bgcolor=bg_seg,
                                        border_radius=6,
                                        padding=ft.Padding.symmetric(horizontal=6, vertical=2),
                                        content=ft.Text(
                                            seg_name,
                                            size=9,
                                            weight=ft.FontWeight.BOLD,
                                            color=fg_seg,
                                        ),
                                    ),
                                ],
                            ),
                        ],
                    ),
                )
            )

        self.stops_timeline.controls = timeline_items
        try:
            self.app_page.update()
        except Exception:
            pass