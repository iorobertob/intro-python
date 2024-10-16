import numpy as np
import matplotlib.pyplot as plt
from scipy.fft import fft
import sounddevice as sd
from matplotlib.animation import FuncAnimation

# Parameters
sampling_rate = 48000  # Sampling rate in Hz
block_duration = 0.05  # Block duration in seconds
block_size = int(sampling_rate * block_duration)  # Number of samples per block

# Set the scale mode (choose "log" for logarithmic, "linear" for linear scale)
frequency_scale = 'log'  # Options: 'linear' or 'log'
amplitude_scale = 'log'  # Options: 'linear' or 'log'

# Frequency axis
frequencies = np.fft.fftfreq(block_size, 1 / sampling_rate)[:block_size // 2]

# Adjust the frequency axis for logarithmic scale (only use positive frequencies)
if frequency_scale == 'log':
    # Exclude zero and negative frequencies
    positive_frequencies = frequencies[frequencies > 0]
else:
    positive_frequencies = frequencies

# Create a figure for plotting
fig, ax = plt.subplots(figsize=(10, 4))
line, = ax.plot(positive_frequencies, np.zeros(len(positive_frequencies)))  # Initialize plot with zeros

# Configure plot axes
ax.set_xlabel('Frequency [Hz]')
ax.set_ylabel('Magnitude')

if frequency_scale == 'log':
    ax.set_xscale('log')
    ax.set_xlim([positive_frequencies[0], sampling_rate / 2])
else:
    ax.set_xlim(0, sampling_rate / 2)

if amplitude_scale == 'log':
    ax.set_ylabel('Magnitude [dB]')
    ax.set_ylim(-100, 0)  # Decibels range
else:
    ax.set_ylabel('Magnitude')
    ax.set_ylim(0, 1)

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

    if frequency_scale == 'log':
        # Exclude zero and negative frequencies from fft_magnitude to match the length of `positive_frequencies`
        fft_magnitude = ff
        t_magnitude[frequencies > 0]

    # Apply logarithmic transformation for amplitude if needed
    if amplitude_scale == 'log':
        fft_magnitude = 20 * np.log10(np.maximum(fft_magnitude, 1e-10))  # Convert to decibels, avoid log(0)

    # Update the line plot with the new FFT data
    line.set_ydata(fft_magnitude)

    # Dynamically adjust the y-axis for linear scale if necessary
    if amplitude_scale == 'linear':
        ax.set_ylim(0, np.max(fft_magnitude) + 1)
    
    return line,

# Open the audio stream
with sd.InputStream(channels=1, callback=audio_callback, samplerate=sampling_rate, blocksize=block_size):
    # Use FuncAnimation to update the plot
    ani = FuncAnimation(fig, update_plot, blit=True, interval=50, cache_frame_data=False)

    plt.show()