"""
Guo Chaoran - Teaching Knowledge GUI
Task 10: Sine Signal Spectrum Leakage
Task 14: Sampling Frequency and Spectrum Relation
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter as tk
from tkinter import ttk
import matplotlib.gridspec as gridspec


# ==================== Task 10: Sine Signal Spectrum Leakage ====================

class SpectrumLeakageApp:
    def __init__(self, parent):
        self.parent = parent
        self.running = False
        self.current_freq = 0
        self.setup_ui()

    def setup_ui(self):
        # Grid layout: display area 7 parts, parameter area 3 parts
        self.parent.rowconfigure(0, weight=7)
        self.parent.rowconfigure(1, weight=3)
        self.parent.columnconfigure(0, weight=1)

        # Display area
        display_frame = tk.Frame(self.parent, bg='#f0f0f0')
        display_frame.grid(row=0, column=0, sticky='nsew', padx=5, pady=5)

        # Create chart - horizontal layout
        self.fig = plt.figure(figsize=(12, 6))
        self.fig.suptitle('Task 10: Sine Signal Spectrum Leakage', fontsize=14, fontweight='bold')
        gs = gridspec.GridSpec(1, 2)
        self.ax1 = self.fig.add_subplot(gs[0, 0])  # Left: full spectrum
        self.ax2 = self.fig.add_subplot(gs[0, 1])  # Right: zoomed

        self.canvas = FigureCanvasTkAgg(self.fig, master=display_frame)
        self.canvas.get_tk_widget().pack(fill='both', expand=True)

        # Parameter input area
        param_frame = tk.Frame(self.parent, bg='#e8e8e8', relief='sunken', bd=2)
        param_frame.grid(row=1, column=0, sticky='nsew', padx=5, pady=5)

        # Parameter area title
        title_label = tk.Label(param_frame, text="Parameter Settings", font=('Arial', 12, 'bold'), bg='#e8e8e8')
        title_label.grid(row=0, column=0, columnspan=5, pady=(5, 10))

        # Row 1: Sampling frequency and Num Samples
        ttk.Label(param_frame, text="Sampling Freq (Hz):").grid(row=1, column=0, sticky='e', padx=20, pady=8)
        self.fs_var = tk.StringVar(value="1000")
        ttk.Entry(param_frame, textvariable=self.fs_var, width=12).grid(row=1, column=1, sticky='w', padx=20, pady=8)

        ttk.Label(param_frame, text="Num Samples:").grid(row=1, column=2, sticky='e', padx=20, pady=8)
        self.N_var = tk.StringVar(value="100")
        ttk.Entry(param_frame, textvariable=self.N_var, width=12).grid(row=1, column=3, sticky='w', padx=20, pady=8)

        # Row 2: Start frequency and End frequency
        ttk.Label(param_frame, text="Start Freq (Hz):").grid(row=2, column=0, sticky='e', padx=20, pady=8)
        self.f_start_var = tk.StringVar(value="50")
        ttk.Entry(param_frame, textvariable=self.f_start_var, width=12).grid(row=2, column=1, sticky='w', padx=20, pady=8)

        ttk.Label(param_frame, text="End Freq (Hz):").grid(row=2, column=2, sticky='e', padx=20, pady=8)
        self.f_end_var = tk.StringVar(value="55")
        ttk.Entry(param_frame, textvariable=self.f_end_var, width=12).grid(row=2, column=3, sticky='w', padx=20, pady=8)

        # Column 4: Start/Stop button
        self.start_btn = ttk.Button(param_frame, text="Start", command=self.toggle_animation, width=12)
        self.start_btn.grid(row=1, column=4, rowspan=2, padx=30, pady=8)

        # Initial plot
        self.plot_static()

    def plot_static(self):
        """Initialize static chart"""
        self.ax1.clear()
        self.ax1.set_title('Sine Signal Spectrum (Click "Start" to play)', fontsize=12)
        self.ax1.set_xlabel('Freq (Hz)')
        self.ax1.set_ylabel('Amplitude')
        self.ax1.grid(True, alpha=0.3)

        self.ax2.clear()
        self.ax2.set_title('Zoomed Spectrum (bar)', fontsize=12)
        self.ax2.set_xlabel('Freq (Hz)')
        self.ax2.set_ylabel('Amplitude')
        self.ax2.grid(True, alpha=0.3, axis='y')

        self.fig.tight_layout()
        self.canvas.draw()

    def toggle_animation(self):
        if self.running:
            self.running = False
            self.start_btn.config(text="Start")
        else:
            try:
                self.validate_params()
                self.running = True
                self.start_btn.config(text="Stop")
                self.run_animation()
            except ValueError as e:
                self.show_error(str(e))

    def validate_params(self):
        fs = float(self.fs_var.get())
        f_start = float(self.f_start_var.get())
        f_end = float(self.f_end_var.get())

        if abs(f_start) >= fs / 2 or abs(f_end) >= fs / 2:
            raise ValueError("Start and end frequency must be less than fs/2")
        if abs(f_end - f_start) > 20:
            raise ValueError("Frequency difference must be less than 20Hz")

    def run_animation(self):
        if not self.running:
            return

        try:
            fs = float(self.fs_var.get())
            N = int(self.N_var.get())
            f_start = float(self.f_start_var.get())
            f_end = float(self.f_end_var.get())

            # Dynamic frequency change
            if self.current_freq == 0:
                self.current_freq = f_start

            # Frequency step
            freq_step = 0.5
            self.current_freq += freq_step
            if self.current_freq > f_end:
                self.current_freq = f_start

            # Generate sine signal
            t = np.arange(N) / fs
            f = self.current_freq
            signal = np.sin(2 * np.pi * f * t)

            # Calculate FFT
            fft_result = np.fft.fft(signal)
            freq_axis = np.fft.fftfreq(N, 1 / fs)

            # Get positive frequency
            positive_freq_idx = freq_axis >= 0
            freq_positive = freq_axis[positive_freq_idx]
            amplitude = np.abs(fft_result[positive_freq_idx]) * 2 / N
            if len(amplitude) > 0:
                amplitude[0] = amplitude[0] / 2

            # Plot spectrum (line)
            self.ax1.clear()
            self.ax1.plot(freq_positive, amplitude, 'b-', linewidth=1)
            self.ax1.set_title(f'Sine Signal Spectrum (f={f:.1f}Hz)', fontsize=12)
            self.ax1.set_xlabel('Freq (Hz)')
            self.ax1.set_ylabel('Amplitude')
            self.ax1.grid(True, alpha=0.3)

            # Plot zoomed spectrum (bar)
            # Range: current sine freq * (1±5%)
            self.ax2.clear()
            f_min = f * 0.95
            f_max = f * 1.05

            local_idx = (freq_positive >= f_min) & (freq_positive <= f_max)
            freq_local = freq_positive[local_idx]
            amplitude_local = amplitude[local_idx]

            if len(freq_local) > 0:
                self.ax2.bar(freq_local, amplitude_local, width=0.3, color='red', alpha=0.7)
            self.ax2.set_title(f'Zoomed (Range: {f_min:.1f}-{f_max:.1f}Hz, ±5%)', fontsize=12)
            self.ax2.set_xlabel('Freq (Hz)')
            self.ax2.set_ylabel('Amplitude')
            self.ax2.grid(True, alpha=0.3, axis='y')

            self.fig.tight_layout()
            self.canvas.draw()

            if self.running:
                self.parent.after(100, self.run_animation)

        except Exception as e:
            self.running = False
            self.start_btn.config(text="Start")
            self.show_error(str(e))

    def show_error(self, msg):
        error_win = tk.Toplevel(self.parent)
        error_win.title("Error")
        ttk.Label(error_win, text=msg, padding=20).pack()
        ttk.Button(error_win, text="OK", command=error_win.destroy).pack()


# ==================== Task 14: Sampling Frequency and Spectrum Relation ====================

class SamplingSpectrumApp:
    def __init__(self, parent):
        self.parent = parent
        self.keep_history = False
        self.setup_ui()

    def setup_ui(self):
        # Grid layout: display area 7 parts, parameter area 3 parts
        self.parent.rowconfigure(0, weight=7)
        self.parent.rowconfigure(1, weight=3)
        self.parent.columnconfigure(0, weight=1)

        # Display area
        display_frame = tk.Frame(self.parent, bg='#f0f0f0')
        display_frame.grid(row=0, column=0, sticky='nsew', padx=5, pady=5)

        # Create chart - vertical layout
        self.fig = plt.figure(figsize=(10, 8))
        self.fig.suptitle('Task 14: Sampling Frequency and Spectrum Relation', fontsize=14, fontweight='bold')
        gs = gridspec.GridSpec(2, 1)
        self.ax1 = self.fig.add_subplot(gs[0, 0])  # Top: linear scale
        self.ax2 = self.fig.add_subplot(gs[1, 0])  # Bottom: log scale

        self.canvas = FigureCanvasTkAgg(self.fig, master=display_frame)
        self.canvas.get_tk_widget().pack(fill='both', expand=True)

        # Parameter input area
        param_frame = tk.Frame(self.parent, bg='#e8e8e8', relief='sunken', bd=2)
        param_frame.grid(row=1, column=0, sticky='nsew', padx=5, pady=5)

        # Parameter area title
        title_label = tk.Label(param_frame, text="Parameter Settings", font=('Arial', 12, 'bold'), bg='#e8e8e8')
        title_label.grid(row=0, column=0, columnspan=4, pady=(5, 10))

        # Row 1: Signal type, Sampling frequency
        ttk.Label(param_frame, text="Signal Type:").grid(row=1, column=0, sticky='e', padx=10, pady=8)
        self.signal_type_var = tk.StringVar()
        signal_combo = ttk.Combobox(param_frame, textvariable=self.signal_type_var,
                                     values=["Sine (amp=1, period=0.2)", "Single Pulse (width=0.1)"],
                                     state='readonly', width=22)
        signal_combo.grid(row=1, column=1, sticky='w', padx=10, pady=8)
        signal_combo.current(0)

        ttk.Label(param_frame, text="Sampling Freq (Hz):").grid(row=1, column=2, sticky='e', padx=10, pady=8)
        self.fs_var = tk.StringVar(value="100")
        ttk.Entry(param_frame, textvariable=self.fs_var, width=12).grid(row=1, column=3, sticky='w', padx=10, pady=8)

        # Row 2: Frequency type (radio buttons)
        ttk.Label(param_frame, text="Freq Type:").grid(row=2, column=0, sticky='e', padx=10, pady=8)
        self.freq_type_var = tk.StringVar(value="Digital Freq")
        radio_frame = tk.Frame(param_frame, bg='#e8e8e8')
        radio_frame.grid(row=2, column=1, columnspan=2, sticky='w', padx=10, pady=8)
        ttk.Radiobutton(radio_frame, text="Digital Freq", variable=self.freq_type_var,
                        value="Digital Freq").pack(side='left', padx=5)
        ttk.Radiobutton(radio_frame, text="Analog Freq", variable=self.freq_type_var,
                        value="Analog Freq").pack(side='left', padx=5)

        # Keep history checkbox
        self.keep_history_var = tk.BooleanVar(value=False)
        ttk.Checkbutton(param_frame, text="Keep History",
                        variable=self.keep_history_var).grid(row=2, column=3, sticky='w', padx=10, pady=8)

        # Row 3: Display button
        display_btn = ttk.Button(param_frame, text="Display", command=self.plot_spectrum, width=15)
        display_btn.grid(row=3, column=0, columnspan=4, pady=15)

        # Initial plot
        self.plot_static()

    def plot_static(self):
        """Initialize static chart"""
        self.ax1.clear()
        self.ax1.set_title('Signal Spectrum (Linear Scale)', fontsize=12)
        self.ax1.set_xlabel('Freq')
        self.ax1.set_ylabel('Amplitude')
        self.ax1.grid(True, alpha=0.3)

        self.ax2.clear()
        self.ax2.set_title('Signal Spectrum (Log Scale, dB)', fontsize=12)
        self.ax2.set_xlabel('Freq')
        self.ax2.set_ylabel('Amplitude (dB)')
        self.ax2.grid(True, alpha=0.3)

        self.fig.tight_layout()
        self.canvas.draw()

    def plot_spectrum(self):
        try:
            signal_type = self.signal_type_var.get()
            fs = float(self.fs_var.get())
            freq_type = self.freq_type_var.get()
            keep_history = self.keep_history_var.get()

            # Sampling parameters
            duration = 1.0
            t = np.arange(int(fs * duration)) / fs

            # Generate signal
            if "Sine" in signal_type:
                f0 = 5  # period 0.2s -> freq 5Hz
                signal = np.sin(2 * np.pi * f0 * t)
                signal_name = f'Sine (f={f0}Hz)'
            else:
                pulse_width = 0.1
                signal = np.zeros_like(t)
                pulse_samples = int(pulse_width * fs)
                signal[:pulse_samples] = 1
                signal_name = f'Single Pulse (width={pulse_width}s)'

            # Calculate FFT
            N = len(signal)
            fft_result = np.fft.fft(signal)
            freq_axis = np.fft.fftfreq(N, 1 / fs)

            positive_freq_idx = freq_axis >= 0
            freq_positive = freq_axis[positive_freq_idx]
            amplitude = np.abs(fft_result[positive_freq_idx]) * 2 / N
            if len(amplitude) > 0:
                amplitude[0] = amplitude[0] / 2

            # Frequency axis type
            if freq_type == "Digital Freq":
                freq_display = freq_positive / fs
                xlabel = 'Digital Freq (cycles/sample)'
            else:
                freq_display = freq_positive
                xlabel = 'Analog Freq (Hz)'

            # Clear old plots
            if not keep_history:
                self.ax1.clear()
                self.ax2.clear()
                self.ax1.set_title('Signal Spectrum (Linear Scale)', fontsize=12)
                self.ax1.set_xlabel(xlabel)
                self.ax1.set_ylabel('Amplitude')
                self.ax1.grid(True, alpha=0.3)
                self.ax2.set_title('Signal Spectrum (Log Scale, dB)', fontsize=12)
                self.ax2.set_xlabel(xlabel)
                self.ax2.set_ylabel('Amplitude (dB)')
                self.ax2.grid(True, alpha=0.3)

            # Plot linear scale
            self.ax1.plot(freq_display, amplitude, linewidth=1, label=signal_name)
            self.ax1.legend()

            # Plot log scale
            amplitude_log = np.maximum(amplitude, 1e-10)
            self.ax2.plot(freq_display, 20 * np.log10(amplitude_log),
                           linewidth=1, label=signal_name)
            self.ax2.legend()

            self.fig.tight_layout()
            self.canvas.draw()

        except Exception as e:
            error_win = tk.Toplevel(self.parent)
            error_win.title("Error")
            ttk.Label(error_win, text=str(e), padding=20).pack()
            ttk.Button(error_win, text="OK", command=error_win.destroy).pack()


# ==================== Main Program ====================

def main():
    root = tk.Tk()
    root.title("Teaching Knowledge GUI - Guo Chaoran")
    root.geometry("1000x800")

    # Create Notebook (tabs)
    notebook = ttk.Notebook(root)
    notebook.pack(fill='both', expand=True, padx=10, pady=10)

    # Task 10: Sine Signal Spectrum Leakage
    app10_frame = tk.Frame(notebook)
    app10 = SpectrumLeakageApp(app10_frame)
    notebook.add(app10_frame, text="Task 10: Spectrum Leakage")

    # Task 14: Sampling Frequency and Spectrum Relation
    app14_frame = tk.Frame(notebook)
    app14 = SamplingSpectrumApp(app14_frame)
    notebook.add(app14_frame, text="Task 14: Sampling & Spectrum")

    root.mainloop()


if __name__ == "__main__":
    main()