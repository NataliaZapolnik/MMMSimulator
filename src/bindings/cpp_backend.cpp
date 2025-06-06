#include <vector>
#include <math.h>
#include <fstream>
#include <corecrt_math_defines.h>

enum class InputSignalType{
    SINUS, SQUARE, TRIANGLE
};

class Parameters {
public:
    double a1 = 0, a0 = 0;
    double b2 = 0, b1 = 0, b0 = 0;
    double kp = 0, ki = 0;
    double amplitude = 1.0;
    double frequency = 1.0;
    double duration = 10.0;
    double dt = 0.01;
};

class Simulation{
public:
    Simulation(InputSignalType signal_type, Parameters parameters) 
    : signal(signal_type)
    {
       switch(signal_type){
        case InputSignalType::SINUS : 
            input_signal = sinus(parameters);
            break;
        case InputSignalType::SQUARE :
            input_signal = square(parameters);
            break;
        case InputSignalType::TRIANGLE :
            input_signal = triangle(parameters);
            break;
       } 
       start_simulation(parameters);
    };

    const std::vector<double>& get_input() const { return input_signal; }
    const std::vector<double>& get_output() const { return output_signal; }
    const std::vector<double>& get_error() const { return error_signal; }
    const std::vector<double>& get_control() const { return control_signal; }

private: 
    InputSignalType signal;
    std::vector<double> input_signal;
    std::vector<double> output_signal;
    std::vector<double> error_signal;
    std::vector<double> control_signal;
        
    std::vector<double> square(Parameters params) {
        std::vector<double> signal;
        for (double t = 0.0; t <= params.duration; t += params.dt) {
            signal.push_back((sin(2 * M_PI * params.frequency * t) >= 0) ? params.amplitude : 0.0);
        }
        return signal;
    }

    std::vector<double> sinus(Parameters params) {
        std::vector<double> signal;
        for (double t = 0.0; t <= params.duration; t += params.dt) {
            signal.push_back(params.amplitude * sin(2 * M_PI * params.frequency * t));
        }
        return signal;
    }

    std::vector<double> triangle(Parameters params) {
        std::vector<double> signal;
        double T = 1.0 / params.frequency;
        for (double t = 0.0; t <= params.duration; t += params.dt) {
            double cycle = fmod(t, T) / T;
            double value = (cycle < 0.5) ? (4 * params.amplitude * cycle - params.amplitude) : (-4 * params.amplitude * (cycle - 0.5) + params.amplitude);
            signal.push_back(value);
        }
        return signal;
    }

   void start_simulation(Parameters params) {
        int N = static_cast<int>(params.duration / params.dt);
        output_signal.assign(N, 0.0);
        error_signal.assign(N, 0.0);
        control_signal.assign(N, 0.0);

        for (int k = 2; k < N; ++k) {
            // Oblicz uchyb
            error_signal[k] = input_signal[k] - output_signal[k - 1];

            // Regulator PI
            control_signal[k] = control_signal[k - 1]
                + params.kp * (error_signal[k] - error_signal[k - 1])
                + params.ki * params.dt * error_signal[k];

            // Model ARX – transmitancja obiektu
            output_signal[k] = -params.a1 * output_signal[k - 1]
                - params.a0 * output_signal[k - 2]
                + params.b2 * control_signal[k]
                + params.b1 * control_signal[k - 1]
                + params.b0 * control_signal[k - 2];
        }
    }

};

void export_to_csv(const std::vector<double>& signal, const std::string& filename, double dt = 0.01) {
    std::ofstream file(filename);
    if (!file.is_open()) return;
    file << "time,value\n";
    for (int i = 0; i < signal.size(); i++) {
        file << (i * dt) << "," << signal[i] << "\n";
    }
    file.close();
}

#include <pybind11/stl.h>

namespace py = pybind11;

PYBIND11_MODULE(cpp_backend, m) {
    py::enum_<InputSignalType>(m, "InputSignalType")
        .value("SINUS", InputSignalType::SINUS)
        .value("SQUARE", InputSignalType::SQUARE)
        .value("TRIANGLE", InputSignalType::TRIANGLE)
        .export_values();

    py::class_<Parameters>(m, "Parameters")
        .def(py::init<>())
        .def_readwrite("a1", &Parameters::a1)
        .def_readwrite("a0", &Parameters::a0)
        .def_readwrite("b2", &Parameters::b2)
        .def_readwrite("b1", &Parameters::b1)
        .def_readwrite("b0", &Parameters::b0)
        .def_readwrite("kp", &Parameters::kp)
        .def_readwrite("ki", &Parameters::ki)
        .def_readwrite("amplitude", &Parameters::amplitude)
        .def_readwrite("frequency", &Parameters::frequency)
        .def_readwrite("duration", &Parameters::duration)
        .def_readwrite("dt", &Parameters::dt);

    py::class_<Simulation>(m, "Simulation")
        .def(py::init<InputSignalType, Parameters>())
        .def("get_input", &Simulation::get_input)
        .def("get_output", &Simulation::get_output)
        .def("get_error", &Simulation::get_error)
        .def("get_control", &Simulation::get_control);

    m.def("export_to_csv", &export_to_csv, py::arg("signal"), py::arg("file") = 0.01);
}