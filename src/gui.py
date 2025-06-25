from dearpygui import dearpygui as dpg 
from config import FONT_PATH
import cpp_backend as sim

def run_simulation_callback():
    params = sim.Parameters()
    params.amplitude = dpg.get_value("amplitude_input")
    params.frequency = dpg.get_value("frequency_input")
    params.a0 = dpg.get_value("a0_input")
    params.a1 = dpg.get_value("a1_input")
    params.b2 = dpg.get_value("b2_input")
    params.b1 = dpg.get_value("b1_input")
    params.b0 = dpg.get_value("b0_input")
    params.kp = dpg.get_value("kp_input")
    params.ki = dpg.get_value("ki_input")
    params.dt = dpg.get_value("dt_input")
    params.duration = dpg.get_value("t_input")
    params.impulse_duration = dpg.get_value("impulse_duration_input")
    signal = dpg.get_value("signal_selector")

    #dynamiczne pobieranie parametrów
    if signal == "Sygnał impulsowy":
        params.impulse_duration = dpg.get_value("impulse_duration_input")
        params.frequency = 1.0 
    else:
        params.frequency = dpg.get_value("frequency_input")
        params.impulse_duration = 1.0 
   

    if signal == "Sygnał prostokątny":
        simulation = sim.Simulation(sim.InputSignalType.SQUARE, params)
    elif signal == "Sygnał sinusoidalny":
        simulation = sim.Simulation(sim.InputSignalType.SINUS, params)
    elif signal == "Sygnał trójkątny":
        simulation = sim.Simulation(sim.InputSignalType.TRIANGLE, params)
    else:
        simulation = sim.Simulation(sim.InputSignalType.IMPULSE, params)

    
    output = simulation.get_output()
    input_signal = simulation.get_input()
    error = simulation.get_error()
    
    dt = params.dt
    N = len(output)
    time = [i * dt for i in range(N)]

    dpg.delete_item("y_axis", children_only=True)
    dpg.set_axis_limits("x_axis", 0, params.duration)

    if dpg.get_value("show_output"):
        dpg.add_line_series(time, output, label="Wyjście", parent="y_axis")
    if dpg.get_value("show_input") and input_signal:
        dpg.add_line_series(time, input_signal, label="Wejście", parent="y_axis")
    if dpg.get_value("show_error"):
        dpg.add_line_series(time, error, label="Uchyb", parent="y_axis")
    if dpg.get_value("csv"):
        sim.export_to_csv(output, "data/Wykres.csv", params.dt)

#callback do dynamicznego pokazwyania parametrów sygnału
def signal_selector_callback():
    signal = dpg.get_value("signal_selector")
    if signal == "Sygnał impulsowy":
        dpg.hide_item("frequency_input")
        dpg.show_item("impulse_duration_input")
    else:
        dpg.show_item("frequency_input")
        dpg.hide_item("impulse_duration_input")


# --- Tworzenie GUI ---
dpg.create_context()
dpg.create_viewport(title="MMMSimulator", width=920, height=650, resizable=True, decorated=True)
dpg.setup_dearpygui()

#kolorystyka GUI 
with dpg.theme() as global_theme:
    with dpg.theme_component(dpg.mvAll):
        dpg.add_theme_color(dpg.mvThemeCol_WindowBg, (30, 0, 60, 255))        # ciemne fioletowe tło okna
        dpg.add_theme_color(dpg.mvThemeCol_ChildBg, (40, 0, 80, 255))         # tło child_window
        dpg.add_theme_color(dpg.mvThemeCol_PopupBg, (40, 0, 80, 255))
        dpg.add_theme_color(dpg.mvThemeCol_Border, (0, 0, 0, 0))
        dpg.add_theme_color(dpg.mvThemeCol_Text, (255, 255, 255, 255))        # biały tekst
        dpg.add_theme_color(dpg.mvThemeCol_Button, (200, 0, 200, 255))        # fioletowy przycisk
        dpg.add_theme_color(dpg.mvThemeCol_ButtonHovered, (255, 0, 255, 255)) # jaśniejszy po najechaniu
        dpg.add_theme_color(dpg.mvThemeCol_ButtonActive, (150, 0, 150, 255))  # ciemniejszy po kliknięciu
        dpg.add_theme_color(dpg.mvThemeCol_FrameBg, (60, 0, 100, 255))        # tło inputów
        dpg.add_theme_color(dpg.mvThemeCol_CheckMark, (255, 0, 255, 255))     # kolor ptaszka w checkboxie
        dpg.add_theme_color(dpg.mvThemeCol_SliderGrab, (255, 0, 255, 255))
        dpg.add_theme_color(dpg.mvThemeCol_SliderGrabActive, (200, 0, 200, 255))
        dpg.add_theme_color(dpg.mvThemeCol_Header, (100, 0, 150, 255))
        dpg.add_theme_color(dpg.mvThemeCol_HeaderHovered, (150, 0, 200, 255))
        dpg.add_theme_color(dpg.mvThemeCol_HeaderActive, (200, 0, 255, 255))


dpg.bind_theme(global_theme)

with dpg.font_registry():
    font_id = dpg.add_font(FONT_PATH, 15, default_font=True)
    dpg.add_font_range(0x0100, 0x017F, parent=font_id)

with dpg.window(tag="main"):
    dpg.bind_font(font_id)
    with dpg.child_window(width=-1, height=-1, border=False):
        #kontener na cała górną sekcję 
        with dpg.child_window(width=-1, height=300, border=False):
            #with dpg.group(horizontal=True, horizontal_spacing=20):
             with dpg.table(header_row=False, resizable=False, policy=dpg.mvTable_SizingStretchProp, borders_innerV=False, borders_outerV=False, borders_innerH=False, borders_outerH=False):
                dpg.add_table_column(init_width_or_weight=1)
                dpg.add_table_column(init_width_or_weight=1)
                dpg.add_table_column(init_width_or_weight=1)
                with dpg.table_row():
                    # Okno sygnału
                    #segment 1
                    with dpg.group():
                        dpg.add_button(label="Sygnał wejściowy:", enabled=False, height=30)
                        dpg.add_spacer(height=10)
                        dpg.add_combo(tag="signal_selector", label="Sygnał", items=["Sygnał prostokątny", "Sygnał sinusoidalny", "Sygnał trójkątny", "Sygnał impulsowy"], default_value="Sygnał prostokątny", callback=signal_selector_callback)
                        dpg.add_input_float(tag="amplitude_input", label="A", default_value=1.0, min_value=0.0, min_clamped=True, step=0.1)
                        dpg.add_input_float(tag="frequency_input", label="f[Hz]", default_value=1.0, min_value=0.0, min_clamped=True, step=1.0)
                        dpg.add_input_float(tag="impulse_duration_input", label="ti[s]", default_value=1.0, min_value=0.0, min_clamped=True, step=0.1, show=False)
                    # Parametry regulatora PI
                    #segment 2
                    with dpg.group():
                        dpg.add_button(label="Parametry układu:", enabled=False, height=30)
                        dpg.add_spacer(height=10)
                        dpg.add_input_float(tag="a1_input", label="a1", default_value=1.0)
                        dpg.add_input_float(tag="a0_input", label="a0", default_value=1.0)
                        dpg.add_input_float(tag="b2_input", label="b2", default_value=1.0)
                        dpg.add_input_float(tag="b1_input", label="b1", default_value=1.0)
                        dpg.add_input_float(tag="b0_input", label="b0", default_value=1.0)
                        dpg.add_spacer(height=13)
                        dpg.add_input_float(tag="kp_input", label="Kp", default_value=1.0)
                        dpg.add_input_float(tag="ki_input", label="Ki", default_value=1.0)


                    # Czas symulacji
                    #segment 3
                    with dpg.group():
                        dpg.add_button(label="Parametry symulacji:", enabled=False, height=30)
                        dpg.add_spacer(height=10)
                        dpg.add_input_float(tag="t_input", label="t[s]", default_value=10.0, min_value=0.0, min_clamped=True)
                        dpg.add_input_float(tag="dt_input", label="dt[s]", default_value=0.01, min_value=0.0000001,min_clamped=True, step=0.01)
                
        
        #przycisk start
        with dpg.group(horizontal=True):
            dpg.add_button(label="START", callback=run_simulation_callback, width=100, height=30)
            dpg.add_spacer(width=60)
            dpg.add_checkbox(tag="show_output", label="Sygnał wyjściowy", default_value=True)
            dpg.add_spacer(width=20)
            dpg.add_checkbox(tag="show_input", label="Sygnał wejściowy", default_value=False)
            dpg.add_spacer(width=20)
            dpg.add_checkbox(tag="show_error", label="Uchyb", default_value=False)
            dpg.add_spacer(width=80)
            dpg.add_checkbox(tag="csv", label="Zapisz do CSV", default_value=False)

        #wykres na dole 
        with dpg.child_window(tag="plot_window", width=-1, height=-1, border=False ):
            with dpg.plot(tag="plot", height=-1, width=-1, no_inputs=False):
                dpg.add_plot_axis(dpg.mvXAxis, label="Czas", tag="x_axis")
                dpg.add_plot_axis(dpg.mvYAxis, label="Wartość", tag="y_axis")
                dpg.set_axis_limits("x_axis", 0, 10)
dpg.show_viewport()
dpg.set_primary_window("main", True)
dpg.start_dearpygui()
dpg.destroy_context()