import numpy as np
import matplotlib.pyplot as plt
from scipy.fft import fft
import sounddevice as sd
from matplotlib.animation import FuncAnimation

# Parameters
sampling_rate = 48000  # Sampling rate in Hz
block_duration = 0.05  # Block duration in seconds
block_size = int(sampling_rate * block_duration)  # Number of samples per block

# Frequency axis
frequencies = np.fft.fftfreq(block_size, 1 / sampling_rate)[:block_size // 2]

# Create a figure for plotting
fig, ax = plt.subplots(figsize=(10, 4))
line, = ax.plot(frequencies, np.zeros(block_size // 2))  # Initialize plot with zeros

# Configure plot
ax.set_xlim(0, sampling_rate / 2)
ax.set_ylim(0, 1)
ax.set_xlabel('Frequency [Hz]')
ax.set_ylabel('Magnitude')
ax.set_title('Real-time Audio Spectrum')
ax.grid(True)

# Buffer to store audio blocks
audio_buffer = np.zeros(block_size)

# Audio input stream callback
def audio_callback(indata, frames, time, status):
    global audio_buffer
    if status:
        print(status, flush=True)  # Log any warnings like "input overflow"
    audio_buffer = indata[:, 0]  # Copy the audio data into the buffer

# This function updates the plot in real time
def update_plot(frame):
    global audio_buffer

    # Compute the FFT of the latest audio block
    fft_values = fft(audio_buffer)
    fft_magnitude = np.abs(fft_values[:block_size // 2])

    # Update the line plot with the new FFT data
    line.set_ydata(fft_magnitude)

    # Dynamically adjust the y-axis to fit the data
    ax.set_ylim(0, np.max(fft_magnitude) + 1)
    
    return line,

# Open the audio stream
with sd.InputStream(channels=1, callback=audio_callback, samplerate=sampling_rate, blocksize=block_size):
    # Use FuncAnimation to update the plot
    ani = FuncAnimation(fig, update_plot, blit=True, interval=50)

    plt.show()