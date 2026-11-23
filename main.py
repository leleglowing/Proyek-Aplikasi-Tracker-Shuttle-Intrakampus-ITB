import asyncio
import flet as ft
from services.fleet_engine import FleetEngine
from ui.home_view import HomeView


async def main(page: ft.Page):
    page.title = "Shuttle ITB Jatinangor"
    page.window.width = 416
    page.window.height = 860
    page.window.resizable = False
    page.padding = 0
    page.bgcolor = "#F8FAFC"
    page.theme_mode = ft.ThemeMode.LIGHT

    engine = FleetEngine()
    home_view = HomeView(engine=engine, page=page)
    page.add(home_view)

    # Loop pembaruan posisi shuttle setiap 0.25 detik
    async def simulation_loop():
        while True:
            await asyncio.sleep(0.25)
            engine.update(0.25)
            home_view.refresh_ui()

    page.run_task(simulation_loop)


if __name__ == "__main__":
    ft.run(main)