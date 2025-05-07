from dearpygui import dearpygui as dpg

# Funkcja callback do przycisku
def run_simulation_callback():
    a1 = dpg.get_value("a1_input")
    a0 = dpg.get_value("a0_input")
    kp = dpg.get_value("kp_input")
    ki = dpg.get_value("ki_input")
    signal = dpg.get_value("signal_selector")

    print(f"Symulacja: a1={a1}, a0={a0}, Kp={kp}, Ki={ki}, sygnał={signal}")
    # W przyszłości: symulacja + aktualizacja wykresu

# --- Tworzenie kontekstu GUI ---
dpg.create_context()
dpg.create_viewport(title='Symulator PI', width=920, height=650)
with dpg.window(label="Symulator PI", width=900, height=600):

    # Górna część z 3 panelami w poziomie
    with dpg.group(horizontal=True):

        with dpg.child_window(width=280, height=160, label="Transmitancja"):
            dpg.add_text("Parametry transmitancji")
            dpg.add_input_float(label="a1", tag="a1_input", default_value=1.0)
            dpg.add_input_float(label="a0", tag="a0_input", default_value=0.0)
            dpg.add_input_float(label="b2", tag="b2_input", default_value=0.0)
            dpg.add_input_float(label="b1", tag="b1_input", default_value=0.0)
            dpg.add_input_float(label="b0", tag="b0_input", default_value=0.0)

        with dpg.child_window(width=280, height=160, label="PI"):
            dpg.add_text("Sterownik PI")
            dpg.add_input_float(label="Kp", tag="kp_input", default_value=1.0)
            dpg.add_input_float(label="Ki", tag="ki_input", default_value=0.5)

        with dpg.child_window(width=280, height=160, label="Sygnał"):
            dpg.add_text("Wejście")
            dpg.add_combo(("Prostokątny", "Trójkątny", "Harmoniczny"), label="Typ sygnału", tag="signal_selector")
            dpg.add_input_float(label="Czas symulacji [s]", tag="czas_symulacji", default_value=10.0)
            dpg.add_button(label="Start symulacji", callback=run_simulation_callback)

    # Dolna część – wykres
    with dpg.child_window(width=-1, height=400):
        with dpg.plot(label="Odpowiedź czasowa", height=-1, width=-1):
            dpg.add_plot_legend()
            dpg.add_plot_axis(dpg.mvXAxis, label="Czas", tag="x_axis")
            with dpg.plot_axis(dpg.mvYAxis, label="Wyjście", tag="y_axis"):
                dpg.add_line_series([], [], label="Odpowiedź", tag="line_series")

# --- Uruchomienie GUI ---
dpg.create_viewport(title='Symulator PI', width=920, height=650)
dpg.setup_dearpygui()
dpg.show_viewport()
dpg.start_dearpygui()
dpg.destroy_context()
