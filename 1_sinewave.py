import matplotlib
import numpy as np
import matplotlib.pyplot as plt
from scipy.io.wavfile import write
from scipy.fft import fft, fftfreq
import sys

# np.set_printoptions(threshold=sys.maxsize)

# Parameters
duration  = 10  # seconds
frequency = 340  # A4 note, 440 Hz!1
sampling_rate = 48000  # Standard CD-quality sampling rate

# Generate time array
t = np.linspace(0, duration, int(sampling_rate * duration), endpoint=False)

# Generate sine wave
sine_wave = 0.5 * np.sin(2 * np.pi * frequency * t)

# Plot the sine wave
plt.figure(figsize=(10, 4))
plt.plot(t, sine_wave)
plt.title(f"Sine Wave at {frequency} Hz")
plt.xlabel("Time [s]")
plt.ylabel("Amplitude")
plt.xlim(0, 0.02)  # Zoom into the first 20 ms for better visualization
plt.grid(True)
plt.show(block=False)  # Non-blocking plot

# Save sine wave to a WAV file
write('sine_wave.wav', sampling_rate, np.int16(sine_wave * 32767))

# Calculate FFT
fft_values = fft(sine_wave)
fft_freq   = fftfreq(len(sine_wave), 1/sampling_rate)

# Plot the FFT
plt.figure(figsize=(10, 4))
plt.plot(fft_freq[:len(fft_freq)//2], np.abs(fft_values)[:len(fft_values)//2])
plt.title("FFT of Sine Wave")
plt.xlabel("Frequency [Hz]")
plt.ylabel("Magnitude")
plt.grid(True)
plt.show(block=False)  # Non-blocking plot

# Continue with other tasks or execution
print("Execution continues...")
input("Press [enter] to continue.")
# Add your additional code here
# The plots will remain open until you close them manually