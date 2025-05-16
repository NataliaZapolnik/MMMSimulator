from dearpygui import dearpygui as dpg
from config import FONT_PATH


def run_simulation_callback():
    a1 = dpg.get_value("a1_input")
    a0 = dpg.get_value("a0_input")
    b2 = dpg.get_value("b2_input")
    b1 = dpg.get_value("b1_input")
    b0 = dpg.get_value("b0_input")
    kp = dpg.get_value("kp_input")
    ki = dpg.get_value("ki_input")
    signal = dpg.get_value("signal_selector")
    sim_time = dpg.get_value("czas_symulacji")

    print(f"Symulacja: a1={a1}, a0={a0}, b2={b2}, b1={b1}, b0={b0}, Kp={kp}, Ki={ki}, sygnał={signal}, czas={sim_time}")
    # TODO: wywołanie backendu i aktualizacja wykresu

def piRegulatorCallback():
    return 1

# --- Tworzenie GUI ---
dpg.create_context()
dpg.create_viewport(title="MMMSimulator", width=920, height=650, resizable=False, decorated=True)
dpg.setup_dearpygui()
print(dpg.mvFontRangeHint_Cyrillic)
with dpg.font_registry():
    with dpg.font(FONT_PATH, 12, default_font=True):
        dpg.add_font_range_hint(dpg.mvFontRangeHint_Cyrillic)

with dpg.window(tag="main"):
    with dpg.group(tag="specs", horizontal=True, horizontal_spacing=100):
        # Okno sygnału
        with dpg.group(width=200):
            dpg.add_text("Sygnał wejściowy:")
            dpg.add_combo(tag="signal_selector", label="Sygnał", items=["Sygnał prostokątny", "Sygnał sinusoidalny", "Sygnał trójkątny"], default_value="Sygnał prostokątny")
            dpg.add_input_float(tag="kp_input", label="Kp", default_value=0.0)
            dpg.add_input_float(tag="ki_input", label="Ki", default_value=0.0)
        # Parametry regulatora PI
        with dpg.group(width=200):
            dpg.add_text("Parametry układu:")
            dpg.add_input_float(tag="a1_input", label="a1", default_value=0.0)
            dpg.add_input_float(tag="a0_input", label="a0", default_value=0.0)
            dpg.add_input_float(tag="b2_input", label="b2", default_value=0.0)
            dpg.add_input_float(tag="b1_input", label="b1", default_value=0.0)
            dpg.add_input_float(tag="b0_input", label="b0", default_value=0.0)
            dpg.add_button(label="Regulator PI", callback=piRegulatorCallback)

        # Czas symulacji
        with dpg.group(width=200):
            dpg.add_text("Parametry symulacji:")
            dpg.add_input_float(tag="t", label="t[s]", default_value=10.0)
            dpg.add_input_float(tag="dt", label="dt[s]", default_value=0.1)
    with dpg.group(tag="plot", width=920):
        dpg.add_text("Wykres:")
        dpg.add_plot( height=300, width=600, no_inputs=True)

# --- Start GUI ---
dpg.show_viewport()
dpg.set_primary_window("main", True)
dpg.start_dearpygui()
dpg.destroy_context()
