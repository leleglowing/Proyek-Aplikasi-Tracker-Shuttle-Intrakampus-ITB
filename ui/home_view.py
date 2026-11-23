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

        self.origin_stop_id = STOPS[0]["id"]   # Default: Halte Gerbang Utama (1)
        self.dest_stop_id = STOPS[4]["id"]     # Default: Halte Perpustakaan & GSG (32/31)
        self.selected_shuttle_id = "ITB-01"

        # 1. Peta Interaktif di bagian atas
        self.map_view = InteractiveCampusMap(map_width=400, map_height=330)

        # Tombol floating di atas peta (Legenda Rute & Speed Toggle)
        self.speed_btn = ft.Container(
            bgcolor="#FFFFFF",
            border_radius=20,
            padding=ft.Padding.symmetric(horizontal=12, vertical=6),
            shadow=ft.BoxShadow(blur_radius=8, color="#22000000"),
            on_click=self._toggle_sim_speed,
            content=ft.Row(
                spacing=4,
                controls=[
                    ft.Icon("speed", size=15, color=ITB_BLUE),
                    ft.Text("Simulasi 15x", size=11, weight=ft.FontWeight.W_600, color=ITB_BLUE),
                ],
            ),
        )

        self.legend_chip = ft.Container(
            bgcolor="#FFFFFF",
            border_radius=20,
            padding=ft.Padding.symmetric(horizontal=10, vertical=6),
            shadow=ft.BoxShadow(blur_radius=8, color="#22000000"),
            content=ft.Row(
                spacing=6,
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
            height=330,
            controls=[
                self.map_view,
                ft.Container(left=12, top=12, content=self.legend_chip),
                ft.Container(right=12, top=12, content=self.speed_btn),
            ],
        )

        # 2. Banner Header Biru ITB (Mirip banner Koridor & Jam Operasional Metro Jabar Trans)
        is_open, op_label = self.engine.is_operational_now()
        status_pill_color = "#16A34A" if is_open else "#F59E0B"

        self.hours_banner = ft.Container(
            bgcolor=ITB_BLUE,
            border_radius=ft.BorderRadius.only(top_left=20, top_right=20),
            padding=ft.Padding.only(left=16, right=16, top=14, bottom=14),
            on_click=self._show_operational_dialog,
            content=ft.Column(
                spacing=6,
                controls=[
                    ft.Row(
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                        controls=[
                            ft.Row(
                                spacing=8,
                                controls=[
                                    ft.Icon("directions_bus", color="#FFFFFF", size=18),
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
                                    ft.Icon("access_time", color="#FFFFFF", size=16),
                                    ft.Text(
                                        f"OPERATIONAL • {OPERATIONAL_INFO['hours_display']}",
                                        color="#FFFFFF",
                                        size=12,
                                        weight=ft.FontWeight.W_500,
                                    ),
                                ],
                            ),
                            ft.Icon("info_outline", color="#CBE3FA", size=16),
                        ],
                    ),
                ],
            ),
        )

        # 3. Kartu Pemilih Titik Jemput & Tujuan (Origin - Destination Card)
        stop_options = [
            ft.dropdown.Option(key=s["id"], text=s["name"]) for s in STOPS
        ]

        self.origin_dropdown = ft.Dropdown(
            value=self.origin_stop_id,
            options=stop_options,
            text_size=13,
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
            text_size=13,
            color=TEXT_DARK,
            border=ft.InputBorder.NONE,
            dense=True,
            content_padding=ft.Padding.symmetric(horizontal=4, vertical=0),
            on_select=self._on_route_selection_change,
            expand=True,
        )

        od_card = ft.Container(
            bgcolor="#FFFFFF",
            margin=ft.Margin.symmetric(horizontal=14, vertical=10),
            padding=ft.Padding.all(12),
            border_radius=14,
            border=ft.Border.all(1, "#E2E8F0"),
            shadow=ft.BoxShadow(blur_radius=10, color="#12000000"),
            content=ft.Row(
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                controls=[
                    ft.Column(
                        expand=True,
                        spacing=4,
                        controls=[
                            ft.Row(
                                spacing=8,
                                controls=[
                                    ft.Icon("my_location", color=ITB_BLUE, size=18),
                                    self.origin_dropdown,
                                ],
                            ),
                            ft.Divider(height=1, color="#E2E8F0"),
                            ft.Row(
                                spacing=8,
                                controls=[
                                    ft.Icon("place", color="#F57C00", size=18),
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
                        content=ft.Icon("swap_vert", color=ITB_BLUE, size=20),
                    ),
                ],
            ),
        )

        # 4. Baris Pil Armada & Estimasi Waktu Penjemputan (ITB-01 & ITB-02)
        self.shuttle_chips_row = ft.Row(
            spacing=8,
            scroll=ft.ScrollMode.AUTO,
        )
        shuttle_strip = ft.Container(
            padding=ft.Padding.symmetric(horizontal=14, vertical=2),
            content=self.shuttle_chips_row,
        )

        # 5. Daftar Timeline Halte Rute Intrakampus
        self.stops_timeline = ft.Column(
            spacing=0,
            scroll=ft.ScrollMode.AUTO,
            expand=True,
        )

        bottom_sheet = ft.Container(
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
                        padding=ft.Padding.only(left=16, top=8, bottom=4),
                        content=ft.Text(
                            "DAFTAR TITIK PEMBERHENTIAN (KLIK UNTUK PILIH JEMPUT)",
                            size=10,
                            weight=ft.FontWeight.BOLD,
                            color=TEXT_MUTED,
                        ),
                    ),
                    ft.Container(
                        padding=ft.Padding.symmetric(horizontal=16, vertical=4),
                        expand=True,
                        content=self.stops_timeline,
                    ),
                ],
            ),
        )

        self.controls = [map_stack, bottom_sheet]
        self.refresh_ui()

    def _toggle_sim_speed(self, e):
        if self.engine.speed_multiplier > 1.0:
            self.engine.speed_multiplier = 1.0
            label = "Real-time 1x"
        else:
            self.engine.speed_multiplier = 15.0
            label = "Simulasi 15x"
        self.speed_btn.content.controls[1].value = label
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
                ft.TextButton("Tutup", on_click=lambda _: self.app_page.close(dlg)),
            ],
        )
        self.app_page.open(dlg)

    def refresh_ui(self):
        # 1. Update peta & posisi 2 shuttle
        self.map_view.render(self.engine.shuttles, self.origin_stop_id, self.dest_stop_id)

        # 2. Hitung ETA penjemputan di titik jemput user
        etas = self.engine.get_eta_for_stop(self.origin_stop_id)

        # Render pil shuttle (mirip MJT K5-13, MJT K5-01 di referensi Metro Jabar Trans)
        chips = []
        for idx, info in enumerate(etas):
            is_nearest = idx == 0
            eta_text = "Tiba Sekarang" if info["eta_minutes"] == 0 else f"±{info['eta_minutes']} mnt ({info['stops_remaining']} halte)"
            chips.append(
                ft.Container(
                    bgcolor=ITB_BLUE if is_nearest else "#FFFFFF",
                    border=ft.Border.all(1.5, ITB_BLUE if is_nearest else "#CBD5E1"),
                    border_radius=12,
                    padding=ft.Padding.symmetric(horizontal=12, vertical=8),
                    content=ft.Row(
                        spacing=6,
                        controls=[
                            ft.Icon(
                                "directions_bus",
                                size=16,
                                color="#FFFFFF" if is_nearest else ITB_BLUE,
                            ),
                            ft.Column(
                                spacing=1,
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

        # 3. Render daftar halte vertikal
        seg_badge_colors = {
            "RED": ("#FEE2E2", "#B91C1C", "Merah"),
            "YELLOW": ("#FEF3C7", "#B45309", "Kuning"),
            "BLUE": ("#DBEAFE", "#1D4ED8", "Biru"),
        }

        timeline_items = []
        for idx, stop in enumerate(STOPS):
            is_origin = stop["id"] == self.origin_stop_id
            is_dest = stop["id"] == self.dest_stop_id
            bg_seg, fg_seg, seg_name = seg_badge_colors[stop["segment"]]

            # Cek apakah ada shuttle yang baru melewati/berada di halte ini
            active_bus_label = ""
            for s in self.engine.shuttles:
                if s.last_stop_id == stop["id"]:
                    active_bus_label = f"🚌 {s.unit_id}"

            dot_color = ITB_BLUE if is_origin else ("#F57C00" if is_dest else "#94A3B8")

            timeline_items.append(
                ft.Container(
                    padding=ft.Padding.symmetric(vertical=7, horizontal=6),
                    border_radius=8,
                    bgcolor=ITB_LIGHT_BLUE if is_origin else "transparent",
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
        if getattr(self, "_page", None) is not None:
            self.app_page.update()