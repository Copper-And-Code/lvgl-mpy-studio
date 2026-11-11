from PySide6.QtCore import QBuffer, QByteArray, QIODevice, QObject

SAMPLE_RATE = 22050
LEVEL = 40            # amplitude of the square wave around 128: a buzzer, not an alarm
MAX_TONE_MS = 3000    # duration of tone() without off()


def square_wave(frequency, milliseconds, rate=SAMPLE_RATE):
    samples = rate * milliseconds // 1000
    half_period = max(1, rate // (2 * frequency))
    return bytes(128 + LEVEL if (index // half_period) % 2 == 0 else 128 - LEVEL for index in range(samples))


class TonePlayer(QObject):
    """Play the buzzer tones; without an audio device it stays silent.

    QtMultimedia loads FFmpeg: it is initialised only at the first sound.
    """

    def __init__(self, parent=None):
        super().__init__(parent)
        self._sink = None
        self._buffer = None
        self._create_sink = None
        self._prepared = False

    def _prepare(self):
        self._prepared = True
        try:
            from PySide6.QtMultimedia import QAudioFormat, QAudioSink, QMediaDevices
        except ImportError:
            return
        device = QMediaDevices.defaultAudioOutput()
        audio_format = QAudioFormat()
        audio_format.setSampleRate(SAMPLE_RATE)
        audio_format.setChannelCount(1)
        audio_format.setSampleFormat(QAudioFormat.SampleFormat.UInt8)
        if not device.isNull() and device.isFormatSupported(audio_format):
            self._create_sink = lambda: QAudioSink(device, audio_format, self)

    def play(self, frequency, milliseconds):
        self.stop()
        if frequency <= 0:
            return
        if not self._prepared:
            self._prepare()
        if self._create_sink is None:
            return
        self._buffer = QBuffer(self)
        self._buffer.setData(QByteArray(square_wave(frequency, milliseconds or MAX_TONE_MS)))
        self._buffer.open(QIODevice.ReadOnly)
        self._sink = self._create_sink()
        self._sink.start(self._buffer)

    def stop(self):
        if self._sink is not None:
            self._sink.stop()
            self._sink.deleteLater()
            self._sink = None
        if self._buffer is not None:
            self._buffer.close()
            self._buffer.deleteLater()
            self._buffer = None
