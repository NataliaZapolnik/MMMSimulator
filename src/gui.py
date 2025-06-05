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
#dpg.create_viewport(title="MMMSimulator", width=920, height=650, resizable=False, decorated=True)
dpg.create_viewport(title="MMMSimulator", width=920, height=650, resizable=True, decorated=True)
dpg.setup_dearpygui()

#kolorystyka GUI 
with dpg.theme() as global_theme:
    with dpg.theme_component(dpg.mvAll):
        dpg.add_theme_color(dpg.mvThemeCol_WindowBg, (30, 0, 60, 255))        # ciemne fioletowe tło okna
        dpg.add_theme_color(dpg.mvThemeCol_ChildBg, (40, 0, 80, 255))         # tło child_window
        dpg.add_theme_color(dpg.mvThemeCol_PopupBg, (40, 0, 80, 255))
        dpg.add_theme_color(dpg.mvThemeCol_Border, (100, 0, 150, 255))
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
    font_id = dpg.add_font(FONT_PATH, 12, default_font=True)
    dpg.add_font_range(0x0100, 0x017F, parent=font_id)

with dpg.window(tag="main"):
    dpg.bind_font(font_id)
    with dpg.child_window(width=-1, height=-1, border=False):
        #kontener na cała górną sekcję 
        with dpg.child_window(width=-1, height=200, border=False):
            #with dpg.group(horizontal=True, horizontal_spacing=20):
             with dpg.table(header_row=False, resizable=True, policy=dpg.mvTable_SizingStretchProp, borders_innerV=True, borders_outerV=True):
                dpg.add_table_column()
                dpg.add_table_column()
                dpg.add_table_column()
                with dpg.table_row():
                    # Okno sygnału
                    #segment 1
                    with dpg.group():
                        dpg.add_button(label="Sygnał wejściowy:", enabled=False, width=-1, height=30)
                        dpg.add_combo(tag="signal_selector", label="Sygnał", items=["Sygnał prostokątny", "Sygnał sinusoidalny", "Sygnał trójkątny"], default_value="Sygnał prostokątny")
                        dpg.add_input_float(tag="amplitude_input", label="Amplituda", default_value=1.0)
                        dpg.add_input_float(tag="frequency_input", label="Częstotliwość", default_value=1.0)
                    # Parametry regulatora PI
                    #segment 2
                    with dpg.group():
                        dpg.add_button(label="Parametry układu:", enabled=False, width=-1, height=30)
                        dpg.add_input_float(tag="a1_input", label="a1", default_value=0.0)
                        dpg.add_input_float(tag="a0_input", label="a0", default_value=0.0)
                        dpg.add_input_float(tag="b2_input", label="b2", default_value=0.0)
                        dpg.add_input_float(tag="b1_input", label="b1", default_value=0.0)
                        dpg.add_input_float(tag="b0_input", label="b0", default_value=0.0)
                        dpg.add_input_float(tag="kp_input", label="Kp", default_value=0.0)
                        dpg.add_input_float(tag="ki_input", label="Ki", default_value=0.0)


                    # Czas symulacji
                    #segment 3
                    with dpg.group():
                        dpg.add_button(label="Parametry symulacji:", enabled=False, width=-1, height=30)
                        dpg.add_input_float(tag="t", label="t[s]", default_value=10.0)
                        dpg.add_input_float(tag="dt", label="dt[s]", default_value=0.1)
                
        
        #przycisk start
        with dpg.group(horizontal=True):
            dpg.add_button(label="START", callback=run_simulation_callback, width=100, height=40)
            dpg.add_spacer(width=20)
            dpg.add_checkbox(tag="show_output", label="Sygnał wyjściowy", default_value=True)
            dpg.add_checkbox(tag="show_input", label="Sygnał wejściowy", default_value=False)
            dpg.add_checkbox(tag="show_error", label="Uchyb", default_value=False)
        #wykres na dole 
        with dpg.child_window(tag="plot", width=-1, height=-1, border=False ):
            dpg.add_text("Wykres:")
            #dpg.add_plot( height=300, width=600, no_inputs=True)
            dpg.add_plot( height=-1, width=-1, no_inputs=True)

# --- Start GUI ---
dpg.show_viewport()
dpg.set_primary_window("main", True)
dpg.start_dearpygui()
dpg.destroy_context()
