#include <vector>
#include <math.h>
#include <corecrt_math_defines.h>
using namespace std;

class Signal {
public:

};

enum class InputSignalType{
    SINUS, SQUARE, TRIANGLE
};

class Simulation{
public:
    Simulation(InputSignalType signal_type, Parameters signal_parameters, Parameters schema_parameters, Parameters pi_parameters) 
    : signal(signal_type), signal_params(signal_parameters), schema_params(schema_parameters), pi_params(pi_parameters)
    {
       switch(signal_type){
        case InputSignalType::SINUS : 
            input_signal = sinus(signal_parameters);
            break;
        case InputSignalType::SQUARE :
            input_signal = square(signal_parameters);
            break;
        case InputSignalType::TRIANGLE :
            input_signal = triangle(signal_parameters);
            break;
       } 

    };

    const vector<double>& get_output() const { return output_signal; }
    const vector<double>& get_error() const { return error_signal; }
    const vector<double>& get_control() const { return control_signal; }

private: 
    vector <double> input_signal;
    vector<double> output_signal;
    vector<double> error_signal;
    vector<double> control_signal;
    Parameters signal_params;
    InputSignalType signal;
    Parameters schema_params;
    Parameters pi_params;
        
     vector<double> square(Parameters params) {
        vector<double> signal;
        for (double t = 0.0; t <= params.duration; t += params.dt) {
            signal.push_back((sin(2 * M_PI * params.frequency * t) >= 0) ? params.amplitude : 0.0);
        }
        return signal;
    }

    vector<double> sinus(Parameters params) {
        vector<double> signal;
        for (double t = 0.0; t <= params.duration; t += params.dt) {
            signal.push_back(params.amplitude * sin(2 * M_PI * params.frequency * t));
        }
        return signal;
    }

    vector<double> triangle(Parameters params) {
        vector<double> signal;
        double T = 1.0 / params.frequency;
        for (double t = 0.0; t <= params.duration; t += params.dt) {
            double cycle = fmod(t, T) / T;
            double value = (cycle < 0.5) ? (4 * params.amplitude * cycle - params.amplitude) : (-4 * params.amplitude * (cycle - 0.5) + params.amplitude);
            signal.push_back(value);
        }
        return signal;
    }

   void start_simulation() {
        int N = static_cast<int>(signal_params.duration / signal_params.dt);
        output_signal.assign(N, 0.0);
        error_signal.assign(N, 0.0);
        control_signal.assign(N, 0.0);

        for (int k = 2; k < N; ++k) {
            // Oblicz uchyb
            error_signal[k] = input_signal[k] - output_signal[k - 1];

            // Regulator PI
            control_signal[k] = control_signal[k - 1]
                + pi_params.kp * (error_signal[k] - error_signal[k - 1])
                + pi_params.ki * signal_params.dt * error_signal[k];

            // Model ARX – transmitancja obiektu
            output_signal[k] = -schema_params.a1 * output_signal[k - 1]
                - schema_params.a0 * output_signal[k - 2]
                + schema_params.b2 * control_signal[k]
                + schema_params.b1 * control_signal[k - 1]
                + schema_params.b0 * control_signal[k - 2];
        }
    }

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